
class Controller:
    
    def __init__(self, model, view):
        self.model = model
        self.view = view

        self.view.button_open.clicked.connect \
            (lambda: self.extend(self.view.button_open.text()))

        self.view.button_close.clicked.connect \
            (lambda: self.extend(self.view.button_close.text()))

        self.view.button_delete.clicked.connect \
            (self.delete)

        self.view.button_add.clicked.connect \
            (lambda: self.extend(self.view.button_add.text()))

        self.view.button_7.clicked.connect \
            (lambda: self.extend(self.view.button_7.text()))

        self.view.button_8.clicked.connect \
            (lambda: self.extend(self.view.button_8.text()))

        self.view.button_9.clicked.connect \
            (lambda: self.extend(self.view.button_9.text()))

        self.view.button_subtract.clicked.connect \
            (lambda: self.extend(self.view.button_subtract.text()))

        self.view.button_4.clicked.connect \
            (lambda: self.extend(self.view.button_4.text()))

        self.view.button_5.clicked.connect \
            (lambda: self.extend(self.view.button_5.text()))

        self.view.button_6.clicked.connect \
            (lambda: self.extend(self.view.button_6.text()))

        self.view.button_multiply.clicked.connect \
            (lambda: self.extend(self.view.button_multiply.text()))

        self.view.button_1.clicked.connect \
            (lambda: self.extend(self.view.button_1.text()))

        self.view.button_2.clicked.connect \
            (lambda: self.extend(self.view.button_2.text()))

        self.view.button_3.clicked.connect \
            (lambda: self.extend(self.view.button_3.text()))

        self.view.button_divide.clicked.connect \
            (lambda: self.extend(self.view.button_divide.text()))

        self.view.button_opposite.clicked.connect \
            (self.opposite)

        self.view.button_0.clicked.connect \
            (lambda: self.extend(self.view.button_0.text()))

        self.view.button_point.clicked.connect \
            (lambda: self.extend(self.view.button_point.text()))

        self.view.button_equals.clicked.connect \
            (self.evaluate)

    def update_view(self):
        self.view.line_edit.setText(self.model.expression)
    
    def extend(self, char):
        self.model.extend(char)
        self.update_view()
    
    def delete(self):
        self.model.delete()
        self.update_view()

    def opposite(self):
        self.model.opposite()
        self.update_view()

    def evaluate(self):
        self.model.evaluate()
        self.update_view()
    
    def on(self):
        self.view.show()
