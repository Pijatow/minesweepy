from kivy.core.window import Window
from kivy.config import Config
from kivy.app import App

from kivy.uix.screenmanager import ScreenManager, Screen

from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.uix.togglebutton import ToggleButton
from kivy.uix.boxlayout import BoxLayout

from main import Game, Cell


class MinesweepyApp(App):
    def build(self):
        sm = ScreenManager()
        self.sm = sm

        welcome = Screen(name="welcome")
        play = Screen(name="play")
        game_over = Screen(name="game_over")
        win = Screen(name="win")

        sm.add_widget(welcome)
        sm.add_widget(play)
        sm.add_widget(game_over)
        sm.add_widget(win)

        def on_select(instance):
            self.selected_difficulty = instance.text.lower()
            g = Game(self.selected_difficulty)
            self.g = g
            self.board_row = g.board_size
            self.board_col = g.board_size

            # xy pixel size of cells
            self.cell_x, self.cell_y = 40, 40
            min_window_width = self.cell_x * self.board_col + 100
            min_window_height = self.cell_y * self.board_row + 100
            Window.minimum_width = min_window_width
            Window.minimum_height = min_window_height

            # play screen elements
            stack = FloatLayout()
            game_info = Label(
                text=f"{self.g.difficulty}\ntotal bombs:{self.g.bomb_count}\nsize:{self.g.board_size}x{self.g.board_size}"
            )
            grid = GridLayout()

            # create an empty 2d list of cells
            self.buttons = [
                [None for _ in range(self.board_row)] for _ in range(self.board_col)
            ]
            board = self.g.board

            # add cell button widgets
            for x in range(self.board_col):
                for y in range(self.board_row):
                    bomb_cell = Button(on_touch_down=self.on_click)
                    bomb_cell.cell = board[x][y]
                    grid.add_widget(bomb_cell)
                    self.buttons[x][y] = bomb_cell

            # register play screen and its widgets
            stack.add_widget(grid)
            stack.add_widget(game_info)
            play.add_widget(stack)

            self.update_board()
            Window.size = (min_window_width, min_window_height)
            sm.current = "play"

        # welcome screen elements
        welcome_layout = BoxLayout(orientation="vertical")

        # render difficulty choices
        btn1 = ToggleButton(text="Small", group="difficulty")
        btn1.bind(on_press=on_select)

        btn2 = ToggleButton(text="Easy", group="difficulty")
        btn2.bind(on_press=on_select)

        btn3 = ToggleButton(text="Medium", group="difficulty")
        btn3.bind(on_press=on_select)

        btn4 = ToggleButton(text="Test", group="difficulty")
        btn4.bind(on_press=on_select)

        welcome_layout.add_widget(btn1)
        welcome_layout.add_widget(btn2)
        welcome_layout.add_widget(btn3)
        welcome_layout.add_widget(btn4)
        welcome.add_widget(welcome_layout)

        # game_over screen elements
        game_over_layout = Label(
            text="GAME OVER!", pos_hint={"center_x": 0.5, "center_y": 0.5}
        )
        game_over.add_widget(game_over_layout)

        # win screen elements
        win_layout = Label(text="WON!", pos_hint={"center_x": 0.5, "center_y": 0.5})
        win.add_widget(win_layout)

        return sm

    def on_click(self, instance, touch):
        if instance.collide_point(*touch.pos):  # Check if click is within this button
            cell: Cell = instance.cell
            if touch.button == "left":
                result = cell.reveal()
                if not result:  # GAME OVER
                    self.sm.current = "game_over"
            elif touch.button == "right":
                cell.toggle_flagged()

            # check winning condition
            if Cell.raw_flag_count == self.g.bomb_count == Cell.bomb_flag_count:
                self.sm.current = "win"
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
    Config.set("input", "mouse", "mouse,disable_multitouch")
    Window.size = (400, 500)

    MinesweepyApp().run()
