@echo off

python -m venv .venv

call .venv\Scripts\activate

pip install uv
uv sync

pip install ocrmypdf PyMuPDF spacy
python -m spacy download fr_core_news_sm

echo.

python -m furet

pause