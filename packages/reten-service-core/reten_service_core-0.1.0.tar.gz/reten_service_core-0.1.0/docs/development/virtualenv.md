# Configuración del Entorno Virtual

Este documento describe la configuración del entorno virtual para el desarrollo de `reten-service-core`.

## Requisitos Previos

- Python 3.10 o superior
- pip (última versión recomendada)
- virtualenv o venv (incluido con Python 3)

## Creación del Entorno Virtual

1. Crear un nuevo entorno virtual:
   ```bash
   python -m venv venv
   ```

2. Activar el entorno virtual:

   **Linux/macOS**:
   ```bash
   source venv/bin/activate
   ```

   **Windows**:
   ```bash
   venv\Scripts\activate
   ```

## Instalación de Dependencias

1. Actualizar pip a la última versión:
   ```bash
   python -m pip install --upgrade pip
   ```

2. Instalar el paquete en modo desarrollo:
   ```bash
   pip install -e ".[dev]"
   ```

   Esto instalará:
   - Todas las dependencias base del proyecto
   - Dependencias de desarrollo (pytest, ruff, etc.)

## Verificación de la Instalación

1. Verificar que el entorno está activado:
   ```bash
   which python  # Debería mostrar el python del entorno virtual
   ```

2. Verificar las dependencias instaladas:
   ```bash
   pip list
   ```

3. Ejecutar los tests para confirmar que todo funciona:
   ```bash
   pytest
   ```

## Mantenimiento

1. Actualizar dependencias:
   ```bash
   pip install --upgrade -e ".[dev]"
   ```

2. Desactivar el entorno virtual:
   ```bash
   deactivate
   ```

3. Recrear el entorno virtual (si es necesario):
   ```bash
   deactivate  # Si está activado
   rm -rf venv
   python -m venv venv
   source venv/bin/activate  # O venv\Scripts\activate en Windows
   pip install -e ".[dev]"
   ```

## Solución de Problemas

1. Si hay problemas con las dependencias:
   ```bash
   pip install --force-reinstall -e ".[dev]"
   ```

2. Si hay conflictos de versiones:
   - Revisar `pyproject.toml` para las versiones específicas
   - Usar `pip freeze > requirements.txt` para guardar un estado funcional
   - Usar `pip install -r requirements.txt` para restaurar ese estado

## Integración con IDEs

### VS Code
1. Seleccionar el intérprete del entorno virtual:
   - `Cmd/Ctrl + Shift + P` -> "Python: Select Interpreter"
   - Seleccionar el python del entorno virtual (`./venv/bin/python`)

### PyCharm
1. Configurar el intérprete:
   - Settings -> Project -> Python Interpreter
   - Añadir intérprete -> Existing Environment
   - Seleccionar `./venv/bin/python`
