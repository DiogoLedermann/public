class Robot():

    def __init__(self, name, color, weight):
        self.name = name
        self.color = color
        self.weight = weight
        self.owner = None

    def introduceSelf(self):
        print(f'Hello World! My name is {self.name} and my owner is {self.owner}!')

class Person():

    def __init__(self, name=None, personality=None, stance='standing'):
        self.name = name
        self.personality = personality
        self.stance = stance
        self.robotOwned = None

    def layDown(self):
        self.stance = 'laying'

    def sitDown(self):
        self.stance = 'sitting'

    def standUp(self):
        self.stance = 'standing'

    def buyRobot(self, robot):
        self.robotOwned = robot
        robot.owner = self.name

r1 = Robot('Tom', 'red', 30)
r2 = Robot('Jerry', 'blue', 40)

p1 = Person('Alice', 'agressive', stance='standing')
p2 = Person('Becky', 'talkative', stance='sitting')

p1.buyRobot(r2)
p2.buyRobot(r1)

p1.robotOwned.introduceSelf()
p2.robotOwned.introduceSelf()
