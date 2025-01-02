"""Module for implementing an observable pattern."""

class WatchedVariable:
    """A wrapper for a variable to fire an on_change event.
    """
    def __init__(self):
        self._value = None

    @property
    def value(self):
        """Gets the value wrapped by the object.
        """
        return self._value

    @value.setter
    def value(self, new_value):
        """Sets the value wrapped by the object and triggers
        the on_change callback.
        """
        self._value = new_value
        if self._value is not None:
            self.on_change()

    def on_change(self):
        """Callback to be overriden."""
