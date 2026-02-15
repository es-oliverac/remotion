#!/bin/bash
# Script para subir el código a GitHub
# Ejecuta este script manualmente en tu terminal

set -e

echo "🚀 Iniciando proceso de subida a GitHub..."

# 1. Inicializar repo git
echo "📦 Inicializando repositorio Git..."
cd "C:/Users/User/Downloads/remotion-main"
git init

# 2. Configurar usuario (usa tus credenciales de GitHub)
echo "⚙️  Configurando usuario Git..."
git config user.name "es-oliverac"
git config user.email "es-oliverac@users.noreply.github.com"

# 3. Añadir todos los archivos
echo "➕ Añadiendo archivos..."
git add .

# 4. Commit inicial
echo "💾 Haciendo commit..."
git commit -m "Add FastAPI server for Remotion - Integration with n8n and Easypanel

- Created packages/fastapi-server with FastAPI application
- Added Node.js wrapper for @remotion/renderer
- Implemented async job queue with WebSocket progress
- Added Dockerfile for containerized deployment
- Included n8n integration examples and curl documentation
- Ready for easypanel deployment"

# 5. Añadir remote
echo "🔗 Configurando remoto..."
git remote add origin https://github.com/es-oliverac/remotion.git

# 6. Push (te pedirá credenciales)
echo "⬆️  Haciendo push a GitHub..."
echo "Cuando te pida credenciales:"
echo "  Username: es-oliverac"
echo "  Password: TU_PAT_AQUI"
echo ""
git branch -M main
git push -u origin main

echo "✅ Completado!"
