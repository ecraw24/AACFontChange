@echo on
setlocal EnableExtensions

:: Customize Window
title TouchChat Mass Button Editor

::renames the whichever file is dropped to .zip so it can be extracted
copy "%~1" "temp.zip"

::copies directory of file just dropped
set temppath=%cd%
set filename=%~n1
::echo %filename%


::unzips file to a Temp directory in the folder that contains the .ce file
setlocal
cd /d %~dp0
Call :UnZipFile "%temppath%\Temp\" "%temppath%\temp.zip"
exit /b

:UnZipFile <ExtractTo> <newzipfile>
set vbs="%temp%\_.vbs"
if exist %vbs% del /f /q %vbs%
>%vbs%  echo Set fso = CreateObject("Scripting.FileSystemObject")
>>%vbs% echo If NOT fso.FolderExists(%1) Then
>>%vbs% echo fso.CreateFolder(%1)
>>%vbs% echo End If
>>%vbs% echo set objShell = CreateObject("Shell.Application")
>>%vbs% echo set FilesInZip=objShell.NameSpace(%2).items
>>%vbs% echo objShell.NameSpace(%1).CopyHere(FilesInZip)
>>%vbs% echo Set fso = Nothing
>>%vbs% echo Set objShell = Nothing
cscript //nologo %vbs%
if exist %vbs% del /f /q %vbs%

::renames the c4v and changes it's extension to .db so it can be modified by SQLite3
ren "%temppath%\Temp\*.c4v" *.db

::finds the DB file and sets the fn variable to its file name
for %%A IN ("%temppath%\Temp\*.db") DO (set fn=%%~nxA)

CLS

echo Font options: Amaranth, Arial, Caudex, Courier New, Frutiger Linotype, Gentium Basic, Georgia, Istok Web, Josefin Sans, Puritan, Tahoma, Times New Roman, Trebuchet MS, Ubuntu, Verdana

::prompt user for which fonts to change from and to
set /P sourcefont=Enter font to change FROM: 
set /P destfont=Enter font to change TO: 

::runs SQLite script on DB file to change font
"c:\Program Files (x86)\SQLite3\sqlite3" "%temppath%\Temp\%fn%" "update button_styles set font_name='%destfont%' where font_name='%sourcefont%';"

echo You changed all %sourcefont% to %destfont%

echo Font options (6 - 150)

set /P sourcefontsize=Enter font size to change FROM: 
set /P destfontsize=Enter font size to change TO: 

::runs SQLite script on DB file to change font size
"c:\Program Files (x86)\SQLite3\sqlite3" "%temppath%\Temp\%fn%" "update button_styles set font_height='%destfontsize%' where font_height='%sourcefontsize%';"

echo You changed all %sourcefontsize% to %destfontsize%

::renames the .db file back to .c4v to prepare it to be zipped again
ren "%temppath%\Temp\*.db" *.c4v

::using 7-zip to zip all files into one file
"C:\Program Files\7-Zip\7z.exe" a -tzip "%temppath%\%filename%-new.zip" "%temppath%\Temp\*.*"

::renames the .zip file back to .ce so it can be used by ChatEditor and TouchChat
ren "%temppath%\%filename%-new.zip" *.ce

del /q "%temppath%\temp.zip"
rd /s /q "%temppath%\Temp"