import ttkbootstrap as tb
from tkinter import StringVar, IntVar, messagebox
from plyer import notification

class PomodoroApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🍅 Pomodoro Timer")
        self.root.geometry("400x500")
        self.root.resizable(False, False)

        # Variables
        self.session_count = IntVar(value=0)
        self.timer_running = False
        self.work_time = IntVar(value=25)  # Default 25 min
        self.break_time = IntVar(value=5)   # Default 5 min
        self.time_left = self.work_time.get() * 60

        # UI Elements
        tb.Label(root, text="🍅 Pomodoro Timer", font="Arial 18 bold").pack(pady=10)

        self.time_display = tb.Label(root, text="25:00", font="Arial 24 bold")
        self.time_display.pack(pady=10)

        self.status_label = tb.Label(root, text="Work Session", font="Arial 14")
        self.status_label.pack(pady=5)

        # Time input fields
        tb.Label(root, text="Work Time (min):").pack()
        self.work_entry = tb.Entry(root, textvariable=self.work_time, width=5)
        self.work_entry.pack(pady=5)

        tb.Label(root, text="Break Time (min):").pack()
        self.break_entry = tb.Entry(root, textvariable=self.break_time, width=5)
        self.break_entry.pack(pady=5)

        # Buttons
        self.start_button = tb.Button(root, text="▶ Start", bootstyle="success", command=self.start_timer)
        self.start_button.pack(pady=5)

        self.stop_button = tb.Button(root, text="⏹ Stop", bootstyle="danger", command=self.stop_timer)
        self.stop_button.pack(pady=5)

        tb.Label(root, text="🍅 Sessions Completed:").pack(pady=5)
        self.session_label = tb.Label(root, textvariable=self.session_count, font="Arial 14")
        self.session_label.pack(pady=5)

    def validated_input(self):
        try:
            work_time = int(self.work_entry.get())
            break_time = int(self.break_entry.get())
            if work_time <= 0 or break_time <= 0:
                raise ValueError
            return work_time, break_time
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid positive numbers for work and break times.")
            return None, None

    def start_timer(self):
        """Start the Pomodoro timer with user-defined times."""
        if not self.timer_running:
            self.timer_running = True
            self.time_left = self.work_time.get() * 60  # Get updated time from input
            self.run_timer()

    def stop_timer(self):
        """Stop the timer."""
        self.timer_running = False

    def reset_timer(self):
        self.timer_running = False
        self.time_left = self.work_time.get() * 60
        self.time_display.comfig(text=f'{self.work_time.get():02d}:00')
        self.status_label.config(text='work session')

    def run_timer(self):
        """Run the countdown timer."""
        if self.timer_running and self.time_left > 0:
            mins, secs = divmod(self.time_left, 60)
            self.time_display.config(text=f"{mins:02d}:{secs:02d}")
            self.time_left -= 1
            self.root.after(1000, self.run_timer)
        else:
            self.timer_end()

    def timer_end(self):
        """Handle what happens when the timer reaches 0."""
        if self.timer_running:
            self.timer_running = False
            if self.status_label.cget("text") == "Work Session":
                self.session_count.set(self.session_count.get() + 1)
                notification.notify(title="⏳ Time's Up!", message="Take a break!", timeout=5)
                self.status_label.config(text="Break Time")
                self.time_left = self.break_time.get() * 60  # Get updated break time
            else:
                notification.notify(title="✅ Back to Work!", message="Start another Pomodoro session!", timeout=5)
                self.status_label.config(text="Work Session")
                self.time_left = self.work_time.get() * 60  # Get updated work time
            self.start_timer()

    def send_notification(self,title,message):
        notification.notify(title=title, message=message, timeout=5)

# Run the App
root = tb.Window(themename="superhero")
app = PomodoroApp(root)
root.mainloop()
