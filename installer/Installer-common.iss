#define MyAppName "eBookCollection"
#define MyAppVersion "0.1.0.5"
#define MyAppPublisher "LordKBX Workshop"
#define MyAppURL "https://github.com/LordKBX/EbookCollection"

[Setup]
; NOTE: The value of AppId uniquely identifies this application.
; Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{7D39BD8F-2E4A-4C20-8137-454F85D050CC}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
VersionInfoVersion={#MyAppVersion}
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
Source: "D:\CODES\Python\EbookCollection\editor\*.py"; DestDir: "{app}\editor"; Flags: ignoreversion

Source: "D:\CODES\Python\EbookCollection\ressources\cover_patterns\*"; DestDir: "{app}\ressources\cover_patterns"; Flags: ignoreversion  

Source: "D:\CODES\Python\EbookCollection\ressources\fonts\Arimo\*"; DestDir: "{app}\ressources\fonts\Arimo"; Flags: ignoreversion
Source: "D:\CODES\Python\EbookCollection\ressources\fonts\CamingoCode\*"; DestDir: "{app}\ressources\fonts\CamingoCode"; Flags: ignoreversion
Source: "D:\CODES\Python\EbookCollection\ressources\fonts\Cooper Hewitt\*"; DestDir: "{app}\ressources\fonts\Cooper Hewitt"; Flags: ignoreversion
Source: "D:\CODES\Python\EbookCollection\ressources\fonts\Exo1\*"; DestDir: "{app}\ressources\fonts\Exo1"; Flags: ignoreversion
Source: "D:\CODES\Python\EbookCollection\ressources\fonts\HK Grotesk\*"; DestDir: "{app}\ressources\fonts\HK Grotesk"; Flags: ignoreversion
Source: "D:\CODES\Python\EbookCollection\ressources\fonts\Josefin sans\*"; DestDir: "{app}\ressources\fonts\Josefin sans"; Flags: ignoreversion
Source: "D:\CODES\Python\EbookCollection\ressources\fonts\Kanit\*"; DestDir: "{app}\ressources\fonts\Kanit"; Flags: ignoreversion
Source: "D:\CODES\Python\EbookCollection\ressources\fonts\Lobster Two\*"; DestDir: "{app}\ressources\fonts\Lobster Two"; Flags: ignoreversion
Source: "D:\CODES\Python\EbookCollection\ressources\fonts\Montserrat\*"; DestDir: "{app}\ressources\fonts\Montserrat"; Flags: ignoreversion
Source: "D:\CODES\Python\EbookCollection\ressources\fonts\Montserrat Alternates\*"; DestDir: "{app}\ressources\fonts\Montserrat Alternates"; Flags: ignoreversion
Source: "D:\CODES\Python\EbookCollection\ressources\fonts\Open Sans\*"; DestDir: "{app}\ressources\fonts\Open Sans"; Flags: ignoreversion
Source: "D:\CODES\Python\EbookCollection\ressources\fonts\Oswald\*"; DestDir: "{app}\ressources\fonts\Oswald"; Flags: ignoreversion
Source: "D:\CODES\Python\EbookCollection\ressources\fonts\Quicksand\*"; DestDir: "{app}\ressources\fonts\Quicksand"; Flags: ignoreversion
Source: "D:\CODES\Python\EbookCollection\ressources\fonts\Raleway\*"; DestDir: "{app}\ressources\fonts\Raleway"; Flags: ignoreversion
Source: "D:\CODES\Python\EbookCollection\ressources\fonts\Roboto\*"; DestDir: "{app}\ressources\fonts\Roboto"; Flags: ignoreversion
Source: "D:\CODES\Python\EbookCollection\ressources\fonts\Rubik\*"; DestDir: "{app}\ressources\fonts\Rubik"; Flags: ignoreversion
Source: "D:\CODES\Python\EbookCollection\ressources\fonts\Sinkin Sans\*"; DestDir: "{app}\ressources\fonts\Sinkin Sans"; Flags: ignoreversion
Source: "D:\CODES\Python\EbookCollection\ressources\fonts\Source Sans Pro\*"; DestDir: "{app}\ressources\fonts\Source Sans Pro"; Flags: ignoreversion
Source: "D:\CODES\Python\EbookCollection\ressources\fonts\Ubuntu\*"; DestDir: "{app}\ressources\fonts\Ubuntu"; Flags: ignoreversion

Source: "D:\CODES\Python\EbookCollection\ressources\icons\*"; DestDir: "{app}\ressources\icons"; Flags: ignoreversion
Source: "D:\CODES\Python\EbookCollection\ressources\icons\black\*"; DestDir: "{app}\ressources\icons\black"; Flags: ignoreversion
Source: "D:\CODES\Python\EbookCollection\ressources\icons\tmp\*"; DestDir: "{app}\ressources\icons\tmp"; Flags: ignoreversion
Source: "D:\CODES\Python\EbookCollection\ressources\icons\white\*"; DestDir: "{app}\ressources\icons\white"; Flags: ignoreversion

Source: "D:\CODES\Python\EbookCollection\ressources\langs\*"; DestDir: "{app}\ressources\langs"; Flags: ignoreversion
Source: "D:\CODES\Python\EbookCollection\ressources\styles\*"; DestDir: "{app}\ressources\styles"; Flags: ignoreversion

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