import asyncio
import json

from ichrome import AsyncChromeDaemon


async def main():
    async with AsyncChromeDaemon() as cd:
        async with cd.connect_tab() as tab:
            url = 'http://httpbin.org/ip'

            RequestPatternList = [{
                'urlPattern': '*httpbin.org/ip*',
                'requestStage': 'Response'
            }]
            async with tab.iter_fetch(RequestPatternList) as f:
                await tab.goto(url, timeout=0)
                # only one request could be catched
                event = await f
                print('request event:', json.dumps(event), flush=True)
                response = await f.get_response(event, timeout=5)
                print('response body:', response['data'])

            # 2. disable image requests
            url = 'https://www.bing.com'
            RequestPatternList = [
                {
                    'urlPattern': '*',
                    'resourceType': 'Image',
                    'requestStage': 'Request'
                },
                {
                    'urlPattern': '*',
                    'resourceType': 'Stylesheet',
                    'requestStage': 'Request'
                },
                {
                    'urlPattern': '*',
                    'resourceType': 'Script',
                    'requestStage': 'Request'
                },
            ]
            async with tab.iter_fetch(RequestPatternList, timeout=5) as f:
                await tab.goto(url, timeout=0)
                async for event in f:
                    if f.match_event(event, RequestPatternList[0]):
                        print('abort request image:',
                              tab.get_data_value(event, 'params.request.url'),
                              flush=True)
                        await f.failRequest(event, 'Aborted')
                    elif f.match_event(event, RequestPatternList[1]):
                        print('abort request css:',
                              tab.get_data_value(event, 'params.request.url'),
                              flush=True)
                        await f.failRequest(event, 'ConnectionRefused')
                    elif f.match_event(event, RequestPatternList[2]):
                        print('abort request js:',
                              tab.get_data_value(event, 'params.request.url'),
                              flush=True)
                        await f.failRequest(event, 'AccessDenied')
                await asyncio.sleep(5)


if __name__ == "__main__":
    asyncio.run(main())
