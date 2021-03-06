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

#include ReadReg(HKEY_LOCAL_MACHINE,'Software\Sherlock Software\InnoTools\Downloader','ScriptPath','');

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

[Code] 
const
  SHCONTCH_NOPROGRESSBOX = 4;
  SHCONTCH_RESPONDYESTOALL = 16;

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
  
  itd_init;

  if not RegKeyExists(HKEY_LOCAL_MACHINE, 'SOFTWARE\\7-Zip') then
  begin
    itd_addfile('http://sd-36502.dedibox.fr/eBookCollection/7zip.zip',expandconstant('{tmp}\eBookCollection-7zip.zip'));
  end;
  
  
  //Start the download after the "Ready to install" screen is shown
  itd_downloadafter(wpReady);

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