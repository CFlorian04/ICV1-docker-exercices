@echo off

:: Récupérer le chemin du répertoire du script
set "scriptDir=%~dp0"

:: PING
cd "%scriptDir%serveur1_ping\"
docker rm ex3_ping
docker image rm ex3_ping
docker build -t ex3_ping .
docker run -p 4567:4567 --network ex3_network --name ex3_ping -e MEDIATOR_URL=http://172.18.0.2:8080 ex3_ping

::pause
