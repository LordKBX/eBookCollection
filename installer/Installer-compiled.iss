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
Compression=lzma2/ultra64
SolidCompression=True
;lowest or admin
PrivilegesRequired=admin
OutputBaseFilename=setup_{#FileAppVersion}.{#FileAppBuild}_compiled 
DisableFinishedPage=True
TimeStampsInUTC=True
UninstallDisplayIcon={uninstallexe}
VersionInfoCompany=LorkKBX Workshop
SetupLogging=True
ArchitecturesInstallIn64BitMode=x64
CompressionThreads=2
MinVersion=0,6.1

[Languages]
Name: "english"; MessagesFile: ".\Default.isl"
Name: "french"; MessagesFile: "compiler:Languages\French.isl"
   
#include "C:\Program Files (x86)\Inno Download Plugin\idp.iss"

[Files]
;Source: "D:\CODES\Python\EbookCollection\*.pyw"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\CODES\Python\EbookCollection\test\build\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "D:\CODES\Python\EbookCollection\LICENSE.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "D:\CODES\Python\EbookCollection\version.txt"; DestDir: "{app}"; Flags: ignoreversion

Source: "D:\CODES\Python\EbookCollection\ressources\*"; DestDir: "{app}\ressources"; Flags: ignoreversion recursesubdirs createallsubdirs

[Registry]
Root: HKLM; Subkey: SOFTWARE\{#MyAppPublisher}\{#MyAppName}; ValueType: string; ValueName: Version; ValueData: "{#FileAppVersion}.{#FileAppBuild}"; Flags: uninsdeletekey

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"

[Icons]
Name: "{commonprograms}\{#MyAppName}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{commonprograms}\{#MyAppName}\{#MyAppName}"; Filename: "{app}\library.exe"; WorkingDir: "{app}"; IconFilename: "{app}\library.exe"; IconIndex: 0
Name: "{commondesktop}\{#MyAppName}"; Filename: "{app}\library.exe debug"; WorkingDir: "{app}"; IconFilename: "{app}\library.exe"; IconIndex: 0; Tasks: desktopicon

[UninstallDelete]
Type: files; Name: "{app}\__pycache__\*" 
Type: files; Name: "{app}\home\__pycache__\*"   
Type: files; Name: "{app}\reader\__pycache__\*"
Type: files; Name: "{app}\data\*"
Type: files; Name: "{app}\icons\*"
Type: files; Name: "{app}\tmp\*"
Type: files; Name: "{app}\tools\*"

[Code]
const
  SHCONTCH_NOPROGRESSBOX = 4;
  SHCONTCH_RESPONDYESTOALL = 16; 

function GetAppVersion(): String;
begin
  Result:='{#FileAppVersion}.{#FileAppBuild}';
end;

function GetInstalledVersion(): String;
var
  InstalledVersion: String;
begin
  InstalledVersion := '';
  RegQueryStringValue(HKLM, 'SOFTWARE\{#MyAppPublisher}\{#MyAppName}', 'Version', InstalledVersion);
  Result := InstalledVersion;
end;

function GetAppID(param: String): String;
begin
  Result := '{#MyAppName}';
end;

procedure UnZip(ZipPath, TargetPath: string); 
var
  Shell: Variant;
  ZipFile: Variant;
  TargetFolder: Variant;
begin
  Shell := CreateOleObject('Shell.Application');

  ZipFile := Shell.NameSpace(ZipPath);
  if VarIsClear(ZipFile) then
    RaiseException(Format('ZIP file "%s" does not exist or cannot be opened', [ZipPath]));

  TargetFolder := Shell.NameSpace(TargetPath);
  if VarIsClear(TargetFolder) then
    RaiseException(Format('Target path "%s" does not exist', [TargetPath]));

  TargetFolder.CopyHere(ZipFile.Items, SHCONTCH_NOPROGRESSBOX or SHCONTCH_RESPONDYESTOALL);
end;

procedure InitializeWizard();
begin
  WizardForm.WelcomeLabel1.Visible := True;   
  WizardForm.WelcomeLabel2.Visible := True;

  if not RegKeyExists(HKEY_LOCAL_MACHINE, 'SOFTWARE\\7-Zip') then
  begin
    idpAddFileSize('http://sd-36502.dedibox.fr/eBookCollection/7zip.zip',expandconstant('{tmp}\eBookCollection-7zip.zip'), 964490)
  end;
  //Start the download after the "Ready to install" screen is shown
  idpDownloadAfter(wpReady);
end;   
     
procedure CurStepChanged(CurStep: TSetupStep);
begin
 if CurStep=ssInstall then begin //Lets install those files that were downloaded for us
  CreateDir(expandconstant('{sd}\Users\{username}\{#MyAppName}\tools'))  

  if not RegKeyExists(HKEY_LOCAL_MACHINE, 'SOFTWARE\\7-Zip') then
  begin 
    UnZip(expandconstant('{tmp}\eBookCollection-7zip.zip'), expandconstant('{sd}\Users\{username}\{#MyAppName}\tools'));
  end;
 end;
end;

function InitializeSetup(): Boolean;
var
  Response: Integer;
  PrevDir: String;
  InstalledVersion: String;
  Version: String;
  //VersionError: String;
begin
  Result := true;
  // read the installation folder
  PrevDir := GetInstalledVersion();

  if length(Prevdir) > 0 then begin
    // I found the folder so it's an upgrade.
    
    // compare versions
    InstalledVersion := GetInstalledVersion();
    Version := GetAppVersion();
    if (InstalledVersion < Version) then begin
      Result := True;
    end else if (InstalledVersion = Version) then begin
      if ActiveLanguage = 'English' then begin
        Response := MsgBox(
          'This version of "{#MyAppName}" is already installed.' + #13#13 +
          'Do you want to continue with the update installation ?', mbError, MB_YESNO
        );
      end else begin
        Response := MsgBox(
          'La présente version de "{#MyAppName}" est la même que celle installée.' + #13#13 +
          'Souhaitez vous vraiment faire une mise à jour ?', mbError, MB_YESNO
        );
      end;
      Result := (Response = IDYES);
    end else begin
      if ActiveLanguage = 'English' then begin
        Response := MsgBox(
          'The installed version of "{#MyAppName}" is newer than this update.' + #13#13 +
          'The existing installation is v'+ InstalledVersion +'.  This update will change the installation to v'+ Version + #13#13 +
          'Do you want to continue with the reverse update installation ?', mbError, MB_YESNO
        );
      end else begin
        Response := MsgBox(
          'la version installée de "{#MyAppName}" est plus récente que celle proposée.' + #13#13 +
          'Laversion actuelle est la v'+ InstalledVersion +'. La version installeur est la v'+ Version + #13#13 +
          'Souhaitez vous vraiment faire cette mise à niveau ?', mbError, MB_YESNO
        );
      end;
      Result := (Response = IDYES);
    end;
  end else begin
    // Didn't find the folder so its a fresh installation.
    Result:=true;
  end;
end;

function ShouldSkipPage(PageID: Integer): Boolean;
var
  PrevDir:String;
begin
  PrevDir := GetInstalledVersion();
  if length(Prevdir) > 0 then begin
    // skip selectdir if It's an upgrade
    if (PageID = wpSelectDir) then begin
     Result := true;
    end else if (PageID = wpSelectProgramGroup) then begin
     Result := true;
    end else if (PageID = wpSelectTasks) then begin
      Result := true;
    end else begin
      Result := false;
    end;
  end;
end;
