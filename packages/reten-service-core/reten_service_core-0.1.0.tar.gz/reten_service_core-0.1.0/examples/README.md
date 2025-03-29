# Ejemplos de reten-service-core

Este directorio contiene ejemplos prácticos de cómo usar los diferentes componentes de reten-service-core.

## Requisitos

Antes de ejecutar los ejemplos, asegúrate de:

1. Tener Python 3.10 o superior instalado
2. Tener el paquete instalado en modo desarrollo:
   ```bash
   pip install -e ".[dev]"
   ```
3. Configurar las variables de entorno necesarias:
   ```bash
   export VALID_API_KEYS='["test-key"]'
   export GCP_PROJECT_ID="your-project-id"
   export GCP_SERVICE_ACCOUNT_PATH="/path/to/credentials.json"  # Opcional
   ```

## Ejemplos Disponibles

### 1. API Básica (`basic_api.py`)

Un ejemplo simple que muestra cómo crear una API FastAPI con autenticación por API Key y logging básico.

**Características:**
- Autenticación con API Key
- Logging configurado
- Endpoint básico

**Ejecución:**
```bash
python examples/basic_api.py
```

### 2. Cliente BigQuery (`bigquery_example.py`)

Demuestra cómo usar el cliente de BigQuery para ejecutar consultas y manejar errores.

**Características:**
- Inicialización del cliente
- Ejecución de consultas con parámetros
- Verificación de existencia de datasets/tablas
- Manejo de errores

**Ejecución:**
```bash
python examples/bigquery_example.py
```

### 3. Servicio Completo (`complete_service.py`)

Un ejemplo completo que integra todos los componentes de la librería en un servicio funcional.

**Características:**
- FastAPI con autenticación API Key
- Logging estructurado con contexto de request
- Integración con BigQuery
- Middleware para logging de requests
- Health checks y métricas
- Manejo de errores

**Endpoints:**
- `GET /health`: Health check del servicio
- `GET /metrics`: Métricas desde BigQuery
  - Parámetros:
    - `days`: Número de días a consultar (default: 7)
    - `dataset_id`: ID del dataset (default: "analytics")
    - `table_id`: ID de la tabla (default: "events")

**Ejecución:**
```bash
python examples/complete_service.py
```

**Prueba de endpoints:**
```bash
# Health check
curl http://localhost:8000/health

# Métricas (con API Key)
curl -H "X-API-Key: test-key" http://localhost:8000/metrics?days=30
```

### 4. Autenticación Detallada (`auth_examples.py`)

Un ejemplo detallado que muestra todas las características del sistema de autenticación por API Key.

**Características:**
- Configuración básica y avanzada del middleware
- Exclusión de rutas específicas
- Personalización del header de autenticación
- Logging de intentos de autenticación
- Manejo personalizado de errores

**Endpoints:**
- `GET /private`: Endpoint que requiere autenticación
- `GET /public`: Endpoint público sin autenticación
- `GET /error`: Endpoint para demostrar manejo de errores

**Ejecución:**
```bash
python examples/auth_examples.py
```

**Prueba de endpoints:**
```bash
# Endpoint privado (con auth válida)
curl -H "X-API-Key: test-key-1" http://localhost:8000/private

# Endpoint privado (auth inválida)
curl -H "X-API-Key: invalid-key" http://localhost:8000/private

# Endpoint público (sin auth)
curl http://localhost:8000/public

# Endpoint de error
curl -H "X-API-Key: test-key-1" http://localhost:8000/error
```

## Mejores Prácticas Demostradas

Los ejemplos ilustran las siguientes mejores prácticas:

1. **Configuración**
   - Uso de variables de entorno
   - Configuración centralizada con Settings
   - Manejo seguro de credenciales

2. **Logging**
   - Logging estructurado
   - Contexto de request
   - Métricas de performance

3. **Manejo de Errores**
   - Try/catch apropiado
   - HTTP exceptions
   - Logging de errores con contexto

4. **Seguridad**
   - Autenticación API Key
   - No exposición de credenciales
   - Validación de inputs

## Personalización

Cada ejemplo puede ser personalizado modificando las variables de entorno o los parámetros en el código. Consulta los comentarios en cada archivo para más detalles.
