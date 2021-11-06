class Request:
    def __init__(self, lhs, rhs, result):
        self.left = lhs
        self.right = rhs
        self.result = result

    def __repr__(self):
        return f"Request: ({self.left}, {self.right}, {self.result})"