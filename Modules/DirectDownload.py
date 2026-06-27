# create a small tk window at top-left corner of the screen, put it on top
# make one label and update that label as progress goes on:

def directDownloadProcess(downloadURL: str, root, label):
	import requests
	from pathlib import Path
	from Modules.Helpers import openFile

	downloads = Path.home() / "Downloads"

	response = requests.get(
		downloadURL,
		headers={
			"User-Agent": (
				"Mozilla/5.0 (X11; Linux x86_64; rv:149.0) "
				"Gecko/20100101 Firefox/149.0"
			)
		},
		allow_redirects=True,
		stream=True
	)

	response.raise_for_status()

	label.config(text=f"Validating content...")
	root.update_idletasks()

	contentType = (
		response.headers
		.get("Content-Type", "")
		.split(";")[0]
	)

	if contentType not in {
		"application/x-osu-beatmap-archive",
		"application/octet-stream",
		"application/zip"
	}:
		print(f"Unexpected content type: {contentType}")
		return False

	filename = "beatmap.osz"

	contentDisposition = response.headers.get(
		"Content-Disposition"
	)

	if (contentDisposition and ("filename=" in contentDisposition)):
		filename = (
			contentDisposition
			.split("filename=")[1]
			.strip('"')
		)

	filePath = downloads / filename

	label.config(text=f"Writing to disk...")
	root.update_idletasks()

	with open(filePath, "wb") as f:
		for chunk in response.iter_content(
			chunk_size=8192
		):
			if chunk:
				f.write(chunk)

	with open(filePath, "rb") as f:
		magic = f.read(4)

	if magic != b"PK\x03\x04":
		print("Downloaded file is not a valid zip")
		filePath.unlink(missing_ok=True)
		return False

	label.config(text=f"Opening file...")
	root.update_idletasks()

	openFile(str(filePath))

	return True
