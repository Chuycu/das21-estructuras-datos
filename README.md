# DASS-21 — Escala de Depresión, Ansiedad y Estrés

Aplicación de escritorio desarrollada en  CustomTkinter para administrar y puntuar el cuestionario DASS-21 *(Depression, Anxiety and Stress Scale — 21 ítems)*. Proyecto académico de la asignatura **Estructuras de Datos**.

---

## Requisitos

- Python 3.10 o superior
- CustomTkinter 5.2.2

```bash
pip install -r requirements.txt
```

## Ejecución

```bash
python main.py
```

---

## Estructura del proyecto

```
dass21/
├── main.py                    # Punto de entrada
├── app.py                     # Controlador principal (DASS21App)
├── colors.py                  # Paleta de colores centralizada
├── requirements.txt
│
├── models/
│   ├── __init__.py            # Exportaciones públicas
│   ├── usuario.py             # Dataclass Usuario + estado de test
│   ├── lista_doble.py         # ★ Lista doblemente enlazada de usuarios
│   ├── cola_preguntas.py      # ★ Cola FIFO de preguntas pendientes
│   └── dass21_models.py       # Preguntas, opciones, lógica de puntuación
│
├── screens/
│   ├── user_management_screen.py   # Pantalla principal — perfil + historial
│   ├── questionnaire_screen.py     # Pantalla del cuestionario (pregunta a pregunta)
│   └── results_screen.py           # Pantalla de resultados
│
└── components/
    ├── header.py              # Encabezado reutilizable
    └── result_card.py         # Tarjeta de resultado por subescala
```

---

## Estructuras de datos implementadas

### 1. Lista doblemente enlazada — `models/lista_doble.py`

Almacena y gestiona el conjunto de usuarios registrados en la sesión.

```
cabeza ←→ Nodo(Usuario) ←→ Nodo(Usuario) ←→ Nodo(Usuario) → None
```

**Clase `Nodo`**

| Atributo    | Tipo              | Descripción                        |
|-------------|-------------------|------------------------------------|
| `usuario`   | `Usuario`         | Dato almacenado                    |
| `siguiente` | `Optional[Nodo]`  | Puntero al nodo siguiente          |
| `anterior`  | `Optional[Nodo]`  | Puntero al nodo anterior           |

**Clase `ListaDobleUsuarios`**

| Método              | Complejidad | Descripción                                      |
|---------------------|-------------|--------------------------------------------------|
| `agregar(usuario)`  | O(1)        | Inserta al final; asigna ID autoincremental      |
| `listar_todos()`    | O(n)        | Recorre desde cabeza y retorna lista Python      |
| `buscar_por_id(id)` | O(n)        | Búsqueda lineal por ID                           |
| `obtener_siguiente(id)` | O(n)    | Retorna el `usuario` del nodo siguiente          |
| `obtener_anterior(id)`  | O(n)    | Retorna el `usuario` del nodo anterior           |


**Uso en la UI:** los botones **← Anterior** y **Siguiente →** de la pantalla de gestión navegan directamente a través de los punteros `.anterior` y `.siguiente` del nodo actual, demostrando la ventaja de la lista doblemente enlazada frente a un arreglo indexado.

---

### 2. Cola FIFO de preguntas — `models/cola_preguntas.py`

Controla el orden en que se presentan las preguntas del cuestionario. Al continuar un test en progreso, las **preguntas pendientes** se encolan primero; las ya respondidas van al final.

```
frente → [idx=2, texto] → [idx=5, texto] → [idx=11, texto] → None ← final
```

**Clase `NodoCola`**

| Atributo    | Tipo                | Descripción                   |
|-------------|---------------------|-------------------------------|
| `indice`    | `int`               | Índice real en PREGUNTAS[0..20]|
| `texto`     | `str`               | Texto de la pregunta          |
| `siguiente` | `Optional[NodoCola]`| Siguiente nodo en la cola     |

**Clase `ColaPreguntas`**

| Método              | Complejidad | Descripción                                     |
|---------------------|-------------|-------------------------------------------------|
| `encolar(idx, txt)` | O(1)        | Agrega al final de la cola                      |
| `desencolar()`      | O(1)        | Extrae del frente; retorna `(indice, texto)`    |
| `esta_vacia()`      | O(1)        | Verifica si no hay preguntas pendientes         |
| `total_restante()`  | O(1)        | Retorna el tamaño actual de la cola             |

**Uso en la UI:** `QuestionnaireScreen` construye la cola ordenando primero los índices sin respuesta y luego los ya respondidos. El usuario avanza con **Siguiente →** y retrocede con **← Anterior** usando un puntero de posición (`_pos`) sobre el arreglo de índices derivado de la cola.

---

## Modelo de datos

### `Usuario` (`models/usuario.py`)

Dataclass que representa a un paciente registrado en la sesión.

| Campo               | Tipo              | Descripción                                          |
|---------------------|-------------------|------------------------------------------------------|
| `nombre`            | `str`             | Nombre completo (obligatorio)                        |
| `edad`              | `Optional[int]`   | Edad en años                                         |
| `genero`            | `Optional[str]`   | Género autodeclarado                                 |
| `fecha_registro`    | `str`             | Timestamp de creación (auto)                         |
| `id`                | `int`             | ID asignado por `ListaDobleUsuarios.agregar()`       |
| `tests_realizados`  | `List[dict]`      | Historial de tests completados                       |
| `test_en_progreso`  | `Optional[list]`  | Respuestas parciales `[-1..3]`; `None` si no hay test activo |

**Métodos de estado de test**

| Método                        | Descripción                                              |
|-------------------------------|----------------------------------------------------------|
| `iniciar_test()`              | Inicializa `test_en_progreso` con 21 valores `-1`        |
| `guardar_progreso(respuestas)`| Actualiza `test_en_progreso` con el estado actual        |
| `finalizar_test()`            | Limpia `test_en_progreso` (→ `None`)                     |
| `tiene_test_en_progreso()`    | `True` si hay un test activo                             |
| `progreso_test()`             | Cuenta cuántas preguntas tienen respuesta (`≥ 0`)        |
| `agregar_test(resp, res, tot)`| Guarda test completado en `tests_realizados`             |

### `Resultado` (`models/dass21_models.py`)

Dataclass de solo lectura producida por `calcular_resultados()`.

| Campo         | Tipo  | Ejemplo                          |
|---------------|-------|----------------------------------|
| `nombre`      | `str` | `"Depresión"` / `"Ansiedad"` / `"Estrés"` |
| `puntaje`     | `int` | `0 – 21`                         |
| `nivel`       | `str` | `"Normal"` / `"Leve"` / `"Moderada"` / `"Severa"` / `"Extremadamente severa"` |
| `descripcion` | `str` | Texto clínico orientativo        |
| `maximo`      | `int` | `21` (para cálculo de barra)     |

---

## Lógica de puntuación DASS-21

`calcular_resultados(respuestas: list[int]) → list[Resultado]`

Cada ítem se puntúa 0–3. Los 21 ítems se asignan a tres subescalas:

| Subescala  | Ítems (1-indexados)          | Rango normal |
|------------|------------------------------|--------------|
| Depresión  | 3, 5, 10, 13, 16, 17, 21    | < 5          |
| Ansiedad   | 2, 4, 7, 9, 15, 19, 20      | < 4          |
| Estrés     | 1, 6, 8, 11, 12, 14, 18     | < 8          |

Los umbrales de severidad son los establecidos por Lovibond & Lovibond (1995).

---

## Flujo de la aplicación

```
Inicio
  └─► UserManagementScreen
        ├─► [+ Nuevo Usuario]  → solicita nombre / edad / género via diálogo
        ├─► [← Anterior / Siguiente →]  → navega con lista doble enlazada
        ├─► [+ Iniciar nuevo test]  → iniciar_test() → QuestionnaireScreen
        ├─► [Continuar test →]  → continue_test() → QuestionnaireScreen (con respuestas previas)
        ├─► [Ver resultado completo]  → view_last_result() → ResultsScreen
        └─► [Descartar]  → finalizar_test() → refresca pantalla

QuestionnaireScreen
  ├── Cola FIFO prioriza preguntas sin responder
  ├── Cada selección → on_save_progress() → usuario.guardar_progreso()
  ├── [Salir]  → guarda progreso → UserManagementScreen
  └── [Ver resultados →]  → on_calculate() → app.show_results()

ResultsScreen
  ├── Muestra puntaje total + 3 ResultCard (dep / anx / str)
  ├── Barra de progreso visual por subescala
  └── [← Volver al inicio]  → UserManagementScreen
```

---

## Arquitectura de la UI (CustomTkinter)

**Paleta de colores** (`colors.py`): todas las pantallas y componentes consumen `COLORES` (dict) y `NIVEL_COLORES` (dict por subescala). Cambiar un valor ahí afecta toda la aplicación.

**Patrón de pantallas**: cada pantalla es un `ctk.CTkFrame` independiente. `DASS21App` (en `app.py`) destruye la pantalla activa (`current_screen.destroy()`) y crea la siguiente, actuando como un router de pantalla única.

**Componentes reutilizables**

| Componente     | Descripción                                                    |
|----------------|----------------------------------------------------------------|
| `Header`       | Barra superior con título y subtítulo. Acepta `title` y `subtitle` por parámetro. |
| `ResultCard`   | Tarjeta de resultado para una subescala: nombre, puntaje, nivel, descripción y barra de progreso. |

---

## Persistencia

Los datos son **en memoria únicamente**. Al cerrar la aplicación, usuarios y tests se pierden. No hay base de datos ni archivos de guardado.

---

## Notas clínicas

> Esta herramienta es de uso orientativo y **no constituye un diagnóstico clínico**. Si el usuario experimenta dificultades significativas, debe ser referido a un profesional de salud mental.
