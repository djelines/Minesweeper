import random

class Minesweeper:
    def __init__(self, rows, columns, bombs):
        """
        Initializes a new instance of the Minesweeper class.
        :param rows: Number of rows in the grid.
        :param columns: Number of columns in the grid.
        :param bombs: Number of bombs in the field.
        """
        self.__rows = rows
        self.__columns = columns
        self.__bombs = bombs
        self.__matrix = [["0" for _ in range(columns)] for _ in range(rows)]
        self.__display_matrix = [[" " for _ in range(columns)] for _ in range(rows)]
        self.__flags = 0
        self.__first_click = True

    def __place_bombs(self, first_click_row, first_click_col):
        """
        Randomly places bombs on the grid while avoiding the user's
        initial clicked cell.
        :param first_click_row: Row of the first click.
        :param first_click_col: Column of the first click.
        """
        placed_bombs = 0
        while placed_bombs < self.__bombs:
            i = random.randint(0, self.__rows - 1)
            j = random.randint(0, self.__columns - 1)
            # Ensures the cell is not the initial clicked cell
            if (i, j) != (first_click_row, first_click_col) and self.__matrix[i][j] != "B":
                self.__matrix[i][j] = "B"
                placed_bombs += 1

        self.__calculate_numbers()

        # If the initial cell is not "0", relocate bombs
        while self.__matrix[first_click_row][first_click_col] != "0":
            for x in range(-1, 2):
                for y in range(-1, 2):
                    new_i = first_click_row + x
                    new_j = first_click_col + y
                    if (0 <= new_i < self.__rows and 0 <= new_j < self.__columns and self.__matrix[new_i][new_j] == "B"):
                        self.__matrix[new_i][new_j] = "0"
                        while True:
                            i = random.randint(0, self.__rows - 1)
                            j = random.randint(0, self.__columns - 1)
                            if self.__matrix[i][j] == "0" and (i, j) != (first_click_row, first_click_col):
                                self.__matrix[i][j] = "B"
                                break
            self.__calculate_numbers()

    def __calculate_numbers(self):
        """
        Calculates the number of adjacent bombs for each cell in the grid
        and updates the grid accordingly.
        """
        for i in range(self.__rows):
            for j in range(self.__columns):
                if self.__matrix[i][j] == "B":
                    continue

                count = 0
                for x in range(-1, 2):
                    for y in range(-1, 2):
                        new_i = i + x
                        new_j = j + y
                        if 0 <= new_i < self.__rows and 0 <= new_j < self.__columns and self.__matrix[new_i][
                            new_j] == "B":
                            count += 1
                self.__matrix[i][j] = str(count)

    def __reveal_cells(self, row, col):
        """
        Recursively reveals adjacent cells if no bombs
        are present around the initial cell.
        :param row: Row of the cell to reveal.
        :param col: Column of the cell to reveal.
        """
        if not (0 <= row < self.__rows and 0 <= col < self.__columns) or self.__display_matrix[row][col] != " ":
            return

        self.__display_matrix[row][col] = self.__matrix[row][col]

        if self.__matrix[row][col] == "0":
            for x in range(-1, 2):
                for y in range(-1, 2):
                    if x != 0 or y != 0:
                        self.__reveal_cells(row + x, col + y)

    def display_solution(self):
        """
        Displays the complete grid with solutions (bombs and numbers).
        """
        print("--- Solution ---")
        for row in self.__matrix:
            print(" ".join(row))

    def click_cell(self, row, col):
        """
        Handles a cell click on the grid.
        :param row: Row of the clicked cell.
        :param col: Column of the clicked cell.
        :return: "lost" if a bomb is clicked, "continue" otherwise, or "flagged" if a flag is present.
        """

        if self.__display_matrix[row][col] == "F":
            return "flagged"  # Do not reveal a flagged cell

        if self.__first_click:
            self.__place_bombs(row, col)  # Place bombs before the first click
            self.__calculate_numbers()
            self.__first_click = False
            self.display_solution()  # Display the solution

        if self.__matrix[row][col] == "B":
            return "lost"

        self.__reveal_cells(row, col)
        return "continue"

    def toggle_flag(self, row, col):
        """
        Adds or removes a flag on a specific cell.
        :param row: Row of the cell.
        :param col: Column of the cell.
        """

        if self.__display_matrix[row][col] == " ":
            self.__display_matrix[row][col] = "\U0001F6A9"  # Red flag
        elif self.__display_matrix[row][col] == "\U0001F6A9":
            self.__display_matrix[row][col] = " "

    def is_won(self):
        """
        Checks if the player has won the game.
        A game is won if all cells without bombs are revealed
        and all cells containing bombs are either not revealed or flagged.
        :return: True if the game is won, False otherwise.
        """
        for i in range(self.__rows):
            for j in range(self.__columns):
                # If a non-bomb cell is not revealed, the player has not won
                if self.__matrix[i][j] != "B" and self.__display_matrix[i][j] == " ":
                    return False
                # If a bomb cell is revealed without a flag, the player has not won
                if self.__matrix[i][j] == "B" and self.__display_matrix[i][j] not in [" ", "\U0001F6A9"]:
                    return False
        return True

    def get_display_matrix(self):
        """
        Returns the current grid to display to the player.
        :return: Display matrix.
        """
        return self.__display_matrix

    def save_first_click(self, row, col):
        """
        Saves the first click for a given grid.
        :param row: Row of the first click.
        :param col: Column of the first click.
        """
        self.first_click_row = row
        self.first_click_col = col

    def load_saved_grid(self, grid_data):
        """
        Loads a saved grid and restores initial parameters.
        :param grid_data: Grid data.
        """
        self.__matrix = grid_data
        self.__first_click = False  # Disable random generation
