# This script will create a virtualenv and auto install 
# all dependencies that are needed for this program

function Green
{
    process { Write-Host $_ -ForegroundColor Green }
}

function Red
{
    process { Write-Host $_ -ForegroundColor Red }
}

function Yellow
{
    process { Write-Host $_ -ForegroundColor Yellow }
}


# opens directory in which the script is located
cd $PSScriptRoot
Write-Output "Working Dir:" | Green
Write-Output $PSScriptRoot | Yellow

Write-Output "Installing virtualenv" | Green
pip install virtualenv

Write-Output "Creating virtualenv" | Green
python -m virtualenv .venv

Write-Output "Activating virtualenv" | Green
.\.venv\Scripts\activate

Write-Output "Installing dependencies" | Green
pip install -r .\requirements.txt

Write-Output "Creating activate.ps1" | Green
# to acticvate the virtualenv using autofill instead of entering the directory path given below
"`$cdir` = pwd
cd `$PSScriptRoot`
.\.venv\Scripts\activate
cd `$cdir` " > activate.ps1
# to deactivate the virtualenv just enter deactivate in the terminal

Write-Output "Done" | Green
Write-Output "Use '.\activate.ps1' to enable virtualenv in future uses" | Green