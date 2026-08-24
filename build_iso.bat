@echo off
REM IMPORTANTE: mantener finales de linea CRLF. Si usas LF, los goto se rompen.
setlocal EnableExtensions
set "SELF=%~dp0"

echo ==================================================
echo   Oreimo Portable - ISO en espanol (Windows)
echo ==================================================
echo.
echo Este asistente genera tu ISO con la traduccion al
echo espanol. Arrastra tu ISO sobre este archivo o
echo ejecuta:  build_iso.bat "C:\ruta\tu.iso"
echo.

set "ISO_IN="
set "ISO_OUT_ARG="

:parse
if "%~1"=="" goto :parse_done
if /i "%~1"=="--out" goto :parse_out
set "ISO_IN=%~1"
shift
goto :parse

:parse_out
set "ISO_OUT_ARG=%~2"
shift
shift
goto :parse

:parse_done

if defined ISO_IN goto :have_in
echo Arrastra tu ISO aqui, o escribe la ruta completa:
set /p "ISO_IN=Ruta del ISO: "
if defined ISO_IN goto :have_in
echo No se indico ninguna ISO. Saliendo...
pause
exit /b 1

:have_in
for %%I in ("%ISO_IN%") do set "ISO_IN=%%~fI"
if exist "%ISO_IN%" goto :have_in2
echo No se encontro el archivo: %ISO_IN%
pause
exit /b 1

:have_in2
if defined ISO_OUT_ARG goto :have_out
set "ISO_OUT=%ISO_IN%"
if /i "%ISO_OUT:~-4%"==".iso" set "ISO_OUT=%ISO_OUT:~0,-4%"
set "ISO_OUT=%ISO_OUT%_ES.iso"
goto :out_normalized
:have_out
set "ISO_OUT=%ISO_OUT_ARG%"
:out_normalized
for %%O in ("%ISO_OUT%") do set "ISO_OUT=%%~fO"

echo ISO de entrada : %ISO_IN%
echo ISO de salida  : %ISO_OUT%
echo.

pushd "%SELF%"

REM ----------------------------------------------------------
REM [1/7] Verificar .NET SDK
REM ----------------------------------------------------------
echo [1/7] Verificando .NET SDK...
set "DOTNET="
if exist "%ProgramFiles%\dotnet\dotnet.exe" set "DOTNET=%ProgramFiles%\dotnet\dotnet.exe"
if not defined DOTNET for /f "delims=" %%i in ('where dotnet 2^>nul') do if not defined DOTNET set "DOTNET=%%i"
if defined DOTNET goto :have_dotnet
echo No se encontro .NET SDK. Intentando instalarlo automaticamente...
winget install Microsoft.DotNet.SDK.10 --accept-source-agreements --accept-package-agreements >nul 2>nul
if exist "%ProgramFiles%\dotnet\dotnet.exe" set "DOTNET=%ProgramFiles%\dotnet\dotnet.exe"
if defined DOTNET goto :have_dotnet
echo.
echo No se pudo instalar .NET SDK automaticamente.
echo Descargalo e instalalo desde:
echo   https://dotnet.microsoft.com/download/dotnet/10.0
echo y vuelve a ejecutar este asistente.
pause
exit /b 1

:have_dotnet
echo    .NET SDK encontrado: %DOTNET%
"%DOTNET%" --version >nul 2>nul
if not errorlevel 1 goto :dotnet_ok
echo    ADVERTENCIA: el .NET SDK detectado no responde:
echo    %DOTNET%
echo    Abre una ventana de cmd, ejecuta "where dotnet" y
echo    copia el resultado en un issue del repositorio.
pause
exit /b 1
:dotnet_ok

REM ----------------------------------------------------------
REM [2/7] Obtener la toolchain base (zapan)
REM ----------------------------------------------------------
set "TC=%SELF%toolchain\FastAsyncOreimoTranslateTool-master"
set "ZIP=%SELF%toolchain\toolchain.zip"
if exist "%TC%\RyuujiApi\RyuujiApi.csproj" goto :toolchain_ok
echo [2/7] Descargando la toolchain base (primera vez)...
if exist "%SELF%toolchain" goto :tc_dir_ok
mkdir "%SELF%toolchain"
:tc_dir_ok
curl -L -o "%ZIP%" "https://github.com/zapan/FastAsyncOreimoTranslateTool/archive/refs/heads/master.zip" >nul 2>nul
if not errorlevel 1 goto :zip_ok
powershell -NoProfile -Command "Invoke-WebRequest -Uri 'https://github.com/zapan/FastAsyncOreimoTranslateTool/archive/refs/heads/master.zip' -OutFile '%ZIP%'"
:zip_ok
if exist "%ZIP%" goto :zip_ok2
echo No se pudo descargar la toolchain. Revisa tu conexion a internet.
pause
exit /b 1
:zip_ok2
powershell -NoProfile -Command "Expand-Archive -LiteralPath '%ZIP%' -DestinationPath '%SELF%toolchain' -Force"
del "%ZIP%" >nul 2>nul
:toolchain_ok
if exist "%TC%\RyuujiApi\RyuujiApi.csproj" goto :tc_ready
echo No se pudo preparar la toolchain. Vuelve a intentarlo.
pause
exit /b 1
:tc_ready

REM ----------------------------------------------------------
REM [3/7] Instalar nuestro driver en la toolchain
REM ----------------------------------------------------------
echo [3/7] Preparando el driver OreimoAutomation...
rmdir /s /q "%TC%\OreimoAutomation" 2>nul
xcopy /e /y /q "%SELF%tool\OreimoAutomation" "%TC%\OreimoAutomation\" >nul

REM ----------------------------------------------------------
REM [4/7] Compilar el driver
REM ----------------------------------------------------------
echo [4/7] Compilando el driver (la primera vez puede tardar)...
"%DOTNET%" build "%TC%\OreimoAutomation" -c Release -v q
if not errorlevel 1 goto :build_ok
echo Fallo la compilacion del driver.
pause
exit /b 1
:build_ok
set "DLL=%TC%\OreimoAutomation\bin\Release\net10.0\OreimoAutomation.dll"
if exist "%DLL%" goto :dll_ok
echo No se encontro el driver compilado.
pause
exit /b 1
:dll_ok

REM ----------------------------------------------------------
REM Pipeline
REM ----------------------------------------------------------
REM Se extrae a un directorio temporal y se detecta el disco
REM por su serial (UMD_DATA.BIN: disc1=NPJH-50568, disc2=NPJH-50569)
set "STAGE=%SELF%work\_incoming"
rmdir /s /q "%STAGE%" 2>nul

echo [5/7] Extrayendo tu ISO...
"%DOTNET%" "%DLL%" extract-iso "%ISO_IN%" --base "%STAGE%"
if errorlevel 1 goto :error

set "DISC=disc1"
findstr /c:"NPJH-50569" "%STAGE%\Data\Iso\UMD_DATA.BIN" >nul 2>nul && set "DISC=disc2"
echo    Disco detectado: %DISC%
set "BUILD=%SELF%work\%DISC%"
rmdir /s /q "%BUILD%" 2>nul
move "%STAGE%" "%BUILD%" >nul
if errorlevel 1 goto :error

echo    Extrayendo datos del juego...
"%DOTNET%" "%DLL%" extract-game --base "%BUILD%"
if errorlevel 1 goto :error

echo [6/7] Aplicando la traduccion al espanol...
set "TRAD=%SELF%translation\Translation.json"
if "%DISC%"=="disc2" set "TRAD=%SELF%translation\Translation_disc2.json"
copy /y "%TRAD%" "%BUILD%\Data\Translation.json" >nul
REM 0 = placeholder obligatorio del parser; 570 px = ancho real de la caja
"%DOTNET%" "%DLL%" insert-linebreaks 0 570 --base "%BUILD%"
if errorlevel 1 goto :error

echo    Reempaquetando datos del juego...
"%DOTNET%" "%DLL%" repack-game --base "%BUILD%"
if errorlevel 1 goto :error

echo [7/7] Reempaquetando la ISO final...
set "PATH=%SELF%tool-bin;%PATH%"
"%DOTNET%" "%DLL%" repack-iso "%ISO_OUT%" --base "%BUILD%"
if errorlevel 1 goto :error

echo.
echo ==================================================
echo   !Listo! Tu ISO en espanol:
echo   %ISO_OUT%
echo ==================================================
echo.
explorer /select,"%ISO_OUT%"
pause
popd
exit /b 0

:error
echo.
echo ERROR: no se pudo completar el proceso.
pause
popd
exit /b 1