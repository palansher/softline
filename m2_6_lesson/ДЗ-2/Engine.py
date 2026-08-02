class Engine:
    """Двигатель"""
    def __init__(self,type):
        self.type = type
    
    def __str__(self):
        return f'{self.type}'
    