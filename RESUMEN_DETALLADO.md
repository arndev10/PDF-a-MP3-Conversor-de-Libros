# 📋 RESUMEN DETALLADO DEL PROYECTO - PDF A MP3

## 🎯 OBJETIVO DEL PROYECTO

Aplicación offline-first que convierte un libro PDF (no-ficción) en múltiples archivos MP3 de aproximadamente 40 minutos cada uno, utilizando tecnologías locales sin dependencias de internet ni APIs pagas.

---

## 📦 DEPENDENCIAS Y LIBRERÍAS UTILIZADAS

### 1. **PyPDF2 (>=3.0.0)**
- **Propósito**: Extracción de texto desde archivos PDF
- **Uso específico**: 
  - Lectura de archivos PDF binarios
  - Extracción de texto página por página
  - Conteo de páginas totales
- **Métodos utilizados**:
  - `PdfReader()`: Para leer el archivo PDF
  - `reader.pages`: Lista de páginas del documento
  - `page.extract_text()`: Extracción de texto plano de cada página

### 2. **pyttsx3 (>=2.90)**
- **Propósito**: Text-to-Speech (TTS) offline
- **Características**:
  - Funciona completamente offline
  - Utiliza el motor de voz del sistema operativo (SAPI5 en Windows)
  - No requiere conexión a internet
- **Configuración utilizada**:
  - `rate=150`: Velocidad de lectura (palabras por minuto)
  - `volume=1.0`: Volumen máximo
  - `save_to_file()`: Guarda directamente a archivo WAV
- **Limitaciones**: Calidad de voz depende del sistema operativo

### 3. **pydub (>=0.25.1)**
- **Propósito**: Manipulación y conversión de audio
- **Uso específico**:
  - Conversión de WAV a MP3
  - Conversión a mono (1 canal)
  - Compresión con bitrate bajo (64k)
- **Dependencia externa**: Requiere `ffmpeg` instalado en el sistema para la conversión a MP3
- **Métodos utilizados**:
  - `AudioSegment.from_wav()`: Carga archivo WAV
  - `set_channels(1)`: Convierte a mono
  - `export()`: Exporta a MP3 con bitrate específico

### 4. **Flask (>=3.0.0)**
- **Propósito**: Framework web para interfaz de prueba local
- **Componentes utilizados**:
  - `Flask`: Aplicación principal
  - `render_template`: Renderizado de HTML
  - `request`: Manejo de peticiones HTTP
  - `jsonify`: Respuestas JSON
  - `send_file` / `send_from_directory`: Descarga de archivos
- **Configuración**:
  - `MAX_CONTENT_LENGTH = 50MB`: Límite de tamaño de archivo
  - `UPLOAD_FOLDER`: Directorio para archivos subidos
  - `host='127.0.0.1'`: Solo accesible localmente
  - `port=5000`: Puerto por defecto
  - `debug=True`: Modo desarrollo

### 5. **Librerías Estándar de Python**
- **pathlib.Path**: Manejo de rutas multiplataforma
- **sys**: Manejo de argumentos CLI y salida de errores
- **json**: Serialización de estadísticas
- **typing**: Type hints (Dict, List)
- **os**: Operaciones del sistema (implícito en Flask)

---

## 📁 ESTRUCTURA DEL PROYECTO

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
├── README.md           # Documentación básica
├── templates/
│   └── index.html      # Interfaz web HTML/CSS/JS
└── output/             # Directorio de salida (generado)
    ├── metadata/
    │   └── stats.json
    ├── text/
    │   ├── full_text.txt
    │   └── parts/
    └── audio/
```

---

## 🔧 MÓDULOS Y FUNCIONALIDAD DETALLADA

### 1. **main.py** - Punto de Entrada CLI

**Responsabilidades**:
- Validación de argumentos de línea de comandos
- Validación del directorio de entrada
- Verificación de existencia de exactamente un PDF
- Inicialización del pipeline

**Funciones**:
- `validate_input_directory(input_dir: Path) -> Path`:
  - Verifica que el directorio existe
  - Verifica que es un directorio válido
  - Busca archivos `.pdf` con `glob("*.pdf")`
  - Valida que haya exactamente 1 PDF
  - Retorna el Path del PDF encontrado
  - Sale con código de error si falla la validación

- `main()`:
  - Valida argumentos (`sys.argv`)
  - Resuelve ruta absoluta con `.resolve()`
  - Llama a validación
  - Importa y ejecuta `run_pipeline()`

**Manejo de Errores**:
- Mensajes claros a `sys.stderr`
- Códigos de salida apropiados
- Listado de PDFs encontrados si hay múltiples

---

### 2. **extractor.py** - Extracción de Texto

**Responsabilidades**:
- Lectura de archivos PDF
- Extracción de texto preservando orden
- Cálculo de estadísticas básicas

**Funciones**:
- `extract_text(pdf_path: Path) -> Dict[str, any]`:
  - Abre PDF en modo binario (`'rb'`)
  - Crea `PdfReader` para leer el documento
  - Itera sobre todas las páginas
  - Extrae texto de cada página con `extract_text()`
  - Une textos con `'\n'` como separador
  - Cuenta palabras con `split()`
  - Retorna diccionario con:
    - `'text'`: Texto completo
    - `'pages'`: Número de páginas
    - `'words'`: Número de palabras

**Características**:
- Preserva orden de lectura
- Ignora imágenes, tablas complejas, footnotes
- Extracción simple y directa

---

### 3. **splitter.py** - División de Texto

**Responsabilidades**:
- Dividir texto en partes de ~40 minutos
- Aplicar lógica de fusión para partes pequeñas
- Mantener orden del texto

**Constantes**:
- `WORDS_PER_MINUTE = 150`: Velocidad de lectura promedio
- `TARGET_MINUTES = 40`: Duración objetivo por parte
- `WORDS_PER_PART = 6000`: Palabras por parte (150 × 40)
- `MIN_PART_WORDS = 3000`: Mínimo para parte independiente (~20 min)

**Funciones**:
- `split_text(text: str) -> List[str]`:
  - Divide texto en palabras individuales
  - Acumula palabras hasta alcanzar `WORDS_PER_PART`
  - Crea nueva parte cuando se alcanza el límite
  - Al finalizar:
    - Si última parte < `MIN_PART_WORDS` y hay partes previas:
      → Fusiona con la parte anterior
    - Si no hay partes previas o es >= `MIN_PART_WORDS`:
      → Crea nueva parte
  - Retorna lista de strings (partes de texto)

**Lógica de Fusión**:
- Evita partes muy cortas (< 20 minutos)
- Mejora experiencia de usuario
- Mantiene partes aproximadamente uniformes

---

### 4. **tts.py** - Text-to-Speech

**Responsabilidades**:
- Generación de audio WAV desde texto
- Configuración del motor TTS
- Guardado de archivos de audio

**Funciones**:
- `generate_wav(text: str, output_path: Path) -> None`:
  - Inicializa motor TTS con `pyttsx3.init()`
  - Configura propiedades:
    - `rate=150`: Velocidad de habla
    - `volume=1.0`: Volumen máximo
  - Crea directorio padre si no existe (`mkdir(parents=True, exist_ok=True)`)
  - Guarda directamente a WAV con `save_to_file()`
  - Ejecuta síntesis con `runAndWait()`

**Características**:
- Completamente offline
- Usa voz del sistema (SAPI5 en Windows)
- Genera archivos WAV sin comprimir
- Síncrono (bloquea hasta completar)

**Limitaciones**:
- Calidad de voz depende del sistema
- Puede ser lento para textos largos
- No permite personalización de voz en MVP

---

### 5. **encoder.py** - Codificación MP3

**Responsabilidades**:
- Conversión de WAV a MP3
- Optimización de tamaño (mono, bajo bitrate)
- Limpieza de archivos temporales

**Funciones**:
- `encode_mp3(wav_path: Path, mp3_path: Path) -> None`:
  - Carga archivo WAV con `AudioSegment.from_wav()`
  - Convierte a mono con `set_channels(1)`
  - Crea directorio padre si no existe
  - Exporta a MP3 con:
    - `format='mp3'`
    - `bitrate='64k'`: Bajo bitrate para archivos pequeños

**Características**:
- Requiere `ffmpeg` instalado
- Reduce tamaño significativamente
- Mono para reducir tamaño (no estéreo necesario para voz)
- Bitrate bajo (64k) suficiente para voz clara

**Dependencia Externa**:
- `ffmpeg`: Herramienta de línea de comandos para conversión
- Debe estar en PATH del sistema

---

### 6. **pipeline.py** - Orquestación

**Responsabilidades**:
- Coordinar todos los módulos
- Gestionar estructura de directorios
- Guardar archivos intermedios
- Evitar reprocesamiento innecesario

**Estructura de Directorios**:
```python
OUTPUT_DIR = 'output'
├── metadata/        # Estadísticas JSON
├── text/
│   ├── full_text.txt
│   └── parts/       # Partes individuales
└── audio/           # Archivos MP3 finales
```

**Funciones**:
- `run_pipeline(pdf_path: Path) -> Dict[str, any]`:
  
  **Paso 1: Extracción**
  - Llama a `extract_text()`
  - Obtiene texto completo, páginas y palabras
  - Muestra progreso en consola
  
  **Paso 2: División**
  - Llama a `split_text()`
  - Obtiene lista de partes
  - Calcula número de partes
  
  **Paso 3: Preparación de Directorios**
  - Crea todos los directorios necesarios
  - Usa `mkdir(exist_ok=True)` para evitar errores
  
  **Paso 4: Guardado de Texto**
  - Guarda texto completo en `full_text.txt`
  - Solo si no existe (cache)
  - Encoding UTF-8
  
  **Paso 5: Estadísticas**
  - Calcula minutos estimados: `word_count / 150`
  - Crea diccionario de stats:
    - `pages`: Número de páginas
    - `words`: Total de palabras
    - `estimated_minutes`: Duración estimada
    - `parts`: Número de partes
  - Guarda en `stats.json` con formato JSON indentado
  
  **Paso 6: Generación de Audio**
  - Itera sobre cada parte
  - Para cada parte:
    - Genera nombre: `part_01.txt`, `part_02.txt`, etc.
    - Guarda texto de la parte (si no existe)
    - Genera nombres de audio:
      - WAV temporal: `temp_part_01.wav`
      - MP3 final: `{book_name}-Part01.mp3`
    - Si MP3 no existe:
      - Genera WAV con `generate_wav()`
      - Convierte a MP3 con `encode_mp3()`
      - Elimina WAV temporal con `unlink()`
      - Muestra progreso
    - Si MP3 existe:
      - Salta generación (cache)
  
  **Paso 7: Retorno**
  - Retorna diccionario con:
    - `success`: True
    - `output_dir`: Ruta del directorio de salida
    - `stats`: Estadísticas
    - `parts`: Número de partes

**Características**:
- Cache inteligente: No reprocesa si archivos existen
- Progreso visible en consola
- Manejo de errores implícito (excepciones se propagan)
- Estructura organizada de salida

---

### 7. **web.py** - Interfaz Web Flask

**Responsabilidades**:
- Servir interfaz HTML
- Manejar subida de archivos
- Ejecutar pipeline desde web
- Servir archivos generados
- Proporcionar API REST

**Configuración**:
```python
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 50 * 1024 * 1024  # 50MB
app.config['UPLOAD_FOLDER'] = Path('uploads')
```

**Rutas**:

1. **`GET /`**:
   - Renderiza `index.html`
   - Página principal de la aplicación

2. **`POST /api/upload`**:
   - Recibe archivo PDF en `request.files['pdf']`
   - Valida que sea PDF (extensión `.pdf`)
   - Limpia PDFs anteriores del directorio uploads
   - Guarda nuevo PDF
   - Retorna JSON con éxito y nombre de archivo

3. **`POST /api/convert`**:
   - Busca PDF en directorio uploads
   - Valida que haya exactamente uno
   - Ejecuta `run_pipeline()`
   - Retorna resultado JSON o error

4. **`GET /api/files`**:
   - Lista archivos MP3 en `output/audio/`
   - Retorna JSON con nombre y tamaño de cada archivo

5. **`GET /api/download/<filename>`**:
   - Descarga archivo MP3 específico
   - Usa `send_from_directory()` con `as_attachment=True`

6. **`GET /api/stats`**:
   - Lee `stats.json` del directorio metadata
   - Retorna estadísticas en JSON
   - Error 404 si no existe

**Características**:
- API RESTful
- Manejo de errores con códigos HTTP apropiados
- Límite de tamaño de archivo
- Solo accesible localmente (127.0.0.1)

---

### 8. **templates/index.html** - Interfaz Web

**Tecnologías**:
- HTML5
- CSS3 (inline, sin frameworks)
- JavaScript vanilla (sin librerías)

**Estructura**:

**HTML**:
- Estructura semántica
- Formulario de subida con drag & drop
- Área de progreso
- Sección de estadísticas
- Lista de archivos generados

**CSS**:
- Diseño moderno con gradientes
- Responsive design
- Animaciones suaves (`transition`)
- Estados hover y drag-over
- Paleta de colores: púrpura/azul (#667eea, #764ba2)
- Tipografía del sistema

**JavaScript**:
- **Event Listeners**:
  - Click en área de subida → abre selector de archivos
  - Drag & drop de archivos
  - Click en botón de conversión
  
- **Funciones**:
  - `handleFile(file)`: Valida y muestra archivo seleccionado
  - `convertBtn.addEventListener()`: Proceso completo:
    1. Sube PDF con `fetch('/api/upload')`
    2. Actualiza barra de progreso
    3. Llama a `/api/convert`
    4. Muestra progreso
    5. Carga estadísticas y archivos al completar
  - `loadStats()`: Carga estadísticas desde API
  - `loadFiles()`: Lista archivos MP3 disponibles
  - `showStatus(message, type)`: Muestra mensajes de estado

**Características UX**:
- Feedback visual inmediato
- Barra de progreso animada
- Mensajes de estado claros (éxito/error/info)
- Descarga directa de archivos
- Diseño intuitivo y moderno

---

## 🔄 FLUJO DE EJECUCIÓN COMPLETO

### Modo CLI:

```
Usuario ejecuta: python main.py input/
    ↓
main.py valida directorio y PDF
    ↓
main.py llama a pipeline.run_pipeline()
    ↓
pipeline.py:
    1. extractor.extract_text() → texto, páginas, palabras
    2. splitter.split_text() → lista de partes
    3. Crea directorios de salida
    4. Guarda texto completo y partes
    5. Calcula y guarda estadísticas
    6. Para cada parte:
       a. tts.generate_wav() → archivo WAV temporal
       b. encoder.encode_mp3() → archivo MP3 final
       c. Elimina WAV temporal
    ↓
Retorna resultado con estadísticas
```

### Modo Web:

```
Usuario abre http://127.0.0.1:5000
    ↓
Flask sirve index.html
    ↓
Usuario sube PDF → POST /api/upload
    ↓
Usuario hace clic en "Convertir" → POST /api/convert
    ↓
web.py ejecuta pipeline.run_pipeline()
    ↓
Mismo flujo que CLI
    ↓
JavaScript actualiza UI con resultados
    ↓
Usuario descarga MP3s → GET /api/download/<filename>
```

---

## 📊 PARÁMETROS Y CONFIGURACIÓN

### Parámetros de División:
- **Velocidad de lectura**: 150 palabras/minuto
- **Duración objetivo**: 40 minutos por parte
- **Palabras por parte**: 6,000 palabras
- **Mínimo para parte independiente**: 3,000 palabras (~20 min)

### Parámetros de Audio:
- **Velocidad TTS**: 150 palabras/minuto
- **Volumen**: 1.0 (máximo)
- **Canales**: Mono (1 canal)
- **Bitrate MP3**: 64 kbps
- **Formato intermedio**: WAV (sin comprimir)
- **Formato final**: MP3

### Límites:
- **Tamaño máximo de archivo web**: 50 MB
- **Puerto web**: 5000
- **Host web**: 127.0.0.1 (solo local)

---

## 🛠️ HERRAMIENTAS Y TECNOLOGÍAS ADICIONALES

### Requerimientos del Sistema:
- **Python**: 3.11+ (probado con 3.13.1)
- **ffmpeg**: Para conversión WAV → MP3
  - Windows: Instalar desde https://ffmpeg.org
  - O con Chocolatey: `choco install ffmpeg`
- **Motor TTS del Sistema**:
  - Windows: SAPI5 (incluido)
  - Linux: espeak o festival
  - macOS: NSSpeechSynthesizer

### Gestión de Dependencias:
- **pip**: Instalador de paquetes Python
- **requirements.txt**: Lista de dependencias con versiones mínimas

### Control de Versiones:
- **.gitignore**: Excluye:
  - `__pycache__/`: Bytecode de Python
  - `*.pyc`, `*.pyo`: Archivos compilados
  - `env/`, `venv/`: Entornos virtuales
  - `output/`: Archivos generados
  - `*.mp3`, `*.wav`, `*.txt`: Archivos de salida

---

## 📈 CARACTERÍSTICAS DE DISEÑO

### Principios Aplicados:
1. **Offline-first**: Todo funciona sin internet
2. **Determinístico**: Mismos inputs → mismos outputs
3. **Cache inteligente**: No reprocesa archivos existentes
4. **Modularidad**: Un módulo = una responsabilidad
5. **Readability**: Código claro > código clever
6. **Type hints**: Mejora legibilidad y mantenibilidad
7. **Pathlib**: Rutas multiplataforma
8. **Manejo de errores**: Mensajes claros y útiles

### Decisiones de Arquitectura:
- **Síncrono**: No async (no necesario para MVP)
- **Monolítico**: Todo en un proceso (no microservicios)
- **Sin base de datos**: Archivos en sistema de archivos
- **Sin ML**: Solo TTS básico del sistema
- **Sin cloud**: Todo local

---

## 🎨 INTERFAZ WEB - DETALLES TÉCNICOS

### CSS Utilizado:
- **Flexbox**: Para layout de archivos
- **CSS Grid**: Implícito en algunos contenedores
- **Gradientes**: `linear-gradient(135deg, #667eea 0%, #764ba2 100%)`
- **Sombras**: `box-shadow: 0 10px 40px rgba(0,0,0,0.2)`
- **Transiciones**: `transition: all 0.3s`
- **Border-radius**: 6px, 8px, 12px para elementos redondeados

### JavaScript - APIs Utilizadas:
- **Fetch API**: Para peticiones HTTP
- **File API**: Para manejo de archivos
- **Drag & Drop API**: Para arrastrar archivos
- **DOM API**: Manipulación del DOM

### Eventos Manejados:
- `click`: Botones y áreas clickeables
- `dragover`: Archivo arrastrado sobre área
- `dragleave`: Archivo sale del área
- `drop`: Archivo soltado
- `change`: Selector de archivos

---

## 📝 FORMATOS DE ARCHIVO

### Entrada:
- **PDF**: Formato estándar de Adobe
- **Extensiones aceptadas**: `.pdf`

### Salida:
- **TXT**: Texto plano UTF-8
  - `full_text.txt`: Texto completo
  - `part_XX.txt`: Partes individuales
- **JSON**: Estadísticas en formato JSON
  - `stats.json`: Metadatos del libro
- **WAV**: Audio sin comprimir (temporal)
  - `temp_part_XX.wav`: Archivos intermedios
- **MP3**: Audio comprimido (final)
  - `{book_name}-PartXX.mp3`: Archivos finales

---

## 🔍 CASOS DE USO Y FLUJOS

### Caso 1: Conversión Exitosa
1. Usuario proporciona PDF válido
2. Sistema extrae texto
3. Divide en partes apropiadas
4. Genera audio para cada parte
5. Convierte a MP3
6. Usuario obtiene múltiples MP3s de ~40 min

### Caso 2: PDF Ya Procesado
1. Sistema detecta archivos MP3 existentes
2. Salta generación de audio
3. Muestra mensaje "already exists"
4. Usuario puede regenerar eliminando archivos

### Caso 3: Parte Final Pequeña
1. Sistema detecta última parte < 3000 palabras
2. Fusiona con parte anterior
3. Evita archivo muy corto
4. Mejora experiencia de usuario

### Caso 4: Error de Validación
1. Usuario proporciona directorio sin PDF
2. Sistema muestra error claro
3. Sale con código de error
4. No procesa nada

---

## 🚀 OPTIMIZACIONES Y MEJORAS FUTURAS

### Implementadas:
- ✅ Cache de archivos generados
- ✅ Estructura de directorios organizada
- ✅ Progreso visible en consola
- ✅ Validación robusta de entrada

### Posibles Mejoras (No en MVP):
- Detección automática de capítulos
- Personalización de voz TTS
- Ajuste de velocidad de lectura
- Compresión más agresiva
- Procesamiento asíncrono
- Interfaz de usuario más avanzada
- Soporte para múltiples idiomas
- Mejora de calidad de extracción de PDF

---

## 📚 CONOCIMIENTOS TÉCNICOS APLICADOS

### Python:
- Type hints y anotaciones
- Pathlib para rutas
- Context managers (`with`)
- List comprehensions
- F-strings para formateo
- Módulos y paquetes

### Procesamiento de Archivos:
- Lectura binaria de PDFs
- Escritura de texto UTF-8
- Manejo de rutas multiplataforma
- Gestión de directorios

### Audio:
- Formatos WAV y MP3
- Conversión de formatos
- Optimización de tamaño
- Compresión de audio

### Web:
- Framework Flask
- API REST
- HTML5/CSS3/JavaScript
- Drag & Drop
- Fetch API
- JSON

---

## ✅ RESUMEN EJECUTIVO

**Total de Módulos**: 7 archivos Python principales
**Total de Dependencias**: 4 librerías externas
**Líneas de Código Aproximadas**: ~600 líneas (Python) + ~360 líneas (HTML/CSS/JS)
**Tecnologías**: Python 3.11+, Flask, PyPDF2, pyttsx3, pydub
**Arquitectura**: Modular, offline-first, determinística
**Interfaz**: CLI + Web (local)
**Formato Salida**: MP3 mono, 64kbps, ~40 min por archivo

Este proyecto demuestra una implementación completa de un pipeline de procesamiento de documentos con generación de audio, siguiendo principios de código limpio, modularidad y usabilidad.
