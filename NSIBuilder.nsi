!include "MUI2.nsh"
!include "LogicLib.nsh"

Name     "osu! Map Downloader"
OutFile  "osuMapDownloader-setup.exe"
Unicode  True

RequestExecutionLevel user

InstallDir       "$LOCALAPPDATA\Programs\osuMapDownloader"
InstallDirRegKey HKCU "Software\osuMapDownloader" "InstallDir"

VIProductVersion "1.1.0"
VIAddVersionKey /LANG=0 "ProductName"     "osu! Map Downloader"
VIAddVersionKey /LANG=0 "FileDescription" "osu! Map Downloader Setup"
VIAddVersionKey /LANG=0 "FileVersion"     "1.1.0"
VIAddVersionKey /LANG=0 "ProductVersion"  "1.1.0"
VIAddVersionKey /LANG=0 "LegalCopyright"  "Copyright (c) 2026 Saurabh"

!define MUI_ABORTWARNING

!define MUI_WELCOMEPAGE_TITLE "Welcome to osu! Map Downloader Setup"
!define MUI_WELCOMEPAGE_TEXT "This wizard will install osu! Map Downloader on your computer.$\r$\n$\r$\nAfter installation you will need to open Settings › Apps › Default Apps and set osu! Map Downloader as your Web browser so that osu! beatmap links are handled automatically.$\r$\n$\r$\nClick Next to continue."
!insertmacro MUI_PAGE_WELCOME

!insertmacro MUI_PAGE_DIRECTORY

!insertmacro MUI_PAGE_INSTFILES

!define MUI_FINISHPAGE_TITLE "Installation Complete"
!define MUI_FINISHPAGE_TEXT "osu! Map Downloader has been installed successfully.$\r$\n$\r$\nTo finish setup, open Default Apps and choose osu! Map Downloader as your Web browser."
!define MUI_FINISHPAGE_RUN
!define MUI_FINISHPAGE_RUN_TEXT "Open Default Apps settings"
!define MUI_FINISHPAGE_RUN_FUNCTION OpenDefaultApps
!insertmacro MUI_PAGE_FINISH

!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES

!insertmacro MUI_LANGUAGE "English"

Function OpenDefaultApps
  ExecShell "open" "ms-settings:defaultapps"
FunctionEnd

Function .onInit
  ReadRegStr $0 HKCU "Software\osuMapDownloader" "InstallDir"
  ${If} $0 == ""
    StrCpy $INSTDIR "$LOCALAPPDATA\Programs\osuMapDownloader"
  ${EndIf}
FunctionEnd

Section "osu! Map Downloader" SecMain
  SectionIn RO

  SetOutPath "$INSTDIR"
  File /r "dist\osuMapDownloader\*"

  WriteRegStr HKCU "Software\Classes\osuMapDownloaderURL" "" "URL:osu! Map Downloader"
  WriteRegStr HKCU "Software\Classes\osuMapDownloaderURL" "URL Protocol" ""
  WriteRegStr HKCU "Software\Classes\osuMapDownloaderURL\DefaultIcon" "" "$INSTDIR\osuMapDownloader.exe,0"
  WriteRegStr HKCU "Software\Classes\osuMapDownloaderURL\shell\open\command" "" '"$INSTDIR\osuMapDownloader.exe" "%1"'

  WriteRegStr HKCU "Software\Clients\StartMenuInternet\osuMapDownloader" "" "osu! Map Downloader"
  WriteRegStr HKCU "Software\Clients\StartMenuInternet\osuMapDownloader\Capabilities" "ApplicationName" "osu! Map Downloader"
  WriteRegStr HKCU "Software\Clients\StartMenuInternet\osuMapDownloader\Capabilities" "ApplicationDescription" "Download osu! beatmaps directly from osu! beatmap links"
  WriteRegStr HKCU "Software\Clients\StartMenuInternet\osuMapDownloader\Capabilities\URLAssociations" "http"  "osuMapDownloaderURL"
  WriteRegStr HKCU "Software\Clients\StartMenuInternet\osuMapDownloader\Capabilities\URLAssociations" "https" "osuMapDownloaderURL"

  WriteRegStr HKCU "Software\RegisteredApplications" "osuMapDownloader" "Software\Clients\StartMenuInternet\osuMapDownloader\Capabilities"

  WriteRegStr HKCU "Software\osuMapDownloader" "InstallDir" "$INSTDIR"

  CreateDirectory "$SMPROGRAMS\osu! Map Downloader"
  CreateShortcut "$SMPROGRAMS\osu! Map Downloader\osu! Map Downloader.lnk" "$INSTDIR\osuMapDownloader.exe" "" "$INSTDIR\osuMapDownloader.exe" 0 "" "" "Download osu! beatmaps"
  CreateShortcut "$SMPROGRAMS\osu! Map Downloader\Uninstall osu! Map Downloader.lnk" "$INSTDIR\Uninstall.exe"

  WriteRegStr   HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\osuMapDownloader" "DisplayName"          "osu! Map Downloader"
  WriteRegStr   HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\osuMapDownloader" "UninstallString"      '"$INSTDIR\Uninstall.exe"'
  WriteRegStr   HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\osuMapDownloader" "QuietUninstallString" '"$INSTDIR\Uninstall.exe" /S'
  WriteRegStr   HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\osuMapDownloader" "InstallLocation"      "$INSTDIR"
  WriteRegStr   HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\osuMapDownloader" "DisplayIcon"          "$INSTDIR\osuMapDownloader.exe,0"
  WriteRegStr   HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\osuMapDownloader" "Publisher"            ""
  WriteRegStr   HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\osuMapDownloader" "DisplayVersion"       "1.0.0"
  WriteRegStr   HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\osuMapDownloader" "URLInfoAbout"         "https://github.com/Saurabh262004/osu-map-downloader"
  WriteRegDWORD HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\osuMapDownloader" "NoModify" 1
  WriteRegDWORD HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\osuMapDownloader" "NoRepair"  1

  WriteUninstaller "$INSTDIR\Uninstall.exe"

SectionEnd

Section "Uninstall"

  RMDir /r "$INSTDIR"

  RMDir /r "$SMPROGRAMS\osu! Map Downloader"

  DeleteRegKey HKCU "Software\Classes\osuMapDownloaderURL"

  DeleteRegKey HKCU "Software\Clients\StartMenuInternet\osuMapDownloader"

  DeleteRegValue HKCU "Software\RegisteredApplications" "osuMapDownloader"

  DeleteRegKey HKCU "Software\osuMapDownloader"

  DeleteRegKey HKCU "Software\Microsoft\Windows\CurrentVersion\Uninstall\osuMapDownloader"

SectionEnd
