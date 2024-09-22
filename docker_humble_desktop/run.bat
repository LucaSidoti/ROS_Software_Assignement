@REM @echo off
@REM setlocal

@REM REM Check if the Xauthority file exists and prepare Xauthority data
@REM set XAUTH=%TEMP%\.docker.xauth
@REM echo Preparing Xauthority data...

@REM for /f "tokens=*" %%i in ('xauth nlist :0 2^>nul ^| tail -n 1 ^| sed -e "s/^..../ffff/"') do set xauth_list=%%i

@REM if not exist %XAUTH% (
@REM     if not "%xauth_list%"=="" (
@REM         echo %xauth_list% | xauth -f %XAUTH% nmerge -
@REM     ) else (
@REM         type nul > %XAUTH%
@REM     )
@REM     icacls %XAUTH% /grant *S-1-1-0:R
@REM )
    
@REM echo Done.
@REM echo.
@REM echo Verifying file contents:
@REM file %XAUTH%
@REM echo --^> It should say "X11 Xauthority data."
@REM echo.
@REM echo Permissions:
@REM icacls %XAUTH%
@REM echo.
@REM echo Running docker...

@REM REM Get the current working directory
@REM for /f %%i in ('cd') do set current_dir=%%i

@REM REM Use dirname to get the parent directory
@REM for %%i in ("%current_dir%") do set parent_dir=%%~dpi
@REM set parent_dir=%parent_dir:~0,-1%

@REM docker run -it ^
@REM     --name humble_desktop ^
@REM     --rm ^
@REM     --privileged ^
@REM     --net=host ^
@REM     -e DISPLAY=unix!DISPLAY! ^
@REM     -e QT_X11_NO_MITSHM=1 ^
@REM     -e XAUTHORITY=%XAUTH% ^
@REM     -v /tmp/.X11-unix:/tmp/.X11-unix:rw ^
@REM     -v %XAUTH%:%XAUTH% ^
@REM     -v /run/user/1000/at-spi:/run/user/1000/at-spi ^
@REM     -v /dev:/dev ^
@REM     -v %parent_dir%:/home/xplore/dev_ws/src ^
@REM     -v base_humble_desktop_home_volume:/home/xplore ^
@REM     ghcr.io/epflxplore/docker_commons:humble-desktop

@REM endlocal
@REM pause

@echo off
setlocal

REM Prepare Xauthority data
echo Preparing Xauthority data...
set "XAUTHORITY=%TEMP%\.docker.xauth"

REM Create Xauthority file if it does not exist
if not exist "%XAUTHORITY%" (
    echo Creating Xauthority file...
    type nul > "%XAUTHORITY%"
)

echo Done.

REM Convert Windows path to Unix format for Docker
set "XAUTHORITY_UNIX=%TEMP%/.docker.xauth"
set "PARENT_DIR=%CD%\.."

REM Run Docker
docker run -it ^
    --name humble_desktop ^
    --rm ^
    --net=host ^
    -e DISPLAY=%DISPLAY% ^
    -e QT_X11_NO_MITSHM=1 ^
    -v /tmp/.X11-unix:/tmp/.X11-unix:rw ^
    -v "%XAUTHORITY_UNIX%:/home/xplore/.Xauthority:rw" ^
    -v "%PARENT_DIR%:/home/xplore/dev_ws/src" ^
    -v base_humble_desktop_home_volume:/home/xplore ^
    ghcr.io/epflxplore/docker_commons:humble-desktop

endlocal

