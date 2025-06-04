class State:
    def __init__(self, name, next_state):
        self.name = name
        self.next_state = next_state

    def setNextState(self, state:str) -> None:
        self.next_state = state

    def getNextState(self):
        return self.next_state