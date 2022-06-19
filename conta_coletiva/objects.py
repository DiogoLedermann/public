import json

class Problem:

    def __init__(self, jsonFile):
        with open(jsonFile) as file:
            data = json.load(file, encoding='utf-8')
        participants = data['Participants']
        products = data['Products']

        self.participants = []
        for participantName in participants:
            self.participants.append(Participant(participantName))
        
        self.products = []
        for productName, productPrice in products:
            self.products.append(Product(productName, productPrice))
    
    def registerConsumers(self):
        print()
        for participant in self.participants:
            for product in self.products:
                answer = yesOrNo(f'Did {participant} consume {product}?')
                if answer == 'y':
                    participant.addConsumed(product)
                    product.addConsumer()
    
    def registerBuyers(self):
        print()
        for participant in self.participants:
            for product in self.products:
                answer = yesOrNo(f'Did {participant} buy {product}?')
                if answer == 'y':
                    participant.addBought(product)
                    product.addBuyer()

    def calculateDebts(self):
        for participant in self.participants:
            for product in participant.consumed:
                participant.debt += product.price / product.consumers
            for product in participant.bought:
                participant.debt -= product.price / product.buyers

    def transactions(self):
        print()
        payers = []
        recievers = []
        for participant in self.participants:
            if participant.debt > 0:
                payers.append(participant)
            elif participant.debt < 0:
                recievers.append(participant)
        
        i, j = 0, 0
        while i < len(payers):
            currentPayer = payers[i]
            currentReceiver = recievers[j]
            if currentPayer.debt > abs(currentReceiver.debt):
                print(f'{currentPayer.name:12} gives {currentReceiver.name:12} ${abs(currentReceiver.debt):.2f}')
                currentPayer.updateDebt(currentReceiver.debt)
                currentReceiver.updateDebt(-currentReceiver.debt)
                j += 1
            else:
                print(f'{currentPayer.name:12} gives {currentReceiver.name:12} ${currentPayer.debt:.2f}')
                currentPayer.updateDebt(-currentPayer.debt)
                currentReceiver.updateDebt(currentPayer.debt)
                i += 1

    def solve(self):
        self.registerConsumers()
        self.registerBuyers()
        self.calculateDebts()
        self.transactions()

class Participant:
    
    def __init__(self, name):
        self.name = name
        self.consumed = []
        self.bought = []
        self.debt = 0
    
    def __repr__(self):
        return self.name
    
    def addConsumed(self, product):
        self.consumed.append(product)
    
    def addBought(self, product):
        self.bought.append(product)
    
    def updateDebt(self, value):
        self.debt += value

class Product:

    def __init__(self, name, price):
        self.name = name
        self.price = price
        self.consumers = 0
        self.buyers = 0
    
    def __repr__(self):
        return self.name
    
    def addConsumer(self):
        self.consumers += 1
    
    def addBuyer(self):
        self.buyers += 1