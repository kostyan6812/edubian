; example1.nsi
;
; This script is perhaps one of the simplest NSIs you can make. All of the
; optional settings are left to their default settings. The installer simply 
; prompts the user asking them where to install, and drops a copy of example1.nsi
; there. 


;--------------------------------

; The name of the installer
Name "MIREA EDUBIAN"

; The file to write
OutFile "mireaedubian_1.0_x64.exe"

; The default installation directory
InstallDir $%HOMEDRIVE%\edubian

; Request application privileges for Windows Vista
RequestExecutionLevel admin


;--------------------------------

; Pages

Page directory
Page instfiles

;--------------------------------

; The stuff to install
Section "" ;No components page, name is not important

  ; Set output path to the installation directory.
  SetOutPath $INSTDIR
 inetc::get https://qemu.weilnetz.de/w64/2017/qemu-w64-setup-20170808.exe "$TEMP\qemu-w64-setup-20170808.exe"
 Pop $R0 ;Get the return value
  StrCmp $R0 "success" +3
    MessageBox MB_OK "Download failed: $R0"
    Quit
 ExecWait "$TEMP\qemu-w64-setup-20170808.exe"
 Delete "$TEMP\qemu-w64-setup-20170808.exe"
 inetc::get https://swupdate.openvpn.org/community/releases/tap-windows-9.21.2.exe "$TEMP\tap-windows-9.21.2.exe"
 Pop $R0 ;Get the return value
  StrCmp $R0 "success" +3
    MessageBox MB_OK "Download failed: $R0"
    Quit
 ExecWait "$TEMP\tap-windows-9.21.2.exe"
 Delete "$TEMP\tap-windows-9.21.2.exe"
 inetc::get https://the.earth.li/~sgtatham/putty/latest/w64/putty.exe "putty.exe" 
 Pop $R0 ;Get the return value
  StrCmp $R0 "success" +3
    MessageBox MB_OK "Download failed: $R0"
    Quit
 ; Put file there
 File edubian.cmd
 File bzImage
 File rootfs.qcow2

 
SectionEnd ; end the section

