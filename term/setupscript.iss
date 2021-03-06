; Script generated by the Inno Setup Script Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

[Setup]
; NOTE: The value of AppId uniquely identifies this application.
; Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{DFB2BB75-4B60-49CA-9C3C-18EC52CA4FC9}
AppName=CoinRacing
AppVersion=1.5
;AppVerName=CoinRacing 1.5
AppPublisher=KPU
AppPublisherURL=http://www.example.com/
AppSupportURL=http://www.example.com/
AppUpdatesURL=http://www.example.com/
DefaultDirName={pf}\CoinRacing
DisableProgramGroupPage=yes
OutputDir=C:\Users\kys\Desktop
OutputBaseFilename=setup
Compression=lzma
SolidCompression=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
Source: "C:\Users\kys\OneDrive - kpu.ac.kr\학교\4-2\2D 게임 프로그래밍\MyGit\term\Project\dist\main.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "C:\Users\kys\OneDrive - kpu.ac.kr\학교\4-2\2D 게임 프로그래밍\MyGit\term\Project\dist\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{commonprograms}\CoinRacing"; Filename: "{app}\main.exe"
Name: "{commondesktop}\CoinRacing"; Filename: "{app}\main.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\main.exe"; Description: "{cm:LaunchProgram,CoinRacing}"; Flags: nowait postinstall skipifsilent

[Dirs]
Name: {app}; Permissions: users-full