import subprocess
import platform
from Modules.Constants import BROWSER_URL_FLAG, BASE_URL

def buildBrowserArgs(browser: str, browserPath: str, url: str) -> list[str]:
	flag = BROWSER_URL_FLAG.get(browser.lower())
	if flag:
		return [browserPath, flag, url]
	return [browserPath, url]

def openInBrowser(url: str):
	from Modules.Settings import getDefaultBrowser
	from Modules.WindowsBrowsers import getBrowserPathWindows

	browser = getDefaultBrowser()

	if platform.system() == "Windows":
		browserPath = getBrowserPathWindows(browser)
		if browserPath:
			subprocess.Popen(buildBrowserArgs(browser, browserPath, url))
			return

	subprocess.Popen(buildBrowserArgs(browser, browser, url))

def openFile(path: str):
	system = platform.system()

	if system == "Windows":
		subprocess.Popen([path], shell=True)

	elif system == "Darwin":
		subprocess.run(["open", path])

	else:
		subprocess.run(["xdg-open", path])

def getBeatmap(token: str, beatmapID: int):
	import requests

	response = requests.get(
		f"{BASE_URL}/beatmaps/{beatmapID}",
		headers={"Authorization": f"Bearer {token}"},
	)

	response.raise_for_status()

	return response.json()

def resolveBeatmapsetID(beatmpID: int) -> int | None:
	from Modules.Credentials import getAccessToken

	try:
		return getBeatmap(
			getAccessToken(),
			beatmpID
		)['beatmapset_id']
	except:
		return None

def getDownloadURL(beatmapsetID: int, service: str) -> str:
	if service == 'beatconnect':
		return f'https://beatconnect.io/b/{beatmapsetID}'

	if service == 'nerinyan': # application/x-osu-beatmap-archive
		return f'http://dl.nerinyan.moe/v2/d/{beatmapsetID}?nv=1'

	if service == 'catboy': # application/x-osu-beatmap-archive
		return f'https://catboy.best/d/{beatmapsetID}'

	if service == 'sayobot': # application/octet-stream
		return f'https://dl.sayobot.cn/beatmaps/download/novideo/{beatmapsetID}'
