import keyring
from Modules.Constants import SERVICE

# ==== auto download preference ====

def disableAutoDownload():
	keyring.set_password(
		SERVICE,
		'auto_download',
		'0'
	)

def enableAutoDownload():
	keyring.set_password(
		SERVICE,
		'auto_download',
		'1'
	)

def getAutoDownload() -> str | None:
	return keyring.get_password(
		SERVICE,
		'auto_download'
	)

def toggleAutoDownload():
	if (getAutoDownload() == '1'):
		disableAutoDownload()
	else:
		enableAutoDownload()

# ==== video download preference ====

def enableVideoDownloadPreference():
	keyring.set_password(
		SERVICE,
		'video_download',
		'1'
	)

def disableVideoDownloadPreference():
	keyring.set_password(
		SERVICE,
		'video_download',
		'0'
	)

def getVideoDownloadPreference() -> str | None:
	return keyring.get_password(
		SERVICE,
		'video_download'
	)

def toggleVideoDownloadPreference():
	if (getVideoDownloadPreference() == '1'):
		disableVideoDownloadPreference()
	else:
		enableVideoDownloadPreference()

# === default browser preference ====

def getDefaultBrowser() -> str:
	browser = keyring.get_password(
		SERVICE,
		'browser'
	)

	if browser: return browser

	setDefaultBrowser('firefox')

	return 'firefox'

def setDefaultBrowser(browser: str):
	keyring.set_password(
		SERVICE,
		'browser',
		browser
	)
