# Estructura del Proyecto

```
PDF A MP3/
├── main.py                  # Punto de entrada CLI - Validación y orquestación
├── extractor.py             # Extracción de texto desde PDF
├── splitter.py              # División de texto en partes de ~40 minutos
├── tts.py                   # Generación de audio WAV usando TTS offline
├── encoder.py               # Conversión de WAV a MP3
├── pipeline.py              # Pipeline principal de procesamiento
├── web.py                   # Interfaz web Flask para pruebas locales
├── requirements.txt         # Dependencias del proyecto
├── .gitignore              # Archivos ignorados por Git
├── README.md               # Documentación principal
├── RESUMEN_DETALLADO.md    # Documentación técnica completa
├── PROJECT_STRUCTURE.md    # Este archivo
└── templates/
    └── index.html          # Interfaz web HTML/CSS/JavaScript
```

## Módulos Principales

### `main.py`
- Validación de argumentos CLI
- Validación del directorio de entrada
- Verificación de existencia de exactamente un PDF
- Inicialización del pipeline

### `extractor.py`
- Lectura de archivos PDF
- Extracción de texto preservando orden
- Cálculo de estadísticas (páginas, palabras)

### `splitter.py`
- División de texto en partes de ~6,000 palabras
- Lógica de fusión para partes pequeñas
- Mantiene orden del texto

### `tts.py`
- Generación de audio WAV desde texto
- Utiliza pyttsx3 (TTS offline)
- Configuración de velocidad y volumen

### `encoder.py`
- Conversión de WAV a MP3
- Optimización (mono, 64kbps)
- Requiere ffmpeg

### `pipeline.py`
- Orquestación completa del proceso
- Gestión de directorios de salida
- Cache inteligente
- Guardado de archivos intermedios

### `web.py`
- Servidor Flask local
- API REST para conversión
- Manejo de subida de archivos
- Servicio de descarga de MP3s

## Archivos Generados (No incluidos en Git)

```
output/
├── metadata/
│   └── stats.json
├── text/
│   ├── full_text.txt
│   └── parts/
│       ├── part_01.txt
│       └── ...
└── audio/
    ├── Book-Part01.mp3
    └── ...

uploads/
└── [PDF subido temporalmente]
```
