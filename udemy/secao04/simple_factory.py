from abc import ABCMeta, abstractmethod

class Animal(metaclass=ABCMeta):

    @abstractmethod
    def falar(self):
        pass

class Cachorro(Animal):

    def falar(self):
        print('Au au!')

class Gato(Animal):

    def falar(self):
        print('Miau!')

class Camelo(Animal):

    def falar(self):
        print('Quente')

class Fabrica:

    def criar_animal(self, tipo):
        return eval(tipo)()

if __name__ == '__main__':
    fabrica = Fabrica()
    animal = input('Qual animal você quer que fale? [Cachorro, Gato, Camelo]')
    animal = fabrica.criar_animal(animal)
    animal.falar()
    print(animal.__dict__ )
