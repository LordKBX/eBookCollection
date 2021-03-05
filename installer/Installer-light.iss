#define VerFile FileOpen("D:\CODES\Python\EbookCollection\test\VERSION.txt")
#define FileAppVersion FileRead(VerFile)
#expr FileClose(VerFile)

#define VerFile FileOpen("D:\CODES\Python\EbookCollection\test\VERSION_BUILD.txt")
#define FileAppBuild FileRead(VerFile)
#expr FileClose(VerFile)

#define MyAppName "eBookCollection"
#define MyAppPublisher "LordKBX Workshop"
#define MyAppURL "https://github.com/LordKBX/EbookCollection"

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
DefaultDirName={userdocs}\{#MyAppName}
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
LicenseFile=D:\CODES\Python\EbookCollection\LICENSE.txt
SetupIconFile=D:\CODES\Python\EbookCollection\ressources\icons\app_icon.ico
Compression=lzma
SolidCompression=yes    
;lowest or admin
PrivilegesRequired=admin
OutputBaseFilename=setup_{#FileAppVersion}.{#FileAppBuild}_light

[Languages]
Name: "english"; MessagesFile: ".\Default.isl"

[Files]
Source: "D:\CODES\Python\EbookCollection\*.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\CODES\Python\EbookCollection\*.ui"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\CODES\Python\EbookCollection\*.bat"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\CODES\Python\EbookCollection\*.txt"; DestDir: "{app}"; Flags: ignoreversion

Source: "D:\CODES\Python\EbookCollection\editor\*.py"; DestDir: "{app}\editor"; Flags: ignoreversion
Source: "D:\CODES\Python\EbookCollection\editor\*.ui"; DestDir: "{app}\editor"; Flags: ignoreversion 
Source: "D:\CODES\Python\EbookCollection\editor\*.bat"; DestDir: "{app}\editor"; Flags: ignoreversion 

Source: "D:\CODES\Python\EbookCollection\reader\*.py"; DestDir: "{app}\reader"; Flags: ignoreversion
Source: "D:\CODES\Python\EbookCollection\reader\*.ui"; DestDir: "{app}\reader"; Flags: ignoreversion
Source: "D:\CODES\Python\EbookCollection\reader\*.bat"; DestDir: "{app}\reader"; Flags: ignoreversion

Source: "D:\CODES\Python\EbookCollection\common\*.py"; DestDir: "{app}\common"; Flags: ignoreversion

Source: "D:\CODES\Python\EbookCollection\ressources\*"; DestDir: "{app}\ressources"; Flags: ignoreversion recursesubdirs createallsubdirs  

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"

[Icons]
Name: "{commonprograms}\{#MyAppName}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{commonprograms}\{#MyAppName}\{#MyAppName}"; Filename: "python {app}\main.py"; WorkingDir: "{app}"; IconFilename: "{app}\ressources\icons\app_icon.ico"; IconIndex: 0; Flags: createonlyiffileexists
Name: "{commondesktop}\{#MyAppName}"; Filename: "python {app}\main.py"; WorkingDir: "{app}"; IconFilename: "{app}\ressources\icons\app_icon.ico"; IconIndex: 0; Tasks: desktopicon

[UninstallDelete]
Type: files; Name: "{app}\__pycache__\*" 
Type: files; Name: "{app}\editor\__pycache__\*"   
Type: files; Name: "{app}\reader\__pycache__\*"
Type: files; Name: "{app}\ressources\*"