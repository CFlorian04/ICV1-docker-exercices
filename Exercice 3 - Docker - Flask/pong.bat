@echo off

:: Récupérer le chemin du répertoire du script
set "scriptDir=%~dp0"

:: PONG
cd "%scriptDir%serveur2_pong\"
docker rm ex3_pong
docker image rm ex3_pong
docker build -t ex3_pong .
docker run -p 5372:5372 --network ex3_network --name ex3_pong -e MEDIATOR_URL=http://172.18.0.2:8080 ex3_pong

::pause
