import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk
import os

# Set the current working directory to the script's directory
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Initialize global variables
offense_icon = "🗡️"  # Sword emoji for offense player
defense_icon = "🛡️"  # Shield emoji for defense player
offense_wins = 0
defense_blocks = 0
current_player = "Offense"
board = [""] * 9
offense_name = ""
defense_name = ""

# Initialize the main window with a more colorful and styled theme
root = tk.Tk()
root.title("Tic Tac Toe")
root.geometry("600x700")

# Function to resize and update the background image
def update_background_image():
    global bg_image_label, bg_image
    width, height = root.winfo_width(), root.winfo_height()
    img = Image.open(bg_image_path)
    img = img.resize((width, height), Image.LANCZOS)
    bg_image = ImageTk.PhotoImage(img)
    bg_image_label.config(image=bg_image)

# Create a label to hold the background image
bg_image_path = "background.png"
bg_image_label = tk.Label(root)
bg_image_label.place(relwidth=1, relheight=1)  # Fill the entire window
update_background_image()  # Initial update

# Bind the resizing of the window to update the background image
root.bind("<Configure>", lambda event: update_background_image())

# Function to handle starting a new game
def start_new_game():
    global offense_name, defense_name, offense_wins, defense_blocks, current_player, board
    offense_name = offense_entry.get()
    defense_name = defense_entry.get()
    if offense_name == "" or defense_name == "":
        messagebox.showerror("Error", "Please enter both player names.")
        return
    offense_wins = 0
    defense_blocks = 0
    current_player = "Offense"
    board = [""] * 9
    for button in buttons:
        button.config(text="", state=tk.NORMAL, bg="#ecf0f1")
    update_score()
    main_frame.pack(fill=tk.BOTH, expand=True)
    name_frame.pack_forget()

def initialize_game():
    global offense_wins, defense_blocks, current_player, board
    offense_wins = 0
    defense_blocks = 0
    current_player = "Offense"
    board = [""] * 9
    for button in buttons:
        button.config(text="", state=tk.NORMAL, bg="#ecf0f1")
    update_score()

def update_score():
    """ Update the score label to show the current scores with player names dynamically adjusted """
    score_label.config(text=f"{offense_name[:15]} (Offense) Wins: {offense_wins}   |   {defense_name[:15]} (Defense) Blocks: {defense_blocks}")

def check_winner(icon):
    win_positions = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]
    for pos in win_positions:
        if board[pos[0]] == board[pos[1]] == board[pos[2]] == icon:
            return True
    return False

def check_full():
    return all(cell in [offense_icon, defense_icon] for cell in board)

def on_button_click(index):
    global current_player, offense_wins, defense_blocks

    if current_player == "Offense":
        icon = offense_icon
    else:
        icon = defense_icon

    if board[index] == "":
        buttons[index].config(text=icon, state=tk.DISABLED, disabledforeground="black")
        board[index] = icon

        if check_winner(icon):
            if current_player == "Offense":
                offense_wins += 1
                messagebox.showinfo("Result", f"{offense_name} wins this round!")
            else:
                messagebox.showinfo("Result", f"This round is a draw! {defense_name} wins with three in a row.")
            reset_board()
        elif check_full():
            defense_blocks += 1
            messagebox.showinfo("Result", f"{defense_name} blocks this round!")
            reset_board()
        else:
            current_player = "Defense" if current_player == "Offense" else "Offense"
            update_background_color()
            update_score()

    if offense_wins == 3:
        messagebox.showinfo("Game Over", f"{offense_name} wins the game!")
        initialize_game()
    elif defense_blocks == 3:
        messagebox.showinfo("Game Over", f"{defense_name} wins the game!")
        initialize_game()

def reset_board():
    global board
    board = [""] * 9
    for button in buttons:
        button.config(text="", state=tk.NORMAL, bg="#ecf0f1")
    update_background_color()
    update_score()

def update_background_color():
    """Change the background color to indicate the current player's turn."""
    if current_player == "Offense":
        root.configure(bg="#34495e")
    else:
        root.configure(bg="#d35400")

# Create the GUI layout with enhanced design
name_frame = tk.Frame(root, padx=20, pady=20, bg='#34495e')
tk.Label(name_frame, text="Enter Player Names", font=("Helvetica", 18, 'bold'), fg='#ecf0f1', bg='#34495e').pack(pady=(0, 10))

tk.Label(name_frame, text="Offense Player Name: ", font=("Helvetica", 14), fg='#ecf0f1', bg='#34495e').pack()
offense_entry = tk.Entry(name_frame, font=("Helvetica", 14))
offense_entry.pack(pady=(0, 10))

tk.Label(name_frame, text="Defense Player Name: ", font=("Helvetica", 14), fg='#ecf0f1', bg='#34495e').pack()
defense_entry = tk.Entry(name_frame, font=("Helvetica", 14))
defense_entry.pack(pady=(0, 10))

start_button = tk.Button(name_frame, text="Start Game", font=("Helvetica", 14, 'bold'), bg="#1abc9c", fg='#ffffff', activebackground="#16a085", command=start_new_game)
start_button.pack(pady=(20, 0))

name_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

main_frame = tk.Frame(root, bg='#34495e')
score_label = tk.Label(main_frame, text="", font=("Helvetica", 16, 'bold'), fg='#ecf0f1', bg='#34495e')
score_label.pack(pady=(0, 20))

frame = tk.Frame(main_frame, bg='#34495e')
frame.pack()

buttons = []
for i in range(9):
    button = tk.Button(frame, text="", font=("Segoe UI Emoji", 24, 'bold'), width=5, height=2,
                       command=lambda i=i: on_button_click(i), bg="#ecf0f1", activebackground="#95a5a6", relief=tk.RAISED, bd=3)
    button.grid(row=i//3, column=i%3, padx=5, pady=5)
    buttons.append(button)

initialize_game_button = tk.Button(main_frame, text="Restart Game", font=("Helvetica", 14, 'bold'), bg="#e74c3c", fg='#ffffff', activebackground="#c0392b", command=initialize_game)
initialize_game_button.pack(pady=10)

update_score()
update_background_color()

# Start the game loop
root.mainloop()
