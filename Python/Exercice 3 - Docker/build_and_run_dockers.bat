
:: Création du réseau
docker network create ex3_network

start /B cmd /c "annuaire.bat"
start /B cmd /c "ping.bat"
start /B cmd /c "pong.bat"
