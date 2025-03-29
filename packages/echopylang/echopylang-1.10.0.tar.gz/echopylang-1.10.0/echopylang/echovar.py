class EchoVar:
    def __init__(self):
        self._storage = {}

    def __getattr__(self, name):
        if name in self._storage:
            return self._storage[name]
        raise AttributeError(f"Variable '{name}' not defined")

    def __setattr__(self, name, value):
        if name.startswith('_'):
            super().__setattr__(name, value)
        else:
            self._storage[name] = value

# Синглтон
var = EchoVar()
