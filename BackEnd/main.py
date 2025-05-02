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

@app.route('/ping')
def ping():
    return 'pong'

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
