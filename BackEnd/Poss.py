class Posicion:
    def __init__(self, posx, posy):
        self.Posx = posx
        self.Posy = posy

    def __repr__(self):
        return f'Pocision(x={self.Posx}, y={self.Posy})'

    def getX(self):
        return self.Posx

    def getY(self):
        return self.Posy