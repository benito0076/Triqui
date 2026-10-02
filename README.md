# ❌⭕ Triqui Arcade

> El juego de tres en línea de toda la vida, reinventado: rivales con IA, modos locos y un tablero que no se deja ganar fácil.

Proyecto del curso de IA para desarrollar un juego de Triqui completo, divertido y con personalidad.

## La idea

Todos sabemos jugar Triqui, y todos sabemos que, bien jugado, siempre termina en empate. **Triqui Arcade** parte de ahí: si el juego clásico está resuelto, hay que hacerlo interesante con rivales memorables, variantes del tablero y una IA que aprende de ti.

## Funcionalidades planeadas

### Modos de juego
- **Clásico**: tablero 3x3, X contra O.
- **Gran Triqui**: tablero 5x5 o 7x7 donde se necesitan 4 o 5 en línea.
- **Triqui Supremo**: nueve tableros pequeños dentro de uno grande. Donde juegas determina dónde juega tu rival.
- **Fichas fugaces**: solo puedes tener 3 fichas en el tablero; al poner la cuarta, desaparece la más antigua. Aquí ya no hay empates.
- **Contrarreloj**: 5 segundos por jugada, o pierdes el turno.

### Rivales con IA
| Rival | Personalidad |
|---|---|
| 🐣 **Pollito** | Juega al azar. Ideal para calentar. |
| 🦊 **Zorro** | Bloquea y ataca, pero cae en trampas básicas. |
| 🧠 **Minimax** | Perfecto e imbatible. Lo mejor que puedes lograr es empatar. |
| 🎭 **El Camaleón** | Estudia tu estilo durante la partida y adapta su estrategia. |

Cada rival comenta las jugadas con frases propias.

### Extras
- Modo dos jugadores en el mismo equipo.
- Marcador de victorias, derrotas y empates por rival.
- Repetición de la última partida, jugada por jugada.
- Modo "pista": la IA sugiere la mejor jugada y explica por qué.
- Temas visuales: clásico de papel, neón retro y pizarra de colegio.
- Efectos de sonido y una animación al ganar.

## Hoja de ruta

- [x] Inicializar el repositorio
- [x] Lógica del tablero y detección de ganador/empate
- [x] Interfaz jugable en modo clásico (consola)
- [x] Interfaz gráfica con tkinter, marcador y línea ganadora
- [x] IA nivel Pollito y Zorro
- [x] IA Minimax (con caché; la poda alfa-beta llegará con los tableros grandes)
- [x] Modo Gran Triqui (5x5 con 4 en línea y 7x7 con 5 en línea)
- [ ] Modo Fichas fugaces
- [ ] Triqui Supremo
- [ ] El Camaleón y las frases de los rivales
- [ ] Marcador, repetición y temas visuales
- [ ] Pulido final y publicación

## Estructura prevista

```
3. Triqui/
├── src/        # lógica del juego e IA
├── assets/     # sonidos, imágenes y temas
├── tests/      # pruebas de las reglas y de la IA
└── README.md
```

## Cómo ejecutarlo

Requiere Python 3.10 o superior y no tiene dependencias. Desde esta carpeta:

```bash
# Ventana gráfica (elige rival, símbolo y modo 2 jugadores dentro de la ventana)
PYTHONPATH=src python -m triqui

# Versión de consola contra la IA (pollito, zorro o minimax)
PYTHONPATH=src python -m triqui --consola --rival zorro

# Consola con tablero grande (clasico, gran5 o gran7)
PYTHONPATH=src python -m triqui --consola --modo gran5 --rival minimax

# Consola, dos personas en el mismo equipo
PYTHONPATH=src python -m triqui --consola --dos-jugadores

# Pruebas
PYTHONPATH=src python -m unittest discover -s tests
```

En PowerShell, define la variable antes: `$env:PYTHONPATH = "src"`.

## Objetivos de aprendizaje

- Modelar un juego como estado, reglas y turnos.
- Implementar búsqueda adversarial (Minimax y poda alfa-beta).
- Diseñar IAs con distintos niveles de dificultad.
- Probar las reglas del juego con pruebas automáticas.
- Trabajar con Git de forma ordenada, con commits pequeños y claros.

## Licencia

Por definir.
