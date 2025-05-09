@echo off

python -m venv .venv

call .venv\Scripts\activate

echo.

python -m furet

pause