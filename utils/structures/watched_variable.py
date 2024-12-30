class WatchedVariable:
    def __init__(self):
        self._value = None
        
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value
        if self._value is not None:
            self.on_change()

    def on_change(self):
        pass