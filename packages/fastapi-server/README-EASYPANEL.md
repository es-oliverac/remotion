# Despliegue en Easypanel - Guía Paso a Paso

## Opción 1: Usar Imagen Docker (Recomendado)

### Paso 1: Build y Push la Imagen

En tu máquina local:

```bash
# Build la imagen
docker build -t TU_USUARIO/remotion-fastapi:latest .

# Push a Docker Hub
docker push TU_USUARIO/remotion-fastapi:latest
```

### Paso 2: Crear Servicio en Easypanel

1. En Easypanel, crea un nuevo servicio tipo "Compose"

2. Pega el siguiente contenido:

```yaml
version: '3.8'

services:
  remotion-api:
    image: TU_USUARIO/remotion-fastapi:latest
    container_name: remotion-fastapi
    volumes:
      - remotion-outputs:/app/outputs
    environment:
      - APP_NAME=Remotion FastAPI Server
      - DEBUG=false
      - MAX_CONCURRENT_RENDERS=2
      - OUTPUT_DIR=/app/outputs
      - BASE_URL=https://tu-dominio.com  # ← Cambiar esto
      - MAX_BROWSER_INSTANCES=3
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/api/v1/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    restart: unless-stopped
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2048M

volumes:
  remotion-outputs:
```

3. Configura el dominio en Easypanel

4. Ajusta `BASE_URL` a tu dominio real

## Opción 2: Build Directo en Easypanel

Si Easypanel soporta build desde GitHub:

1. Sube el código a GitHub

2. En Easypanel, usa la URL del repositorio

3. Configura el contexto del build a `packages/fastapi-server`

## Variables de Entorno Importantes

| Variable | Valor | Descripción |
|----------|-------|-------------|
| `BASE_URL` | `https://tu-dominio.com` | URL pública para descargar videos |
| `MAX_CONCURRENT_RENDERS` | `2` | Videos simultáneos (ajustar según CPU) |
| `MAX_BROWSER_INSTANCES` | `3` | Instancias Chrome en pool |
| `OUTPUT_DIR` | `/app/outputs` | Directorio de salida |
| `DEBUG` | `false` | Modo debug |

## Probar el Despliegue

```bash
# Health check
curl https://tu-dominio.com/api/v1/health

# Render video de prueba
curl -X POST https://tu-dominio.com/api/v1/render/media \
  -H "Content-Type: application/json" \
  -d '{
    "serve_url": "https://remotion-assets.com/bundle.zip",
    "composition": "MyVideo",
    "input_props": {"title": "Test desde Easypanel"}
  }'
```

## Integración con n8n

Una vez desplegado, usa la URL `https://tu-dominio.com` en lugar de `http://localhost:8000` en los ejemplos de curl.

## Solución de Problemas

### El container usa mucha memoria
- Reduce `MAX_CONCURRENT_RENDERS` a `1`
- Reduce `MAX_BROWSER_INSTANCES` a `2`

### Los videos no se pueden descargar
- Verifica que `BASE_URL` tenga tu dominio correcto
- Asegúrate de que el volumen `remotion-outputs` esté montado

### El container falla al iniciar
- Verifica los logs en Easypanel
- Asegúrate de que la imagen Docker sea compatible con Linux (amd64)

### Health check falla
- Aumenta `start_period` a `60s`
- Verifica que el puerto sea `8000`
