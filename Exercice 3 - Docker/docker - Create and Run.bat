@echo off

:: Récupérer le chemin du répertoire du script
set "scriptDir=%~dp0"

:: Annuaire
cd "%scriptDir%serveur3_annuaire\"
docker rm ex3_annuaire
docker image rm  ex3_annuaire
docker build -t ex3_annuaire .
docker run -p 8080:8080 --network ex3_network --name ex3_annuaire ex3_annuaire
cd "%scriptDir%..\.."

:: PING
cd "%scriptDir%serveur1_ping\"
docker rm ex3_ping
docker image rm ex3_ping
docker build -t ex3_ping .
docker run -p 4567:4567 --network ex3_network --name ex3_ping -e MEDIATOR_URL=http://172.18.0.2:8080 ex3_ping

cd "%scriptDir%..\.."

:: PONG
cd "%scriptDir%serveur2_pong\"
docker rm ex3_pong
docker image rm ex3_pong
docker build -t ex3_pong .
docker run -p 5372:5372 --network ex3_network --name ex3_pong -e MEDIATOR_URL=http://172.18.0.2:8080 ex3_pong
cd "%scriptDir%..\.."

::pause
