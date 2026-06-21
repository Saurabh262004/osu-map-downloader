import keyring
from Modules.Constants import SERVICE

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

def getAutoDownload():
	return keyring.get_password(
		SERVICE,
		'auto_download'
	)

def toggleAutoDownload():
	if (getAutoDownload() == '1'):
		disableAutoDownload()
	else:
		enableAutoDownload()

def getDefaultBrowser():
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
