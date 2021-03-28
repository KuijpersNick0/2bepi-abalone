import json

class Grid():
    def __init__(self, myColor):
        self.directions = {
            "NW":[-1, -1],
            "NE":[ 1,  1],
            "E" :[ 0,  1],
            "SE":[ 1,  1],
            "SW":[ 1,  0],
            "W" :[ 0, -1]}
        self.state = None
        self.myColor = myColor
        Grid.BuildGrid(self)

    def BuildGrid(self):
        with open("../Data/state.json", "r") as f:
            data = f.read()

        self.state = json.loads(data)
    
    def __Tests(self, row, column):
        def CheckLimits(self, row, column):
            if self.state["board"][row][column] == 'X':
                raise ValueError(f"[{row}, {column}] is out of board")

        def CheckEmpty(self, row, column):
            if self.state["board"][row][column] == "E":
                raise ValueError(f"[{row}, {column}] is an empty place")

        def CheckColor(self, row, column):
            if self.state["board"][row][column] != self.myColor:
                raise ValueError(f"[{row}, {column}] is not the right color")

        CheckLimits(self, row, column)
        CheckEmpty(self, row, column)
        CheckColor(self, row, column)

    def MoveMarbles(self, marbles:list, direction:str):
        for marble in marbles:
            self.__Tests(marble[0], marble[1])

        marbles.sort();

        print("Smaller marble : ", marbles[0])
        print("Bigger marble : ")

        


a = Grid("W")
a.MoveMarbles([[2, 2],[1, 1]], "SW")