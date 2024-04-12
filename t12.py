import PyChromeDevTools

chrome = PyChromeDevTools.ChromeInterface()
chrome.Network.enable()
chrome.Page.enable()

chrome.Page.navigate(url="http://www.facebook.com")
event,messages=chrome.wait_event("Page.frameStoppedLoading", timeout=60)

for m in messages:
    if "method" in m and m["method"] == "Network.responseReceived":
        try:
            url=m["params"]["response"]["url"]
            print (url)
        except:
            pass