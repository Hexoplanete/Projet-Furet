# Framework Traitement

### Départements pour lesquels ça marche

- SAONE ET LOIRE
- HAUTES_PYRENEES
- SARTHE
- VAR

### Ce que ça fait

input : PDF correspondant à un RAA 

- Réduit qualité PDF
- OCR sur le pdf d'entrée pour générer un nouveau pdf "OCR isé", c'est à dire sous forme de texte
- Séparation des arrêtés d'un recueil : Génère 1 pdf par arrêté du RAA

### Requirements


### Utilisation

python3 .\main.py <Chemin_vers_pdf>

### TESTS : 

Fonctionnent : 

python3 .\main.py ..\input\SAONE_ET_LOIRE\46_pages.pdf
python3 .\main.py ..\input\SAONE_ET_LOIRE\recueil-71-2025-105.pdf
python3 .\main.py ..\input\SAONE_ET_LOIRE\recueil-71-2025-108.pdf

python3 .\main.py ./input/HAUTES_PYRENEES.pdf
python3 .\main.py ./input/SARTHE.pdf
python3 .\main.py ./input/VAR.pdf

