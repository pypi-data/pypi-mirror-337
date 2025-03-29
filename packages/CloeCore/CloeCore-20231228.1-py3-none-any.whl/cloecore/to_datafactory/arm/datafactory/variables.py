class Variable:
    def __init__(self, name: str) -> None:
        self.name = name

    def get_standalone(self) -> str:
        return f"[variables('{self.name}')]"

    def get_expression(self) -> str:
        return f"variables('{self.name}')"
