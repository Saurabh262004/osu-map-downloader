from Modules.Constants import SERVICE, TOKEN_URL

def getCredentials():
	import keyring
	from Modules.GUI import editCredentials

	clientID = keyring.get_password(
		SERVICE,
		'client_id'
	)

	clientSecret = keyring.get_password(
		SERVICE,
		'client_secret'
	)

	if not clientID or not clientSecret:
		editCredentials()

		clientID = keyring.get_password(
			SERVICE,
			'client_id'
		)

		clientSecret = keyring.get_password(
			SERVICE,
			'client_secret'
		)

	return clientID, clientSecret

def getAccessToken() -> str:
	import requests

	clientID, clientSecret = getCredentials()

	response = requests.post(TOKEN_URL, data={
		"client_id": clientID,
		"client_secret": clientSecret,
		"grant_type": "client_credentials",
		"scope": "public",
	})

	response.raise_for_status()

	return response.json()["access_token"]
