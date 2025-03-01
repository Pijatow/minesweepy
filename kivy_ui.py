from kivy.app import App
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.config import Config

from main import Game, Cell


class MinesweepyApp(App):
    def build(self):
        grid = GridLayout(cols=x, rows=y)

        # create an empty 2d list of cells
        self.buttons = [[None for _ in range(x)] for _ in range(y)]

        for i in range(y):
            for j in range(x):
                bomb_cell = Button(
                    size_hint=(None, None),
                    size=(cell_x, cell_y),
                    on_touch_down=self.on_click,
                )
                bomb_cell.cell = board[i][j]
                grid.add_widget(bomb_cell)
                self.buttons[i][j] = bomb_cell  # Store the button reference
        return grid

    def on_click(self, instance, touch):
        if instance.collide_point(*touch.pos):  # Check if click is within this button
            cell: Cell = instance.cell

            # This method is called when any button is pressed
            if touch.button == "left":
                cell.reveal()
            elif touch.button == "right":
                cell.toggle_flagged()


if __name__ == "__main__":
    g = Game(difficulty="easy")
    x = y = g.board_size
    board = g.get_board_object()

    # xy pixel size of cells
    cell_x, cell_y = 40, 40

    # Set window size before the app starts
    Config.set("graphics", "width", f"{cell_y*g.board_size}")
    Config.set("graphics", "height", f"{cell_x*g.board_size}")

    Config.set("input", "mouse", "mouse,disable_multitouch")
    MinesweepyApp().run()
