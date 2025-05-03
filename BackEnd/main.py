from flask import Flask, request, jsonify
from analizador import Analizador, posiciones
import serial
import time
import os
from flask_cors import CORS

# Inicialización de Flask
app = Flask(__name__)
CORS(app, origins=["http://localhost:5173"])
# Configuración global del puerto serial
puerto_serial = None

# Matriz de referencia
matrix = [
    [0, 1, 2, 3],
    [4, 5, 6, 7],
    [8, 9, 'A', 'B'],
    ['C', 'D', 'E', 'F']
]

# ================== Configuración Serial ==================
def inicializar_serial():
    global puerto_serial
    try:
        puerto_serial = serial.Serial(
            port='COM14',
            baudrate=9600,
            timeout=1,
            dsrdtr=False  # Evita reinicio por DTR
        )
        time.sleep(2)  # Espera inicialización Arduino
        print("✅ Puerto serial inicializado")
    except serial.SerialException as e:
        print(f"❌ Error al abrir puerto serial: {e}")

def enviar_serial(mensaje):
    if puerto_serial and puerto_serial.is_open:
        try:
            puerto_serial.write(mensaje)
            print(f"📤 Enviado: {mensaje}")
            respuesta = leer_serial()
            if respuesta:
                print(f"📥 Respuesta recibida: {respuesta}")
            else:
                print("❌ No se recibió respuesta.")
        except Exception as e:
            print(f"❌ Error en comunicación serial: {e}")
    else:
        print("⚠️ Puerto serial no disponible")

def leer_serial():
    try:
        # Esperar datos con timeout más largo
        start_time = time.time()
        while (time.time() - start_time) < 2:  # Esperar máximo 2 segundos
            if puerto_serial.in_waiting > 0:
                respuesta = puerto_serial.readline().decode('utf-8').strip()
                return respuesta
            time.sleep(0.1)
        return None
    except Exception as e:
        print(f"❌ Error al leer serial: {e}")
        return None

# ================== Endpoints API ==================
@app.route('/ping')
def ping():
    return 'pong'

@app.route('/manual', methods=['POST'])
def manual():
    try:
        data = request.get_json()
        
        if not data or 'mensaje' not in data:
            return jsonify({"error": "Formato JSON inválido o falta campo 'mensaje'"}), 400
        
        mensaje = data['mensaje']
        posiciones.clear()
        
        # Enviar mensaje al Arduino
        enviar_serial(f"{mensaje}\n".encode('utf-8'))
        
        return jsonify({"status": "success", "message": "Comando enviado al Arduino"})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/analizer', methods=['POST'])
def analizer():
    try:
        txt = request.data.decode('utf-8')
        posiciones.clear()
        
        # Procesar el texto con el analizador
        Analizador(txt)
        
        # Enviar secuencia de comandos al Arduino
        enviar_serial(b'configuracion\n')
        time.sleep(1)
        
        # Enviar posiciones validadas
        for pos in posiciones:
            x, y = pos.getX(), pos.getY()
            if 0 <= x < 4 and 0 <= y < 4:
                valor = str(matrix[x][y])
                enviar_serial(f"{valor}\n".encode('utf-8'))
                time.sleep(0.5)
            else:
                print(f"⚠️ Posición inválida: x={x}, y={y}")
        
        # Finalizar configuración
        enviar_serial(b'finconfiguracion\n')
        time.sleep(1)
        
        return jsonify({
            "status": "success",
            "message": "Configuración completada",
            "posiciones_validas": len(posiciones)
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ================== Inicialización ==================
if __name__ == '__main__':
    # Solo inicializa el serial si no es el proceso de reload
    if not os.environ.get('WERKZEUG_RUN_MAIN'):
        inicializar_serial()
    
    try:
        app.run(debug=True, port=4000, use_reloader=False)  # Desactiva el reloader integrado
    finally:
        if puerto_serial and puerto_serial.is_open:
            puerto_serial.close()
            print("🔌 Puerto serial cerrado")