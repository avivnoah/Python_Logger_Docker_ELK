@echo off


:start
cls

set python_ver=39

python ./get-pip.py
cd "%AppData%\..\Local\Programs\Python\Python*\Scripts"

python -m pip install --upgrade pip

pip install logging
pip install requests.auth
pip install python-logstash
pip install sys
pip install random
pip install calendar
pip install time
pip install requests
pip install json
pip install os
pip install datetime
pip install event

Set filename=%userprofile%
For %%A in ("%filename%") do (
    Set Folder=%%~dpA
    Set Name=%%~nxA
)
echo.Folder is: %Folder%
echo.Name is: %Name%


cd \
Set Drivename=%CD%

cd "%Drivename%\Program Files\WindowsApps\Python*"

python -m pip install --upgrade pip

pip install logging
pip install requests.auth
pip install python-logstash
pip install sys
pip install random
pip install calendar
pip install time
pip install requests
pip install json
pip install os
pip install datetime
pip install event