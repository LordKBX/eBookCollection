
#define MyAppName "EbookCollection"
#define MyAppVersion "0.1_alpha002"
#define MyAppPublisher "Future Code Technologies"
#define MyAppURL "https://github.com/LordKBX/EbookCollection"

[Setup]
; NOTE: The value of AppId uniquely identifies this application.
; Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{F18AF3E6-A408-4DB9-BFFF-D283FAF9519B}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
;AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={userdocs}\{#MyAppName}
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
LicenseFile=D:\CODES\Python\EbookCollection\LICENSE
SetupIconFile=D:\CODES\Python\EbookCollection\icons\app_icon.ico
Compression=lzma
SolidCompression=yes    
; or admin
PrivilegesRequired=lowest 

[Languages]
Name: "english"; MessagesFile: ".\Default.isl"

[Files]
;Source: "D:\CODES\Python\EbookCollection\*.pyw"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\CODES\Python\EbookCollection\*.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\CODES\Python\EbookCollection\*.bat"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\CODES\Python\EbookCollection\*.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\CODES\Python\EbookCollection\home\*.py"; DestDir: "{app}\home"; Flags: ignoreversion
Source: "D:\CODES\Python\EbookCollection\home\*.ui"; DestDir: "{app}\home"; Flags: ignoreversion 
Source: "D:\CODES\Python\EbookCollection\reader\*.py"; DestDir: "{app}\reader"; Flags: ignoreversion
Source: "D:\CODES\Python\EbookCollection\icons\*.ico"; DestDir: "{app}\icons"; Flags: ignoreversion  
Source: "D:\CODES\Python\EbookCollection\icons\*.png"; DestDir: "{app}\icons"; Flags: ignoreversion     
Source: "D:\CODES\Python\EbookCollection\icons\black\*.png"; DestDir: "{app}\icons\black"; Flags: ignoreversion
Source: "D:\CODES\Python\EbookCollection\icons\white\*.png"; DestDir: "{app}\icons\white"; Flags: ignoreversion
Source: "D:\CODES\Python\EbookCollection\tools\7zip\*"; DestDir: "{app}\tools\7zip"; Flags: ignoreversion
Source: "D:\CODES\Python\EbookCollection\tools\poppler\*"; DestDir: "{app}\tools\poppler"; Flags: ignoreversion

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"

[Icons]
Name: "{commonprograms}\{#MyAppName}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{commonprograms}\{#MyAppName}\{#MyAppName}"; Filename: "python {app}\main.py"; WorkingDir: "{app}"; IconFilename: "{app}\icons\app_icon.ico"; IconIndex: 0; Flags: createonlyiffileexists
Name: "{commondesktop}\{#MyAppName}"; Filename: "python {app}\main.py"; WorkingDir: "{app}"; IconFilename: "{app}\icons\app_icon.ico"; IconIndex: 0; Tasks: desktopicon

[UninstallDelete]
Type: files; Name: "{app}\__pycache__\*" 
Type: files; Name: "{app}\home\__pycache__\*"   
Type: files; Name: "{app}\reader\__pycache__\*"
Type: files; Name: "{app}\data\*"
Type: files; Name: "{app}\icons\*"
Type: files; Name: "{app}\tmp\*"
Type: files; Name: "{app}\tools\*"