<<<<<<< HEAD
from flask import Flask, request
from analizador import Analizer, posiciones
import serial
import time

app = Flask(__name__)

# Matriz de referencia
matrix = [
    [0, 1, 2, 3],
    [4, 5, 6, 7],
    [8, 9, 'A', 'B'],
    ['C', 'D', 'E', 'F']
]

# Función para enviar un mensaje por el puerto serial
def enviar_serial(mensaje):
    try:
        with serial.Serial('COM5', 9600, timeout=1) as puerto:
            puerto.write(mensaje)
            print(f"📤 Enviado: {mensaje}")
            respuesta = leer_serial(puerto)
            if respuesta:
                print(f"📥 Respuesta recibida: {respuesta}")
            else:
                print("❌ No se recibió respuesta.")
    except serial.SerialException as e:
        print("❌ Error al abrir el puerto serial:", e)


# Función para leer la respuesta del puerto serial
def leer_serial(puerto):
    try:
        if puerto.in_waiting > 0:  # Verifica si hay datos disponibles
            respuesta = puerto.readline().decode('utf-8').strip()
            return respuesta
        else:
            return None
    except serial.SerialException as e:
        print("❌ Error al leer del puerto serial:", e)
        return None


# Ruta de prueba
=======
from flask import Flask,request
from analizador import Analizer
from analizador import posiciones

app = Flask(__name__)

# matrix[x-1][y-1]
matrix = [
            [0,1,2,3],
            [4,5,6,7],
            [ 8,9,'A','B'],
            ['C','D','E','F']
        ]

>>>>>>> 7a6386a8397ee67148979d2bacbb9063b3ad698f
@app.route('/ping')
def ping():
    return 'pong'

<<<<<<< HEAD
# Ruta para analizar el texto y enviar datos por el puerto serial
@app.route('/analizer', methods=['POST'])
def analizer():
    txt = request.data.decode('utf-8')
    posiciones.clear()
    enviar_serial(b'modoFiesta\n')
    # Analizer(txt)
    # enviar_serial('configuracion')
    # for pos in posiciones:
    #     x, y = pos.getX(), pos.getY()
    #     if 0 <= x < 4 and 0 <= y < 4:
    #         valor = str(matrix[x][y])
    #         enviar_serial(valor)
    #         time.sleep(1)
    #     else:
    #         print(f"⚠️ Posición fuera de rango: x={x}, y={y}")
    # enviar_serial('finconfiguracion')
    return '✅ Datos procesados y enviados'

# Ejecutar el servidor
if __name__ == '__main__':
    app.run(debug=True, port=4000)
=======
@app.route('/analizer',methods=['POST'])
def analizer():
    txt = request.data.decode('utf-8')
    posiciones.clear()
    Analizer(txt)
    for pos in posiciones:
        if(pos.getX() < 4 and pos.getY() < 4 ):
            print(matrix[pos.getX()][pos.getY()])
        else:
            print('rangos no permitidos debe ser x<4 y y<4')
    return 'recibido'

if __name__ == '__main__':
    app.run(debug = True, port=4000)
>>>>>>> 7a6386a8397ee67148979d2bacbb9063b3ad698f
