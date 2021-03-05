#define VerFile FileOpen("D:\CODES\Python\EbookCollection\test\VERSION.txt")
#define FileAppVersion FileRead(VerFile)
#expr FileClose(VerFile)

#define VerFile FileOpen("D:\CODES\Python\EbookCollection\test\VERSION_BUILD.txt")
#define FileAppBuild FileRead(VerFile)
#expr FileClose(VerFile)

#define MyAppName "eBookCollection"
#define MyAppPublisher "LordKBX Workshop"
#define MyAppURL "https://github.com/LordKBX/eBookCollection"

[Setup]
; NOTE: The value of AppId uniquely identifies this application.
; Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{7D39BD8F-2E4A-4C20-8137-454F85D050CC}
AppName={#MyAppName}
AppVersion={#FileAppVersion}.{#FileAppBuild}
VersionInfoVersion={#FileAppVersion}.{#FileAppBuild}
;AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
LicenseFile=D:\CODES\Python\EbookCollection\LICENSE.txt
SetupIconFile=D:\CODES\Python\EbookCollection\ressources\icons\app_icon.ico
Compression=lzma
SolidCompression=yes    
;lowest or admin
PrivilegesRequired=admin
OutputBaseFilename=setup_{#FileAppVersion}.{#FileAppBuild}_compiled 

[Languages]
Name: "english"; MessagesFile: ".\Default.isl"

[Files]
;Source: "D:\CODES\Python\EbookCollection\*.pyw"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\CODES\Python\EbookCollection\test\build\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "D:\CODES\Python\EbookCollection\LICENSE.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\CODES\Python\EbookCollection\version.txt"; DestDir: "{app}"; Flags: ignoreversion

Source: "D:\CODES\Python\EbookCollection\ressources\*"; DestDir: "{app}\ressources"; Flags: ignoreversion recursesubdirs createallsubdirs

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"

[Icons]
Name: "{commonprograms}\{#MyAppName}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{commonprograms}\{#MyAppName}\{#MyAppName}"; Filename: "{app}\library.exe debug"; WorkingDir: "{app}"; IconFilename: "{app}\library.exe"; IconIndex: 0; Flags: createonlyiffileexists
Name: "{commondesktop}\{#MyAppName}"; Filename: "{app}\library.exe debug"; WorkingDir: "{app}"; IconFilename: "{app}\library.exe"; IconIndex: 0; Tasks: desktopicon

[UninstallDelete]
Type: files; Name: "{app}\__pycache__\*" 
Type: files; Name: "{app}\home\__pycache__\*"   
Type: files; Name: "{app}\reader\__pycache__\*"
Type: files; Name: "{app}\data\*"
Type: files; Name: "{app}\icons\*"
Type: files; Name: "{app}\tmp\*"
Type: files; Name: "{app}\tools\*"