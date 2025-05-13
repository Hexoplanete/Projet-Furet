# Framework Traitement


### Départements pour lesquels ça a été testé et ça marche

- SAONE ET LOIRE
- HAUTES_PYRENEES
- SARTHE
- VAR

### Ce que ça fait

input : PDF correspondant à un RAA 

- Réduit qualité PDF avec magick (ouput/apres_magick/) -> Génère un nouveau pdf
- OCR sur le pdf d'entrée pour générer un nouveau pdf "OCR isé", c'est à dire sous forme de texte (ouput/apres_ocr/) -> Génère un nouveau pdf ocrisé
- Séparation des arrêtés d'un recueil : (ouput/apres_separation/{Nom_RAA}/) -> Génère 1 pdf par arrêté du RAA 
- Assignation des mots clefs à un arrêté (ouput/apres_mot_cle/{Nom_RAA}/) -> Génère des .txt contenant les mots clefs qui ont matchés

**Informations récupérées :**

| Info / RAA       | Endroit où on récupère                                              |                       
|------------------|---------------------------------------------------------------------|
| raaNumber        | Extraction Caractéristiques (code juliette à intégrer)              |                                                                 
| departement      | Crawler                                                             | OK
| date publication | Crawler                                                             | OK
| link             | Crawler                                                             | OK


| Info / Arrêté    | Endroit où on récupère                                              |                  
|------------------|---------------------------------------------------------------------|
| doc_type         | ?                                                                   |
| arreteNumber     | Extraction Caractéristiques (code juliette à intégrer)              | TO DO
| title            | Extraction Caractéristiques (code juliette à intégrer)              | TO DO
| signingDate      | On récupère pas au final                                            | 
| topic            | Dans getKeyWords() car le topic c'est des keywords                  |
| startPage        | Separation RAA                                                      | OK 
| endPage          | Separation RAA                                                      | OK
| campaign         | Dans getKeyWords() car campagne dépend du keyword qui matche        | TO DO now
                                                                                         

### Requirements

### Utilisation

Voir README de PROJET-FURET ou lancer launchPythonEnvWithInstall

### A corriger 

#### Assignation mots clef

Destruction peut matcher avec des trucs de batiment par exemple

Armes aussi !





