import random
import turtle
import tkinter as tk
from tkinter import simpledialog, messagebox
import pygame

# Initialize pygame mixer
pygame.mixer.init()

# Load background music
pygame.mixer.music.load("allgame.mp3")  # Path to your music file
pygame.mixer.music.set_volume(0.1)  # Set volume (0.0 to 1.0)

# Load sound effects
beep_sound = pygame.mixer.Sound("ding.mp3")  # Path to your beep sound file
beep_sound.set_volume(0.1)

sad_sound = pygame.mixer.Sound("lose.mp3")  # Path to your sad sound file
sad_sound.set_volume(0.1)

game_over_sound = pygame.mixer.Sound("endingsound.mp3")  # Path to your game over sound file
game_over_sound.set_volume(0.1)

# Create the main screen
screen = turtle.Screen()
screen.title("Turtle Game")
screen.setup(width=600, height=600)

# Initialize game variables
game_over = False
score = 0
FONT = ('Arial', 20, 'normal')

# Create turtle objects
turtle_list = []
count_down_turtle = turtle.Turtle()
score_turtle = turtle.Turtle()

def setup_score_turtle():
    score_turtle.hideturtle()
    score_turtle.color("blue")
    score_turtle.penup()
    top_height = screen.window_height() / 2
    y = top_height - top_height / 10
    score_turtle.setposition(0, y)
    score_turtle.write(arg='Score: 0', move=False, align='center', font=FONT)

grid_size = 10

def make_turtle(x, y):
    t = turtle.Turtle()

    def handle_click(x, y):
        global score, game_over, interval
        if t.fillcolor() == "red":
            game_over = True
            hide_turtles()
            count_down_turtle.clear()
            count_down_turtle.write("Game Over!", align='center', font=FONT)
            pygame.mixer.music.stop()  # Stop the background music
            sad_sound.play()  # Play sad sound for game over
            stop_countdown()  # Stop the countdown
            stop_turtle_display()  # Stop the turtle display timer
            show_restart_button()  # Show the restart button
        else:
            if not game_over:
                score += 1
                score_turtle.clear()
                score_turtle.write("Score: {}".format(score), move=False, align="center", font=FONT)
                beep_sound.play()  # Play beep sound when turtle is clicked

    t.onclick(handle_click)
    t.penup()
    t.shape("turtle")
    t.shapesize(2, 2)
    t.color("green")
    t.goto(x * grid_size, y * grid_size)
    t.pendown()
    turtle_list.append(t)

x_coordinates = [-20, -10, 0, 10, 20]
y_coordinates = [20, 10, 0, -10]

def setup_turtles():
    for x in x_coordinates:
        for y in y_coordinates:
            make_turtle(x, y)

def hide_turtles():
    for t in turtle_list:
        t.hideturtle()

def show_turtles_randomly():
    if not game_over:
        hide_turtles()
        selected_turtle = random.choice(turtle_list)
        selected_turtle.showturtle()

        # Randomly make some turtles red
        if random.random() < 0.2:  # 20% chance to become red
            selected_turtle.color("red")
        else:
            selected_turtle.color("green")

        global turtle_display_timer
        turtle_display_timer = screen.ontimer(show_turtles_randomly, interval)

def countdown(time):
    global game_over
    top_height = screen.window_height() / 2
    y = top_height - top_height / 10
    count_down_turtle.hideturtle()
    count_down_turtle.penup()
    count_down_turtle.setposition(0, y - 30)
    count_down_turtle.clear()

    if time > 0:
        if not game_over:  # Only update countdown if game is not over
            count_down_turtle.write("Time: {}".format(time), move=False, align="center", font=FONT)
            screen.ontimer(lambda: countdown(time - 1), 1000)
    else:
        if not game_over:
            game_over = True
            count_down_turtle.clear()
            hide_turtles()
            count_down_turtle.write("Game Over!", align='center', font=FONT)
            game_over_sound.play()  # Play game over sound
            show_restart_button()  # Show the restart button

def start_game_up(game_time):
    global game_over
    global interval
    global score
    global turtle_display_timer
    game_over = False
    score = 0
    turtle.tracer(0)
    setup_score_turtle()
    setup_turtles()
    hide_turtles()
    show_turtles_randomly()
    turtle.tracer(1)
    screen.ontimer(lambda: countdown(game_time), 10)
    pygame.mixer.music.play(-1)  # Start background music

def stop_countdown():
    turtle.ontimer(lambda: None, 1000)  # No-op timer to stop countdown

def stop_turtle_display():
    global turtle_display_timer
    if turtle_display_timer:
        screen.ontimer(lambda: None, turtle_display_timer)

def prompt_for_difficulty():
    global interval
    root = tk.Tk()
    root.withdraw()  # Hide the main window
    difficulty = simpledialog.askstring("Select Difficulty", "Enter difficulty (easy, medium, hard):").lower()

    if difficulty == 'easy':
        interval = 1000  # 1 second
    elif difficulty == 'medium':
        interval = 700  # 0.7 seconds
    elif difficulty == 'hard':
        interval = 400  # 0.4 seconds
    else:
        messagebox.showerror("Error", "Invalid difficulty level!")
        root.destroy()
        return prompt_for_difficulty()

    root.destroy()  # Close the tkinter root window
    start_game_up(30)  # Start game with 30 seconds timer

def show_restart_button():
    restart_window = tk.Tk()
    restart_window.title("Game Over")
    restart_window.geometry("200x100")

    def restart_game():
        restart_window.destroy()
        prompt_for_difficulty()

    restart_button = tk.Button(restart_window, text="Restart", command=restart_game)
    restart_button.pack(expand=True)

    restart_window.mainloop()

# Initialize global variable for turtle display timer
turtle_display_timer = None

# Prompt user for difficulty and start the game
prompt_for_difficulty()

# Keep the turtle window open
turtle.mainloop()
