from random import randint

board = []

COLORS = {
    "RED": "\033[91m",
    "BLUE": "\033[94m",
    "GREEN": "\033[92m",
    "YELLOW": "\033[93m",
    "PURPLE": "\033[95m",
    "CYAN": "\033[96m",
    "RESET": "\033[0m",
}


class Game:
    def __init__(self, difficulty="small"):
        """difficulty = easy, medium or hard"""
        self.level = {
            # pair of (bomb_count, board_size)
            "test": (1, 3),
            "small": (15, 10),
            "easy": (120, 25),
            "medium": (150, 30),
            "hard": (170, 30),
        }
        self.difficulty = difficulty
        self.bomb_count, self.board_size = self.level.get(difficulty)
        self.generate_board(self.board_size, self.bomb_count)

    def get_board_object(self):
        return board

    def generate_board(self, board_size, bomb_count):
        # make empty board
        global board
        for i in range(board_size):
            row = []
            for j in range(board_size):
                row.append(Cell(i, j, self))
            board.append(row)

        # populate empty board with bombs
        planted_bombs = 0
        while planted_bombs < bomb_count:
            rand_i = randint(0, board_size - 1)
            rand_j = randint(0, board_size - 1)
            random_cell: Cell = board[rand_i][rand_j]
            if random_cell.convert_to_bomb():  # successful plant
                planted_bombs += 1
        self.board = board

    def render_in_cli(self):
        # print game info
        print(
            f"bomb count:{self.bomb_count}, size:{self.board_size}, difficulty:{self.difficulty}"
        )
        print()

        # top row nums in cyan
        print(COLORS["CYAN"], end="")
        for i in range(self.board_size + 1):
            print(str(i).center(3), end="")
        print(COLORS["RESET"])

        # print grid
        for row_num in range(self.board_size):
            # print left column num in cyan
            print(COLORS["CYAN"] + str(row_num + 1).ljust(3) + COLORS["RESET"], end="")

            for cell in self.board[row_num]:
                if cell.is_bomb:
                    print(COLORS["RED"] + str("#").center(3) + COLORS["RESET"], end="")
                else:
                    print(str(cell.neighbor_bombs_count()).center(3), end="")
            print()


class Cell:
    def __init__(self, row, column, parent: Game):
        self.parent = parent
        self.states = ["hidden", "revealed", "flagged"]
        self.state = self.states[0]  # hidden
        self.is_bomb = False
        self.row = row
        self.column = column

    def convert_to_bomb(self):
        if not self.is_bomb:
            self.is_bomb = True
            return True
        return False

    def toggle_flagged(self):
        if self.state == self.states[1]:  # if revealed, skip
            pass
        elif self.state == self.states[2]:  # if flagged, switch to hidden
            self.state = self.states[0]
        elif self.state == self.states[0]:  # if hidden, switch to flagged
            self.state = self.states[2]

    def game_over(self):
        print("GAME OVER")

    def convert_to_revealed(self):
        self.state = self.states[1]

    def reveal(self):
        if self.is_bomb:
            self.convert_to_revealed()
            self.game_over()
        elif self.neighbor_bombs_count() == 0:
            self.convert_to_revealed()
            for cell in self.get_neighbor_cells():
                if cell.state != self.states[1]:
                    cell.reveal()
        else:
            self.convert_to_revealed()

    def get_neighbor_cells(self):
        # Calculate valid cell boundaries
        # Ensure indices don't go out of bounds (stay between 0 and board size)
        istart = max(0, self.row - 1)
        iend = min(self.parent.board_size - 1, self.row + 1)
        jstart = max(0, self.column - 1)
        jend = min(self.parent.board_size - 1, self.column + 1)

        # get list of neighboring cells
        neighbor_cells = []
        for i in range(istart, iend + 1):
            for j in range(jstart, jend + 1):
                # Skip self
                if i == self.row and j == self.column:
                    continue
                neighbor = board[i][j]
                neighbor_cells.append(neighbor)
        return neighbor_cells

    def neighbor_bombs_count(self):
        count = 0
        for cell in self.get_neighbor_cells():
            if cell.is_bomb:
                count += 1
        return count

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        if self.state == self.states[0]:  # hidden
            return " "
        elif self.state == self.states[2]:  # flagged
            return "?"
        elif self.state == self.states[1]:  # revealed
            if self.is_bomb:
                return "#"
            elif self.neighbor_bombs_count() == 0:
                return " "
            else:
                return str(self.neighbor_bombs_count())


if __name__ == "__main__":
    g = Game("small")
