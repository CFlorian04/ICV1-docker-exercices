@echo off

:: Récupérer le chemin du répertoire du script
set "scriptDir=%~dp0"

:: Annuaire
cd "%scriptDir%serveur3_annuaire\"
docker rm ex3_annuaire
docker image rm  ex3_annuaire
docker build -t ex3_annuaire .
docker run -p 8080:8080 --network ex3_network --name ex3_annuaire ex3_annuaire

::pause
