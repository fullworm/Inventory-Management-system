class State:
    def __init__(self, name):
        self.name = name
        self.finished = False
        self.next_state = ""

    def hasFinished(self) -> bool:
        return self.finished

    def setFinished(self, finished:bool) -> None:
        self.finished = finished

    def setNextState(self, state: str) -> None:
        self.next_state = state

    def getNextState(self) -> str:
        return self.next_state