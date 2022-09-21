from tkinter import *
import os
import math
abspath = os.path.abspath(__file__)
dname = os.path.dirname(abspath)
os.chdir(dname)
# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"
RED = "#e7305b"
GREEN = "#9bdeac"
YELLOW = "#f7f5dd"
FONT_NAME = "Courier"
WORK_MIN = 25
SHORT_BREAK_MIN = 5
LONG_BREAK_MIN = 20
reps = 0
timer = None #global variable used for setting time 
# ---------------------------- TIMER RESET ------------------------------- # 
def reset_timer():
    global timer
    root.after_cancel(timer) #stops timer 
    tick.config(text = "") #sets ticks to blank 
    canvas.itemconfig(timer_text, text = "00:00")
    timer_label.config(text = "Timer", fg = GREEN)
    global reps 
    reps = 0 #resets reps



# ---------------------------- TIMER MECHANISM ------------------------------- # 
def start_timer():
    global reps
    reps +=1 
    if reps % 2 != 0: #checks if need 25 min counter 
        time_in_seconds = WORK_MIN * 60
        timer_label.config(text = "Work")
    elif reps % 8 == 0: #checks if on 4th break
        time_in_seconds = LONG_BREAK_MIN * 60
        timer_label.config(text = "Long break", fg = PINK)
    else: #checks if on 1st, 2nd, or 3rd break
        time_in_seconds = SHORT_BREAK_MIN * 60
        timer_label.config(text = "Short break", fg = RED)

    count_down(time_in_seconds)
# ---------------------------- COUNTDOWN MECHANISM ------------------------------- # 
def count_down(count):
    if count >= 0:
        minutes = math.floor(count / 60) #rounds number down 
        if minutes <10:
            minutes = f"0{minutes}" 
        seconds = count % 60
        if seconds < 10:
            seconds = f"0{seconds}"
        global timer
        timer = root.after(1000, count_down, count-1) #repeatedly calls self whilst counting down
        canvas.itemconfig(timer_text, text = f"{minutes}:{seconds}")

    elif count < 0:
        global reps
        if reps % 2 != 0:
            ticks = tick.cget("text")
            ticks += "✔"
            tick.config(text = ticks)
        start_timer()
        


# ---------------------------- UI SETUP ------------------------------- #
root = Tk()
root.title("Pomodoro Timer")
root.config(padx = 100, pady =50, bg = YELLOW)
root.columnconfigure(1, minsize=300)


#create canvas widget with tomato image 
canvas = Canvas(width = 200, height = 224, bg = YELLOW, ) #highlightthickness prevents border between canvas & main window
tomato_image = PhotoImage(file = "tomato.png")
canvas.create_image(100, 112, image= tomato_image )
timer_text = canvas.create_text(100, 130, text = "00:00", fill = "white", font = (FONT_NAME, 35, "bold"))
canvas.grid(row = 1, column=1)

#Add timer label
timer_label = Label(text = "Timer", font = (FONT_NAME, 30, "bold"), bg = YELLOW, fg = GREEN)
timer_label.grid(row =0, column = 1, columnspan=2)

#add start & reset buttons
start = Button(text = "Start", command = start_timer)
start.grid(row = 2, column = 0)

reset = Button(text = "Reset", command = reset_timer)
reset.grid(row = 2, column = 2)

#add tick (denotes number of work sessions completed)
tick = Label(text = "", font = (FONT_NAME, 10, "bold"), bg=YELLOW, fg=GREEN) #text is added at end of work countdown
tick.grid(row = 3, column = 1)


#initialse tkinter window 
root.mainloop()


try:
            with open("data.txt", mode = "r") as high_score:
                self.high_score = int(high_score.read())
except FileNotFoundError: #if file does not exist, create file with default highscore value
            with open("data.txt", mode = "w") as high_score:
                high_score.write("0")
            with open("data.txt", mode = "r") as high_score:
                self.high_score = int(high_score.read())
