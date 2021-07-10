@echo off
Set filename=%userprofile%
For %%A in ("%filename%") do (
    Set Folder=%%~dpA
    Set Name=%%~nxA
)
echo.Folder is: %Folder%
echo.Name is: %Name%

cd \
Set Drivename=%CD%
echo.Drivename is: %Drivename%

takeown /f "C:\Program Files\WindowsApps\PythonSoftwareFoundation.Python.3.9_3.9.1776.0_x64__qbz5n2kfra8p0" /r
icacls "%Drivename%\program files\windowsapps" /grant %Name%:F /T
icacls "C:\program files\windowsapps\python*" /grant avivo:(OI)(CI)F /T
pause