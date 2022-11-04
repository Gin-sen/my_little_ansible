"""todo.py"""


class Todo:
    """class todo"""
    def __init__(self, name: str, params: dict):
        self.name = name
        self.params = params

    def __repr__(self):
        return f"{self.__class__.__name__}(name={self.name}, params={self.params})"

    def __str__(self):
        return f"{self.__class__.__name__}({self.name}, params={self.params})"
