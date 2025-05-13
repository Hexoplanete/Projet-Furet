# Project FURET


# Installation

```bash
python3 -m venv .venv #  ou `python -m venv .venv` sous Windows
source .venv/bin/activate # ou `.venv\Scripts\activate.bat` sous Windows
```

```bash
pip install uv
uv sync
```

```bash
uv run pyinstaller --onefile -n furet src/furet/__main__.py 
```

```bash
uv run pyinstaller --onefile -n furet src/furet/__main__.py 
```

# Requirements Traitement

python -m spacy download fr_core_news_sm
