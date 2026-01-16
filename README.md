# 📚 PDF a MP3 - Conversor de Libros

Aplicación offline-first que convierte libros PDF en múltiples archivos de audio MP3, cada uno de aproximadamente 40 minutos de duración. Desarrollada completamente en Python con procesamiento local, sin dependencias de internet ni APIs pagas.

## 🚀 Características

- ✅ **Extracción de texto** desde archivos PDF
- ✅ **División inteligente** en partes de ~40 minutos
- ✅ **Generación de audio offline** usando TTS del sistema
- ✅ **Conversión a MP3** optimizada (mono, 64kbps)
- ✅ **Interfaz web local** para pruebas y uso interactivo
- ✅ **Modo CLI** para automatización
- ✅ **Cache inteligente** para evitar reprocesamiento

## 🛠️ Tecnologías Utilizadas

### Backend

- **Python 3.11+**: Lenguaje principal del proyecto
- **PyPDF2**: Extracción de texto desde archivos PDF
- **pyttsx3**: Motor de Text-to-Speech offline que utiliza las voces del sistema operativo
- **pydub**: Manipulación y conversión de audio (WAV → MP3)
- **Flask**: Framework web ligero para la interfaz de prueba local

### Frontend

- **HTML5**: Estructura semántica de la interfaz web
- **CSS3**: Diseño moderno con gradientes y animaciones
- **JavaScript (Vanilla)**: Interactividad sin dependencias externas
  - Fetch API para comunicación con el backend
  - Drag & Drop API para subida de archivos
  - DOM API para manipulación de elementos

### Herramientas del Sistema

- **ffmpeg**: Conversión de audio (requerido para MP3)
- **Motor TTS del Sistema**: 
  - Windows: SAPI5 (incluido)
  - Linux: espeak/festival
  - macOS: NSSpeechSynthesizer

### Librerías Estándar de Python

- **pathlib**: Manejo de rutas multiplataforma
- **sys**: Manejo de argumentos CLI
- **json**: Serialización de datos
- **typing**: Type hints para mejor legibilidad

## 📦 Instalación

### Requisitos Previos

1. **Python 3.11 o superior**
   ```bash
   python --version
   ```

2. **ffmpeg** (para conversión a MP3)
   - **Windows**: 
     - Descarga desde [ffmpeg.org](https://ffmpeg.org/download.html)
     - O con Chocolatey: `choco install ffmpeg`
   - **Linux**: `sudo apt install ffmpeg`
   - **macOS**: `brew install ffmpeg`

### Instalación de Dependencias

```bash
pip install -r requirements.txt
```

Esto instalará:
- PyPDF2>=3.0.0
- pyttsx3>=2.90
- pydub>=0.25.1
- flask>=3.0.0

## 💻 Uso

### Modo CLI

```bash
python main.py input/
```

El directorio `input/` debe contener **exactamente un archivo PDF**.

**Ejemplo:**
```bash
mkdir input
# Copia tu PDF al directorio input/
python main.py input/
```

### Modo Web (Interfaz Local)

Para usar la interfaz web:

```bash
python web.py
```

Luego abre tu navegador en: **http://127.0.0.1:5000**

La interfaz permite:
- Subir PDFs mediante drag & drop o selección
- Ver progreso de conversión en tiempo real
- Descargar archivos MP3 generados
- Ver estadísticas del libro procesado

## 📁 Estructura del Proyecto

```
PDF A MP3/
├── main.py              # Punto de entrada CLI
├── extractor.py         # Extracción de texto PDF
├── splitter.py          # División de texto en partes
├── tts.py               # Generación de audio WAV
├── encoder.py           # Conversión WAV a MP3
├── pipeline.py          # Orquestación completa
├── web.py               # Interfaz web Flask
├── requirements.txt     # Dependencias
├── .gitignore          # Archivos ignorados
├── README.md           # Este archivo
├── RESUMEN_DETALLADO.md # Documentación técnica completa
├── templates/
│   └── index.html      # Interfaz web HTML/CSS/JS
└── output/             # Directorio de salida (generado)
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
```

## 📊 Estructura de Salida

Después de procesar un PDF, se genera la siguiente estructura:

```
output/
├── metadata/
│   └── stats.json          # Estadísticas: páginas, palabras, duración estimada
├── text/
│   ├── full_text.txt       # Texto completo extraído
│   └── parts/
│       ├── part_01.txt     # Parte 1 del texto
│       ├── part_02.txt     # Parte 2 del texto
│       └── ...              # Más partes según el tamaño
└── audio/
    ├── Book-Part01.mp3     # Audio parte 1 (~40 min)
    ├── Book-Part02.mp3     # Audio parte 2 (~40 min)
    └── ...                  # Más archivos MP3
```

## ⚙️ Configuración y Parámetros

### Parámetros de División

- **Velocidad de lectura**: 150 palabras/minuto
- **Duración objetivo**: 40 minutos por parte
- **Palabras por parte**: 6,000 palabras
- **Mínimo para parte independiente**: 3,000 palabras (~20 min)

Si la última parte es menor a 3,000 palabras, se fusiona automáticamente con la parte anterior para evitar archivos muy cortos.

### Parámetros de Audio

- **Velocidad TTS**: 150 palabras/minuto
- **Volumen**: 1.0 (máximo)
- **Canales**: Mono (1 canal) para reducir tamaño
- **Bitrate MP3**: 64 kbps (suficiente para voz clara)
- **Formato intermedio**: WAV (sin comprimir)
- **Formato final**: MP3

## 🔄 Flujo de Procesamiento

1. **Validación**: Verifica que el directorio contenga exactamente un PDF
2. **Extracción**: Lee el PDF y extrae todo el texto
3. **Análisis**: Cuenta páginas y palabras, calcula duración estimada
4. **División**: Divide el texto en partes de ~6,000 palabras cada una
5. **Generación de Audio**: Para cada parte:
   - Genera archivo WAV usando TTS offline
   - Convierte WAV a MP3 con ffmpeg
   - Elimina archivo WAV temporal
6. **Guardado**: Almacena texto completo, partes y archivos MP3

## 🎯 Casos de Uso

- Convertir libros de no-ficción a formato de audio
- Crear audiolibros personalizados
- Procesar documentos largos para escuchar mientras realizas otras actividades
- Accesibilidad: convertir texto a audio para personas con dificultades de lectura

## 📝 Notas Importantes

- **Offline-first**: Todo el procesamiento se realiza localmente, sin conexión a internet
- **Cache inteligente**: Si un archivo MP3 ya existe, se omite su regeneración
- **Calidad de voz**: Depende del motor TTS de tu sistema operativo
- **Tiempo de procesamiento**: Varía según el tamaño del PDF (puede tardar varios minutos)
- **Límite de tamaño web**: 50 MB por archivo PDF

## 🐛 Solución de Problemas

### Error: "No module named 'flask'"
```bash
pip install -r requirements.txt
```

### Error: "ffmpeg not found"
Instala ffmpeg siguiendo las instrucciones en la sección de Instalación.

### Error: "Multiple PDF files found"
El directorio de entrada debe contener exactamente un archivo PDF.

### La voz suena robótica
Esto es normal con TTS del sistema. La calidad depende de las voces instaladas en tu sistema operativo.

## 📄 Licencia

Este proyecto es de código abierto y está disponible para uso personal y educativo.

## 🤝 Contribuciones

Las contribuciones son bienvenidas. Por favor:
1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📚 Documentación Adicional

Para más detalles técnicos, consulta [RESUMEN_DETALLADO.md](RESUMEN_DETALLADO.md)

## 👤 Autor

**arndev10**

- GitHub: [@arndev10](https://github.com/arndev10)

---

⭐ Si este proyecto te resulta útil, considera darle una estrella en GitHub!
