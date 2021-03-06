"""
Base
****

Basic class for all inherited classes.
"""

class Base:
    def __init__(self, parent):
        self._parent = parent
        self.logger = parent.logger
        self.events = parent.events

    def loop(self):
        pass

    """
    # disabled because __dict__ doesn't have all the
    # functions and attributes of a class
    # (and because this wasn't really needed)

    def __getattr__(self, attrname):
        if attrname in self.__dict__:
            return self.__dict__[attrname]
        else:
            return Pipe(self._parent, attrname)
    """


class Pipe():
    """
    Pipe commands from the base class (children) to the events module

    e.g., in io.py you can do: self.setFlashlightMode(power=True) and this
    will call events.setFlashlightMode(power=True)
    """
    def __init__(self, parent, name):
        self._parent = parent
        self._function = name

    def __call__(self, *args, **kwargs):
        events = self._parent.events
        functions = events.__class__.__dict__

        if self._function in functions:
            return functions[self._function](events, *args, **kwargs)
        else:
            raise AttributeError("Event \"{0}\" not found".format(self._function))
