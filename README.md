# StockGuard 🛡️
Sistema de validación y almacenamiento de inventario que permite gestionar stock de forma robusta, con validaciones automáticas y persistencia de datos.

---

# 📋 Descripción

**StockGuard** es una librería Python para la gestión segura de inventario. Proporciona:

- **Modelos de datos** (`models.py`) — estructuras tipadas para representar productos y movimientos de stock.
- **Motor principal** (`stockguard.py`) — lógica de negocio para altas, bajas y consultas de inventario.
- **Capa de almacenamiento** (`storage.py`) — persistencia de datos con lectura/escritura desacoplada del dominio.
- **Validador** (`validator.py`) — reglas de integridad para evitar datos corruptos antes de persistirlos.

---

# ⚙️ Instalación

## Requisitos previos

- Python 3.10 o superior
- `pip`

## Pasos

```bash
# 1. Clona el repositorio
git clone https://github.com/tu-usuario/stockguard.git
cd stockguard

# 2. Crea y activa un entorno virtual (recomendado)
python -m venv .venv
source .venv/bin/activate       # Linux / macOS
.venv\Scripts\activate          # Windows

# 3. Instala las dependencias
pip install -r requirements.txt

# 4. Instala el paquete en modo editable (opcional, para desarrollo)
pip install -e .
```

---

# 🧪 Cómo ejecutar los tests

El proyecto usa **pytest**. Todos los tests se encuentran en el directorio `tests/`.

```bash
# Ejecutar toda la suite
pytest

# Con salida detallada
pytest -v

# Solo un módulo concreto
pytest tests/test_validator.py -v

# Con cobertura de código
pytest --cov=stockguard --cov-report=term-missing
```

Los tests cubren:

| Fichero de test        | Módulo bajo prueba   |
|------------------------|----------------------|
| `test_models.py`       | `models.py`          |
| `test_storage.py`      | `storage.py`         |
| `test_validator.py`    | `validator.py`       |

---

# 🚀 Uso básico (CLI)

```bash
# Ejemplo: añadir un producto al inventario
python -m stockguard add --sku "ABC-001" --nombre "Tornillo M6" --cantidad 500

# Consultar stock de un producto
python -m stockguard query --sku "ABC-001"

# Validar el estado del inventario completo
python -m stockguard validate
```

**Salida esperada:**

```
$ python -m stockguard query --sku "ABC-001"
┌─────────────┬──────────────┬───────────┐
│ SKU         │ Nombre       │ Cantidad  │
├─────────────┼──────────────┼───────────┤
│ ABC-001     │ Tornillo M6  │ 500       │
└─────────────┴──────────────┴───────────┘
```

> **Nota:** reemplaza la captura anterior con una screenshot real de tu terminal una vez que el CLI esté operativo.

---

# 🤖 Uso de IA

## Qué generó la IA

Durante el desarrollo de este proyecto se utilizó IA generativa (Claude, de Anthropic) para:

- **Estructura inicial del proyecto**: generación del scaffold de carpetas (`stockguard/`, `tests/`), `setup.cfg`, `pytest.ini` y `.gitignore`.
- **Esqueleto de módulos**: borradores iniciales de `models.py` (clases de datos con `dataclasses`), `storage.py` (lectura/escritura JSON) y `validator.py` (validaciones básicas de tipo y rango).
- **Suite de tests base**: propuesta inicial de casos de prueba para `test_models.py` y `test_storage.py`, incluyendo fixtures de `conftest.py`.
- **Workflow de CI**: fichero `.github/workflows/CI.yml` con los pasos de instalación, lint y ejecución de pytest.
- **Este README**: estructura, badges y secciones generadas con asistencia de IA y revisadas manualmente.

## Qué modifiqué yo

- **Lógica de negocio en `stockguard.py`**: implementación completa de las operaciones de inventario (consulta, alta, baja) adaptadas a los requisitos reales del proyecto.
- **Validaciones en `validator.py`**: ajuste de las reglas de integridad (umbrales de stock mínimo, formatos de SKU) según las necesidades del dominio.
- **Tests adicionales en `test_validator.py`**: casos edge no contemplados por la IA (valores negativos, SKUs duplicados, campos vacíos).
- **Corrección de bugs**: varios errores de lógica en el borrador de `storage.py` relacionados con el manejo de rutas y codificación UTF-8.
- **Configuración de `setup.cfg`**: ajuste de metadatos, entry points del CLI y dependencias de desarrollo.

---

# 🔄 Integración continua

El proyecto cuenta con un pipeline de CI configurado en **GitHub Actions** (`.github/workflows/CI.yml`) que se ejecuta en cada push y pull request:

```yaml
on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: pip install -r requirements.txt
      - run: pytest -v
```

El badge al inicio de este README refleja el estado actual del pipeline en la rama `main`.

---

# 📁 Estructura del proyecto

```
stockguard/
├── .github/
│   └── workflows/
│       └── CI.yml
├── stockguard/
│   ├── __init__.py
│   ├── models.py
│   ├── stockguard.py
│   ├── storage.py
│   └── validator.py
├── tests/
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_storage.py
│   └── test_validator.py
├── conftest.py
├── requirements.txt
├── setup.cfg
├── pytest.ini
├── Audit.md
└── README.md
```

---

# 📄 Licencia

Este proyecto está bajo la licencia **MIT**. Consulta el fichero [LICENSE](LICENSE MIT) para más detalles.