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

# Requirements Traitement

pip install ocrmypdf PyMuPDF spacy 

python -m spacy download fr_core_news_sm




# Outils à télécharger avec des setups classiques de windows

Magick : https://imagemagick.org/archive/binaries/ImageMagick-7.1.1-47-Q16-HDRI-x64-dll.exe (Réduit la qualité des images -> Nécessaire pour prétraitement avant OCR !)
GhostScript : https://github.com/ArtifexSoftware/ghostpdl-downloads/releases/download/gs10051/gs10051w64.exe (Requirements direct de la bibliothèque OCR utilisée )
Tesseract : https://github.com/tesseract-ocr/tesseract/releases/download/5.5.0/tesseract-ocr-w64-setup-5.5.0.20241111.exe (Requirements direct de la bibliothèque OCR utilisée )