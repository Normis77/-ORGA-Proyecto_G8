class Posicion:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def getX(self): 
        return self.x - 1 if self.x > 0 else 0  # Previene valores negativos
    
    def getY(self): 
        return self.y - 1 if self.y > 0 else 0