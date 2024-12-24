import tkinter as tk
from tkinter import messagebox, simpledialog
import time
from game_logic import Minesweeper
from score_manager import ScoreManager
import pygame


class MinesweeperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Minesweeper")
        self.score_manager = ScoreManager()  # Gestionnaire des scores
        self.difficulty = None
        self.player_name = "Joueur"
        self.game = None

        self.buttons = []
        self.start_time = None
        self.is_game_over = False
        self.__create_home_menu()

    def __create_home_menu(self):
        """Creates the main home menu for the application."""
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.configure(bg="#AED6F1")
        tk.Label(self.root, text="Bienvenue sur Minesweeper !", font=("Arial", 50, "bold"), fg="#34495E",
                 bg="#AED6F1").pack(pady=30)
        button_frame = tk.Frame(self.root, bg="#AED6F1")
        button_frame.pack(pady=20)
        tk.Button(button_frame, text="Commencer le jeu", font=("Arial", 20, "bold"), bg="#AED6F1", fg="#34495E",
                  relief="raised", bd=5, command=self.__create_difficulty_menu).pack(pady=10)
        tk.Button(button_frame, text="Hall of Fame", font=("Arial", 20, "bold"), bg="#AED6F1", fg="#34495E",
                  relief="raised", bd=5, command=self.__show_hall_of_fame).pack(pady=10)
        tk.Button(button_frame, text="Quitter", font=("Arial", 20, "bold"), bg="#AED6F1", fg="#34495E", relief="raised",
                  bd=5, command=self.root.quit).pack(pady=10)

    def __create_difficulty_menu(self):
        """Displays a menu to allow the player to select the game difficulty."""
        for widget in self.root.winfo_children():
            widget.destroy()

        self.root.configure(bg="#AED6F1")
        tk.Label(self.root, text="Choisissez une difficulté", font=("Arial", 30, "bold"), fg="#34495E",
                 bg="#AED6F1").pack(pady=30)
        button_frame = tk.Frame(self.root, bg="#AED6F1")
        button_frame.pack(pady=20)
        tk.Button(button_frame, text="Facile (9x9, 10 bombes)", font=("Arial", 20), bg="#AED6F1", fg="#34495E",
                  relief="raised", bd=5,
                  command=lambda: self.__ask_player_name_and_start_game(9, 9, 10, "Facile")).pack(pady=10)
        tk.Button(button_frame, text="Moyen (16x16, 40 bombes)", font=("Arial", 20), bg="#AED6F1", fg="#34495E",
                  relief="raised", bd=5,
                  command=lambda: self.__ask_player_name_and_start_game(16, 16, 40, "Moyen")).pack(pady=10)
        tk.Button(button_frame, text="Difficile (30x16, 99 bombes)", font=("Arial", 20), bg="#AED6F1", fg="#34495E",
                  relief="raised", bd=5,
                  command=lambda: self.__ask_player_name_and_start_game(30, 16, 99, "Difficile")).pack(pady=10)
        tk.Button(button_frame, text="Retour", font=("Arial", 20, "bold"), bg="#AED6F1", fg="#34495E", relief="raised",
                  bd=5, command=self.__create_home_menu).pack(pady=20)

    def __ask_player_name_and_start_game(self, rows, cols, bombs, difficulty):
        """Prompts the player to input their name and starts the game with the specified settings."""
        player_name = simpledialog.askstring("Nom du joueur", "Entrez votre nom :", parent=self.root)
        self.player_name = player_name.strip() if player_name else "Joueur"
        self.__start_game(rows, cols, bombs, difficulty)

    def __start_game(self, rows, columns, bombs, difficulty):
        """Initializes and starts the Minesweeper game with the given parameters."""
        for widget in self.root.winfo_children():
            widget.destroy()


        pygame.mixer.init()
        pygame.mixer.music.load("music.mp3")
        pygame.mixer.music.play(-1)

        self.difficulty = difficulty
        self.game = Minesweeper(rows, columns, bombs)
        self.buttons = []
        self.start_time = time.time()
        self.is_game_over = False

        # Frame pour centrer le jeu
        game_frame = tk.Frame(self.root)
        game_frame.pack(expand=True)

        # Ajouter le label du chrono
        self.timer_label = tk.Label(game_frame, text="Temps: 0 secondes", font=("Arial", 20), bg="#AED6F1",
                                    fg="#34495E")
        self.timer_label.grid(row=0, column=0, columnspan=columns, pady=(0, 10))

        # Configurer la grille pour s'ajuster à la taille de la fenêtre
        game_frame.grid_columnconfigure(0, weight=1)
        game_frame.grid_rowconfigure(0, weight=1)

        for i in range(rows):
            row_buttons = []
            game_frame.grid_rowconfigure(i + 1, weight=1)  # Chaque ligne peut se redimensionner

            for j in range(columns):
                btn = tk.Button(game_frame, text=" ", width=3, height=1)
                btn.grid(row=i + 1, column=j,
                         sticky="news")  # Utilisation de sticky pour faire en sorte que les boutons s'ajustent
                btn.bind("<Button-1>", lambda e, r=i, c=j: self.__on_click(r, c))
                btn.bind("<Button-2>", lambda e, r=i, c=j: self.__on_right_click(r, c))
                btn.bind("<Button-3>", lambda e, r=i, c=j: self.__on_right_click(r, c))
                row_buttons.append(btn)
            self.buttons.append(row_buttons)

        self.__update_timer()


    def __update_timer(self):
        """Updates the game timer display every second."""
        if self.is_game_over:
            return

        elapsed_time = int(time.time() - self.start_time)
        self.timer_label.config(text=f"Temps: {elapsed_time} secondes")
        self.root.after(1000, self.__update_timer)

    def __on_click(self, row, col):
        """Handles the action when a player left-clicks on a cell."""
        result = self.game.click_cell(row, col)
        self.__update_buttons()

        if result == "lost":
            pygame.mixer.quit()
            self.is_game_over = True
            elapsed_time = int(time.time() - self.start_time)
            messagebox.showinfo("Game Over", f"Vous avez perdu en {elapsed_time} secondes!")
            self.__save_score(elapsed_time, won=False)

            self.endgame_menu()

        elif self.game.is_won():
            pygame.mixer.quit()
            self.is_game_over = True
            elapsed_time = int(time.time() - self.start_time)
            messagebox.showinfo("Félicitations", f"Vous avez gagné en {elapsed_time} secondes!")
            self.__save_score(elapsed_time, won=True)

            self.endgame_menu()

    def __on_right_click(self, row, col):
        """Handles the action when a player right-clicks on a cell to toggle a flag."""
        self.game.toggle_flag(row, col)
        self.__update_buttons()

    def __update_buttons(self):
        """Refreshes the button display to reflect the current game state."""
        display_matrix = self.game.get_display_matrix()
        for i, row in enumerate(display_matrix):
            for j, value in enumerate(row):
                self.buttons[i][j].config(text=value)

    def endgame_menu(self):
        """
        Show endgame options directly in the current window.
        """
        # Efface les widgets existants
        for widget in self.root.winfo_children():
            widget.destroy()

        # Configure la fenêtre principale pour le menu de fin
        self.root.configure(bg="#AED6F1")

        # Message de victoire ou défaite
        if self.game.is_won():
            message = "Félicitations, vous avez gagné !"
        else:
            message = "Dommage, vous avez perdu."

        # Affiche le message
        tk.Label(
            self.root,
            text=message,
            font=("Arial", 24, "bold"),
            bg="#AED6F1",
            fg="#34495E",
            wraplength=400,
            justify="center"
        ).pack(pady=30)

        # Bouton pour recommencer une nouvelle partie
        tk.Button(
            self.root,
            text="Nouvelle Partie",
            font=("Arial", 20),
            bg="#3498DB",
            fg="white",
            command=self.__create_home_menu  # Retour au menu principal
        ).pack(pady=20)

        # Bouton pour quitter
        tk.Button(
            self.root,
            text="Quitter",
            font=("Arial", 20),
            bg="#E74C3C",
            fg="white",
            command=self.root.quit
        ).pack(pady=20)


    def __save_score(self, elapsed_time, won):
        """Saves the player's score to the score manager."""
        grid_id = f"{self.difficulty}_grid"
        if won:
            self.score_manager.add_score(self.player_name, elapsed_time, self.difficulty, grid_id)

    def __show_hall_of_fame(self):
        """Displays the Hall of Fame, showing the best scores for the current difficulty."""
        hall_of_fame = self.score_manager.get_hall_of_fame(self.difficulty)
        if not hall_of_fame:
            messagebox.showinfo("Hall of Fame", "Aucun score enregistré.")
            return

        score_message = "\n".join(f"{score['player_name']} - {score['elapsed_time']} secondes" for score in hall_of_fame)
        messagebox.showinfo("Hall of Fame", f"--- Hall of Fame ---\n{score_message}")


if __name__ == "__main__":
    root = tk.Tk()
    app = MinesweeperApp(root)
    root.mainloop()
