where java
IF %ERRORLEVEL% EQU 0 (ECHO "JAVA IS INSTALLED") ELSE (choco install adoptopenjdk11)
where docker
IF %ERRORLEVEL% EQU 0 (ECHO "DOCKER IS INSTALLED") ELSE (choco install docker-desktop)
