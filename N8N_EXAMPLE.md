# Cómo usar AnimatedWords desde n8n

## Composición: AnimatedWords

Esta composición te permite pasar palabras personalizadas desde n8n y se animarán automáticamente con colores diferentes.

## Parámetros

| Parámetro | Tipo | Requerido | Descripción | Ejemplo |
|-----------|------|-----------|-------------|---------|
| `words` | Array<string> | Sí | Lista de palabras a animar | `["HOLA", "MUNDO"]` |
| `title` | string | No | Título opcional | `"MI VIDEO"` |
| `subtitle` | string | No | Subtítulo opcional | `"Hecho con n8n"` |
| `backgroundColor` | string | No | Color de fondo (hex) | `"#667eea"` |

## Ejemplo 1: Básico - Solo Palabras

**Request JSON:**
```json
{
  "serve_url": "https://n8n-remotion2.alzadl.easypanel.host",
  "composition": "AnimatedWords",
  "inputProps": {
    "words": ["HOLA", "DESDE", "N8N", "CON", "REMOTION"]
  }
}
```

**Resultado:** 5 palabras animadas con colores diferentes

## Ejemplo 2: Con Título y Subtítulo

**Request JSON:**
```json
{
  "serve_url": "https://n8n-remotion2.alzadl.easypanel.host",
  "composition": "AnimatedWords",
  "inputProps": {
    "title": "BIENVENIDO",
    "subtitle": "Video automatizado con n8n + Remotion",
    "words": ["AUTOMATIZACIÓN", "INTELIGENTE", "EFICIENTE", "RAPIDA"]
  }
}
```

**Resultado:** Título arriba + 4 palabras animadas + subtítulo abajo

## Ejemplo 3: Con Color de Fondo Personalizado

**Request JSON:**
```json
{
  "serve_url": "https://n8n-remotion2.alzadl.easypanel.host",
  "composition": "AnimatedWords",
  "inputProps": {
    "words": ["COLOR", "PERSONALIZADO"],
    "title": "MI VIDEO",
    "backgroundColor": "#e74c3c"
  }
}
```

**Resultado:** Fondo rojo con las palabras animadas

## Ejemplo 4: Desde Datos de n8n

Si tienes un nodo anterior con datos:

```json
{
  "serve_url": "https://n8n-remotion2.alzadl.easypanel.host",
  "composition": "AnimatedWords",
  "inputProps": {
    "words": {{ $json.palabras }},
    "title": "{{ $json.titulo }}",
    "subtitle": "{{ $json.mensaje }}"
  }
}
```

## Workflow Completo en n8n

### Nodo 1: HTTP Request - Renderizar Video

**Method:** POST
**URL:** `https://n8n-remotion.alzadl.easypanel.host/api/v1/render/media`

**Body (JSON):**
```json
{
  "serve_url": "https://n8n-remotion2.alzadl.easypanel.host",
  "composition": "AnimatedWords",
  "inputProps": {
    "words": ["PALABRA", "1", "PALABRA", "2", "PALABRA", "3"],
    "title": "",
    "subtitle": ""
  }
}
```

**Respuesta:**
```json
{
  "job_id": "xxx-xxx-xxx",
  "status": "queued",
  "message": "Render job queued successfully"
}
```

### Nodo 2: Wait - Esperar 30 segundos

### Nodo 3: HTTP Request - Verificar Estado

**Method:** GET
**URL:** `https://n8n-remotion.alzadl.easypanel.host/api/v1/jobs/{{ $json.job_id }}`

**Respuesta cuando está completo:**
```json
{
  "job_id": "xxx-xxx-xxx",
  "status": "completed",
  "output_url": "https://n8n-remotion.alzadl.easypanel.host/outputs/xxx.mp4"
}
```

### Nodo 4: IF - Verificar si completó

**Condición:** `{{ $json.status === "completed" }}`

- **Si TRUE:** Descargar video
- **Si FALSE:** Volver al Nodo 2 (Wait)

### Nodo 5: HTTP Request - Descargar Video

**Method:** GET
**URL:** `{{ $json.output_url }}`
**Response Format:** File

## Ejemplos de Palabras

### Nombres:
```json
["MARÍA", "JUAN", "CARLOS", "ANA"]
```

### Numeros:
```json
["1", "2", "3", "4", "5"]
```

### Frases cortas:
```json
 ["HOLA", "MUNDO", "CRUEL", "PERO", "BONITO"]
```

### Con Emojis:
```json
["🎬", "VIDEO", "✨", "FÁCIL", "🚀", "LISTO"]
```

### Palabras largas:
```json
 ["AUTOMATIZACIÓN", "INTELIGENTE", "EFICIENTE"]
```

## Colores Automáticos

Las palabras se colorearán automáticamente con esta paleta:
- Rojo: #FF6B6B
- Turquesa: #4ECDC4
- Azul: #45B7D1
- Verde: #96CEB4
- Amarillo: #FFEAA7
- Y 10 colores más...

Cada palabra tendrá un color diferente automáticamente.

## Duración del Video

- Sin título/subtítulo: ~5 segundos
- Con título: ~10 segundos
- Las palabras aparecen secuencialmente (una cada 0.8 segundos)

## Tips

1. **Máximo 6-8 palabras** para mejor visibilidad
2. Usa **palabras cortas** (1-2 palabras)
3. Los **emojis funcionan** perfectamente ✅
4. El **título y subtítulo son opcionales**
5. Puedes cambiar el **color de fondo** fácilmente
