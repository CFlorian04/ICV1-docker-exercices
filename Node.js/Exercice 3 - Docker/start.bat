
docker-compose down
docker-compose up -d --build

@echo off

@REM start /wait /B cmd /c "stop.bat"

@REM docker network create ping-pong-network


@REM REM Start Annuaire Server
@REM echo Starting Annuaire Server...
@REM cd serveur3_annuaire
@REM docker build -t annuaire-server .
@REM docker run -d --name annuaire-container -p 8080:8080 --network=ping-pong-network annuaire-server
@REM cd ..

@REM REM Start Ping Server
@REM echo Starting Ping Server...
@REM cd serveur1_ping
@REM docker build -t ping-server .
@REM docker run -d --name ping-container -p 4567:4567 --env MEDIATOR_URL=http://host.docker.internal:8080 --network=ping-pong-network ping-server
@REM cd ..

@REM REM Start Pong Server
@REM echo Starting Pong Server...
@REM cd serveur2_pong
@REM docker build -t pong-server .
@REM docker run -d --name pong-container -p 5372:5372 --env MEDIATOR_URL=http://host.docker.internal:8080 --network=ping-pong-network pong-server
@REM cd ..

@REM echo All servers started.
