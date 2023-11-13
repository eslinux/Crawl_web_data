@echo off
SETLOCAL

::Enable virtual environment
set apps_dir=%~dp0
set url="%1"

::echo python "%apps_dir%crawlWeb.py" %url%
python "%apps_dir%crawlWeb.py" %url%

::echo "%apps_dir%.venv\Scripts\activate.bat"
::python -V
::pip -V

ENDLOCAL