import tkinter as tk
from tkinter import ttk
import keyring
from Modules.Constants import SERVICE, AVAILABLE_BROWSERS
from Modules.Settings import getAutoDownload, toggleAutoDownload, getDefaultBrowser, setDefaultBrowser

def applyOsuTheme(root: tk.Tk):
	style = ttk.Style(root)
	style.theme_use("clam")

	# BG = "#fff2f7"                 # main window background
	BG = "#fdf5fa"

	# TEXT = "#333333"               # normal text
	TEXT = "#4a4a4a"

	# ACCENT = "#f4bfd6"             # buttons
	# ACCENT_HOVER = "#efadc9"
	# ACCENT_PRESSED = "#e89bbb"

	ACCENT = "#f7c4da"
	ACCENT_HOVER = "#f4b2cf"
	ACCENT_PRESSED = "#ee9fc2"

	INPUT_BG = "#fffafd"           # entry/combobox field
	INPUT_TEXT = "#333333"

	DROPDOWN_BG = "#fffafd"        # combobox dropdown
	DROPDOWN_TEXT = "#333333"

	CHECKBOX_BG = BG

	BORDER = "#e5c6d4"

	DISABLED_BG = "#f0f0f0"
	DISABLED_TEXT = "#888888"

	style.configure(
		"TEntry",
		insertcolor=ACCENT
	)

	# ROOT

	root.configure(bg=BG)

	root.option_add("*Text.selectBackground", ACCENT)
	root.option_add("*Text.selectForeground", TEXT)

	root.option_add("*Entry.selectBackground", ACCENT)
	root.option_add("*Entry.selectForeground", TEXT)

	root.tk_setPalette(
		background=BG,
		foreground=TEXT,
		activeBackground=ACCENT_HOVER,
		activeForeground=TEXT,
		selectBackground=ACCENT,
		selectForeground=TEXT
	)

	# FRAME

	style.configure(
		"TFrame",
		background=BG
	)

	# LABEL

	style.configure(
		"TLabel",
		background=BG,
		foreground=TEXT
	)

	# BUTTON

	style.configure(
		"TButton",
		background=ACCENT,
		foreground=TEXT,
		bordercolor=BORDER,
		lightcolor=ACCENT,
		darkcolor=ACCENT,
		padding=(10, 5)
	)

	style.map(
		"TButton",
		background=[
			("pressed", ACCENT_PRESSED),
			("active", ACCENT_HOVER)
		],
		foreground=[
			("disabled", DISABLED_TEXT)
		]
	)

	# CHECKBUTTON

	style.configure(
		"TCheckbutton",
		background=CHECKBOX_BG,
		foreground=TEXT
	)

	style.map(
		"TCheckbutton",
		background=[
			("active", CHECKBOX_BG),
			("selected", CHECKBOX_BG)
		],
		foreground=[
			("disabled", DISABLED_TEXT)
		]
	)

	# ENTRY

	style.configure(
		"TEntry",
		fieldbackground=INPUT_BG,
		foreground=INPUT_TEXT,
		bordercolor=BORDER,
		insertcolor=INPUT_TEXT
	)

	style.configure(
		"TEntry",
		fieldbackground=INPUT_BG,
		foreground=INPUT_TEXT,
		bordercolor=BORDER,
		lightcolor=BORDER,
		darkcolor=BORDER
	)

	style.map(
		"TEntry",
		bordercolor=[
			("focus", ACCENT)
		],
		lightcolor=[
			("focus", ACCENT)
		],
		darkcolor=[
			("focus", ACCENT)
		]
	)

	# COMBOBOX

	style.configure(
		"TCombobox",
		fieldbackground=INPUT_BG,
		background=INPUT_BG,
		foreground=INPUT_TEXT,
		arrowcolor=TEXT,
		bordercolor=BORDER
	)

	style.map(
		"TCombobox",
		fieldbackground=[
			("readonly", INPUT_BG)
		],
		background=[
			("readonly", INPUT_BG),
			("active", INPUT_BG)
		],
		foreground=[
			("readonly", INPUT_TEXT)
		]
	)

	# TK WIDGETS

	root.option_add("*Background", BG)
	root.option_add("*Foreground", TEXT)
	root.option_add("*Entry.Background", INPUT_BG)
	root.option_add("*Entry.Foreground", INPUT_TEXT)

	# COMBOBOX DROPDOWN LIST

	try:
		root.tk.eval(f'''
			option add *TCombobox*Listbox.background {DROPDOWN_BG}
			option add *TCombobox*Listbox.foreground {DROPDOWN_TEXT}
			option add *TCombobox*Listbox.selectBackground {ACCENT}
			option add *TCombobox*Listbox.selectForeground {TEXT}
		''')
	except:
		pass

def onTop(root: tk.Tk):
	root.attributes("-topmost", True)
	root.lift()

# tk gui for asking to either 1. download beatmap, 2. open url in browser
def askBeatmapAction() -> bool | None:
	root = tk.Tk()
	root.title("osu! Map Downloader")
	root.resizable(False, False)

	applyOsuTheme(root)
	onTop(root)
	root.focus_force()

	result = None

	def download():
		nonlocal result
		result = True
		root.destroy()

	def openPage():
		nonlocal result
		result = False
		root.destroy()

	def cancel():
		root.destroy()

	main = ttk.Frame(root, padding=20)
	main.grid()

	title = ttk.Label(
		main,
		text="Beatmap detected. What would you like to do?",
		font=("Segoe UI", 10, "bold")
	)
	title.grid(row=0, column=0, columnspan=3, pady=(0, 12))

	# buttons row
	btn_frame = ttk.Frame(main)
	btn_frame.grid(row=1, column=0, columnspan=3, pady=(0, 10))

	ttk.Button(
		btn_frame,
		text="Open Page",
		command=openPage,
		width=14
	).grid(row=0, column=0, padx=5)

	ttk.Button(
		btn_frame,
		text="Download",
		command=download,
		width=14
	).grid(row=0, column=1, padx=5)

	autoDownloadVar = tk.BooleanVar(value=getAutoDownload() == '1')

	auto_check = ttk.Checkbutton(
		main,
		text="Automatically download beatmaps",
		variable=autoDownloadVar,
		command=toggleAutoDownload
	)

	auto_check.grid(row=2, column=0, columnspan=3, pady=(5, 0))

	root.protocol("WM_DELETE_WINDOW", cancel)

	root.mainloop()

	return result

# tk gui for editing credentials
def editCredentials():
	root = tk.Tk()
	root.title("osu! API Credentials")
	root.resizable(False, False)

	applyOsuTheme(root)
	onTop(root)

	main = ttk.Frame(root, padding=20)
	main.grid()

	title = ttk.Label(
		main,
		text="API Credentials",
		font=("Segoe UI", 10, "bold")
	)
	title.grid(row=0, column=0, columnspan=2, pady=(0, 12))

	ttk.Label(main, text="Client ID").grid(
		row=1, column=0, sticky="w", pady=5
	)

	clientIDEntry = ttk.Entry(main, width=35)
	clientIDEntry.grid(row=1, column=1, pady=5)

	ttk.Label(main, text="Client Secret").grid(
		row=2, column=0, sticky="w", pady=5
	)

	clientSecretEntry = ttk.Entry(main, width=35, show="*")
	clientSecretEntry.grid(row=2, column=1, pady=5)

	clientID = keyring.get_password(SERVICE, 'client_id')
	clientSecret = keyring.get_password(SERVICE, 'client_secret')

	if clientID:
		clientIDEntry.insert(0, clientID)
	if clientSecret:
		clientSecretEntry.insert(0, clientSecret)

	def save():
		keyring.set_password(SERVICE, 'client_id', clientIDEntry.get().strip())
		keyring.set_password(SERVICE, 'client_secret', clientSecretEntry.get().strip())
		root.destroy()

	ttk.Button(
		main,
		text="Save",
		command=save
	).grid(row=3, column=0, columnspan=2, pady=(15, 0))

	root.mainloop()

def createIdleWindow():
	root = tk.Tk()
	root.title("osu! Map Downloader")
	root.resizable(False, False)

	applyOsuTheme(root)
	onTop(root)
	root.focus_force()

	main = ttk.Frame(root, padding=20)
	main.grid()

	# Title
	title = ttk.Label(
		main,
		text="What would you like to do?",
		font=("Segoe UI", 11, "bold")
	)
	title.grid(row=0, column=0, columnspan=2, pady=(0, 12))

	# Edit Crerentials Button
	edit_btn = ttk.Button(
		main,
		text="Edit Credentials",
		command=editCredentials
	)
	edit_btn.grid(row=1, column=0, columnspan=2, sticky="ew", pady=(0, 10))

	# Default Browser Dropdown
	ttk.Label(
		main,
		text="Default browser:"
	).grid(row=2, column=0, sticky="w", pady=(0, 5))

	browserVar = tk.StringVar(value=getDefaultBrowser())

	browserDropdown = ttk.Combobox(
		main,
		textvariable=browserVar,
		values=AVAILABLE_BROWSERS,
		state="readonly",
		width=18
	)

	browserDropdown.grid(row=3, column=0, columnspan=2, sticky="ew", pady=(0, 10))

	def onBrowserSelected(_event):
		setDefaultBrowser(browserVar.get())

	browserDropdown.bind("<<ComboboxSelected>>", onBrowserSelected)

	# Auto Download Checkbox
	autoDownloadVar = tk.BooleanVar(value=getAutoDownload() == '1')

	auto_check = ttk.Checkbutton(
		main,
		text="Automatically download beatmaps",
		variable=autoDownloadVar,
		command=toggleAutoDownload
	)
	auto_check.grid(row=4, column=0, columnspan=2, sticky="w", pady=(0, 12))

	# small spacing consistency
	for i in range(2):
		main.columnconfigure(i, weight=1)

	root.mainloop()

def createProgressWindow() -> tuple[tk.Tk, ttk.Label]:
	root = tk.Tk()
	root.title("Download Progress")
	root.geometry("200x50+0+0")
	root.resizable(False, False)

	applyOsuTheme(root)
	onTop(root)

	main = ttk.Frame(root)
	main.pack(expand=True, fill="both", padx=10, pady=10)

	label = ttk.Label(
		main,
		text="Starting download...",
		font=("Segoe UI", 10)
	)
	label.pack(expand=True, fill="both")

	root.update_idletasks()

	return root, label
