#  Manual Técnico

## Proyecto: Buscaminas

---

##  Tecnologías Utilizadas

* GitHub (control de versiones)
* IDE Arduino
* Proteus
* Flask (Backend en Python)
* Comunicación Serial vía Bluetooth

---

##  Código Fuente

### Backend en Python (Flask)

```python
from flask import Flask, jsonify, render_template, request
import re, serial

app = Flask(__name__)
arduino_device = serial.Serial('COM7', 115200)

@app.route('/')
def homepage():
    return render_template('home.html')

@app.route('/bomb_status')
def bomb_status():
    arduino_device.write(b'B')
    response = arduino_device.readline().decode().strip()
    bomb_matrix_state = list(map(int, response.split(',')))
    return jsonify(matrix_state=bomb_matrix_state)

@app.route('/activate_bombs', methods=['POST'])
def activate_bombs():
    bomb_locs = request.form.get('bomb_positions')
    if bomb_locs:
        bomb_locs = bomb_locs.rstrip(',').split(',')
        for location in bomb_locs:
            if location.isdigit():
                bomb_position = int(location)
                if 1 <= bomb_position <= 16:
                    position_string = f'b{bomb_position}\n'
                    arduino_device.write(position_string.encode())
    return render_template('home.html')

@app.route('/text_analysis', methods=['POST'])
def text_analysis():
    input_text = request.form.get('input_text')
    if input_text:
        analysis_result, detected_positions = process_text(input_text)
        return render_template('home.html', analysis_result=analysis_result, detected_positions=detected_positions)
    return 'Error: No text received', 400

def process_text(content):
    lines = content.splitlines()
    analysis_output = []
    positions_detected = []
    for line in lines:
        line = line.strip()
        if line.startswith('//') or line == 'config_start' or line == 'config_end' or not line:
            continue
        if line.startswith('ADD'):
            match = re.match(r'ADD x: (\d+), y: (\d+)', line)
            if match:
                x = int(match.group(1))
                y = int(match.group(2))
                if 1 <= x <= 4 and 1 <= y <= 4:
                    bomb_pos = (y - 1) * 4 + x
                    positions_detected.append(str(bomb_pos))
                    bomb_command = f'{bomb_pos}\n'
                    arduino_device.write(bomb_command.encode())
                    analysis_output.append(f"Valid instruction: {line} -> Position {bomb_pos}")
    return analysis_output, positions_detected

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080)
```

---

### Código Fuente Arduino (resumen)

El código en Arduino gestiona:

* Interacción con teclado matricial
* Control de flip-flops para RAM
* Visualización con LEDs y LCD
* Estados de juego: configuración, jugando, game over

 **Funciones clave**:

* `procesarEntradas()` – lee comandos de Bluetooth y USB
* `leerFlipFlop()` – detecta si hay bomba y actualiza el puntaje
* `resetSistema()` – reinicia LEDs, RAM, LCD y variables
* `actualizarPantalla()` – muestra mensajes e indicadores en la pantalla

---

##  Comandos Reconocidos

| Comando            | Descripción                     |
| ------------------ | ------------------------------- |
| `configuracion`    | Inicia el modo configuración    |
| `finconfiguracion` | Finaliza configuración          |
| `initJuego`        | Inicia el juego                 |
| `finJuego`         | Finaliza el juego               |
| `reset`            | Reinicia el sistema completo    |
| `modoFiesta`       | Activa animación de celebración |
| `1` a `16`         | Verifica casilla específica     |

---

##  Mapeo de Pines Arduino

| Funcionalidad     | Pines                                      |
| ----------------- | ------------------------------------------ |
| Flip-Flops IN     | 22, 24, 26, ..., 52                        |
| Flip-Flops RD     | 23, 25, 27, ..., 53                        |
| LEDs (Casillas)   | 3 a 10, A8 a A15                           |
| LCD (I2C)         | SDA/SCL (dirección 0x27)                   |
| Teclado Matricial | A0–A7                                      |
| LEDs Estado       | 13 (Jugando), 12 (Game Over), 11 (Ganaste) |
| CLK               | 2                                          |

---

##  Recomendaciones Técnicas

* Verificar conexión GND común para todos los módulos.
* Usar resistencias en serie para proteger entradas digitales si es necesario.
* Confirmar dirección del LCD con escáner I2C (`0x27` común).
* Evitar interferencias en cables largos para comunicación serial.
* Emparejar correctamente el módulo HC-06 y mantenerlo a 9600 baudios.

---

##  Notas Finales

Este manual proporciona los detalles técnicos necesarios para comprender y mantener el proyecto Buscaminas desde el punto de vista del hardware y software. Se recomienda mantener el código comentado y el circuito ordenado para facilitar la depuración y futuras mejoras.
