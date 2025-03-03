from kivy.core.window import Window

from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.config import Config

from main import Game, Cell


class MinesweepyApp(App):
    def __init__(self, board_row, board_col, cell_x, cell_y):
        super().__init__()
        self.board_row = board_row
        self.board_col = board_col
        self.cell_x = cell_x
        self.cell_y = cell_y

    def build(self):
        stack = BoxLayout(orientation="vertical")

        game_info = Label()
        grid = GridLayout()

        # create an empty 2d list of cells
                bomb_cell = Button(
                    font_size=20,
                    size_hint=(None, None),
                    size=(cell_x, cell_y),
                    on_touch_down=self.on_click,
                )
        self.buttons = [
            [None for _ in range(self.board_row)] for _ in range(self.board_col)
        ]

        for x in range(self.board_col):
            for y in range(self.board_row):
                bomb_cell.cell = board[x][y]
                grid.add_widget(bomb_cell)
                self.buttons[x][y] = bomb_cell  # Store the button reference

        stack.add_widget(grid)
        stack.add_widget(game_info)
        self.update_board()

        return stack

    def on_click(self, instance, touch):
        if instance.collide_point(*touch.pos):  # Check if click is within this button
            cell: Cell = instance.cell

            # This method is called when any button is pressed
            if touch.button == "left":
                cell.reveal()
            elif touch.button == "right":
                cell.toggle_flagged()
            self.update_board()

    def update_board(self):
        """Update the text and color of all buttons based on the board state."""
        for i in range(self.board_col):
            for j in range(self.board_row):
                button = self.buttons[i][j]
                cell = button.cell

                # coloring the cells
                if cell.state == "revealed":
                    if cell.is_bomb:
                        # Red for bomb
                        rgba = [1, 0, 0, 1]
                    elif cell.neighbor_bombs_count() == 0:
                        # black for empty cells
                        rgba = [0, 0, 0, 1]
                    else:
                        # Light gray for revealed
                        rgba = [1, 1, 1, 0.3]
                elif cell.state == "flagged":
                    # Yellow for flagged
                    rgba = [1, 1, 0, 1]
                elif cell.state == "hidden":
                    # Gray for hidden
                    rgba = [1, 1, 1, 0.5]

                button.background_color = rgba
                button.text = str(cell)


if __name__ == "__main__":
    g = Game(difficulty="small")
    board = g.get_board_object()

    MinesweepyApp.g = g
    MinesweepyApp.board = board

    # xy pixel size of cells
    cell_x, cell_y = 40, 40
    min_window_width = cell_x * g.board_size + 100
    min_window_height = cell_y * g.board_size + 100

    # Set window size before the app starts
    Config.set("graphics", "width", str(min_window_width))
    Config.set("graphics", "height", str(min_window_height))

    Window.minimum_width = min_window_width
    Window.minimum_height = min_window_height
    Config.set("input", "mouse", "mouse,disable_multitouch")
    MinesweepyApp(g.board_size, g.board_size, cell_x, cell_y).run()
