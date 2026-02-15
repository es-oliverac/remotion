@echo off
REM Script para subir el código a GitHub
REM Ejecuta este archivo manualmente en tu terminal

echo 🚀 Iniciando proceso de subida a GitHub...
echo.

cd C:\Users\User\Downloads\remotion-main

REM 1. Inicializar repo git
echo 📦 Inicializando repositorio Git...
git init
echo.

REM 2. Configurar usuario
echo ⚙️  Configurando usuario Git...
git config user.name "es-oliverac"
git config user.email "es-oliverac@users.noreply.github.com"
echo.

REM 3. Añadir todos los archivos
echo ➕ Añadiendo archivos...
git add .
echo.

REM 4. Commit inicial
echo 💾 Haciendo commit...
git commit -m "Add FastAPI server for Remotion - Integration with n8n and Easypanel"
echo.

REM 5. Añadir remote
echo 🔗 Configurando remoto...
git remote add origin https://github.com/es-oliverac/remotion.git
echo.

REM 6. Push
echo ⬆️  Haciendo push a GitHub...
echo.
echo Cuando te pida credenciales:
echo   Username: es-oliverac
echo   Password: TU_PAT_AQUI
echo.
git branch -M main
git push -u origin main

echo.
echo ✅ Completado!
pause
