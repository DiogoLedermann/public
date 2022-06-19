
class Model:
    
    def __init__(self):
        self.expression = ''
    
    def extend(self, char):
        self.expression += char
    
    def delete(self):
        self.expression = self.expression[:-1]
    
    def opposite(self):
        if self.expression.startswith('-'):
            self.expression = self.expression[1:]
        else:
            self.expression = '-' + self.expression
    
    def evaluate(self):
        self.expression = str(eval(self.expression))
