# Project FURET

## Motivation

Chaque préfecture de département publie sur son site des Recueils d'Actes Administratifs, très volumineux, hérérogènes et difficiles à analyser manuellement, qui contiennent diverses décisions pouvant intéresser particuliers, associations et entreprises.  Notre application permet de récupérer, analyser, stocker et accéder facilement et automatiquement à des arrêtés préfectoraux selon le domaine souhaité par l'utilisateur (chasse, terrains, permis ...).


# Installation

Référez vous à la [section d'Installation](https://github.com/Hexoplanete/Projet-Furet/wiki#installation) du wiki.

Pour le développement, rendez vous dans [section développeur](https://github.com/Hexoplanete/Projet-Furet/wiki/Home-d%C3%A9velopeur) du wiki.



## Contexte

Ce projet à été réalisé dans le cadre du projet SMART à l'INSA de Lyon par [l'équipe Hexoplanète](https://github.com/Hexoplanete/Projet-Furet/wiki/%C3%80-propos-de-l'Hexoplan%C3%A8te).




## Commandes testées pour build executable

#### Commande qui semble fonctionner pour enlever erreurs liées à  fr_core_news_sm et ocrmy pdf (mais reste au moins erreurs crawler.regions )
<!-- uv run pyinstaller --onefile -n furet --add-data "libs/fr_core_news_sm/fr_core_news_sm-3.8.0/;fr_core_news_sm" --collect-data ocrmypdf src/furet/__main__.py -->


#### Tests non concluants pour crawler.regions

 <!-- uv run pyinstaller --onefile -n furet --add-data "src/furet/crawler/regions/;crawler-regions" --add-data "libs/fr_core_news_sm/fr_core_news_sm-3.8.0/;fr_core_news_sm"  --additional-hooks-dir=hooks src/ --collect-data ocrmypdf src/furet/__main__.py

 uv run pyinstaller --onefile -n furet --add-data "src/furet/crawler/regions/;crawler-regions" --add-data "src/furet/crawler/;crawler"  --add-data "libs/fr_core_news_sm/fr_core_news_sm-3.8.0/;fr_core_news_sm"  --hidden-import=furet.crawler.regions --collect-data ocrmypdf src/furet/__main__.py --> 

<!-- uv run pyinstaller --onefile -n furet --add-data "libs/fr_core_news_sm/fr_core_news_sm-3.8.0/;fr_core_news_sm" --add-data "src/furet/crawler/regions/;crawler-regions"  --collect-data ocrmypdf --additional-hooks-dir=hook src/furet/__main__.py -->