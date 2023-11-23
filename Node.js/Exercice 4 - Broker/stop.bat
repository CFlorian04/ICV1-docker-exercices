@echo off

REM Stop Ping Server
echo Stopping Ping Server...
docker stop ping-container
docker rm ping-container
echo Ping Server stopped.

REM Stop Pong Server
echo Stopping Pong Server...
docker stop pong-container
docker rm pong-container
echo Pong Server stopped.

REM Stop Annuaire Server
echo Stopping Annuaire Server...
docker stop annuaire-container
docker rm annuaire-container
echo Annuaire Server stopped.

echo All servers stopped.
