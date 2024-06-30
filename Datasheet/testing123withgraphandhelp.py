import serial
import tkinter as tk
from tkinter import ttk, messagebox
from tkinter import filedialog
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from PIL import Image, ImageTk


# Serial communication settings
ARDUINO_PORT = 'COM3'  # Update with the correct port
BAUD_RATE = 9600

# GUI settings
FONT = ('Arial', 14)
FAN_STATUS_TEXT = {
    0: 'OFF',
    1: 'ON'
}

# Create a serial connection to Arduino
arduino = serial.Serial(ARDUINO_PORT, BAUD_RATE, timeout=1)

# Create the GUI window
window = tk.Tk()
window.title("Fan Controlling System")
window.geometry('800x800')
#window.resizable(width=False, height=False)
window.configure(bg='lavender')
window.iconbitmap("fan.ico")

# Create a label for the title
title_label = tk.Label(window, text="Fan Controlling System [Project] | IA3204- Data Acquisition Systems", font=('Times New Roman', 15, 'bold'), bg='lavender')
title_label.pack(pady=20)


# Function to show the help message
def show_help():
    instructions = "Instructions:\n\n" \
                   "1. Temperature Sensing Mode: Select this mode to automatically control the fans based on temperature.\n\n" \
                   "2. Manual Control Mode: Select this mode to manually control the fans.\n\n" \
                   "   - Fan ON: Click this button to turn on the fans.\n" \
                   "   - Fan OFF: Click this button to turn off the fans."
    messagebox.showinfo("Help", instructions)


# Prepare the icon image
icon_path = 'icon.png'  # Replace with the path to your icon image

# Load the icon image
icon_image = Image.open(icon_path)
icon_image = icon_image.resize((25, 25))  # Resize the image if needed
icon_photo = ImageTk.PhotoImage(icon_image)


# Create a label to display the temperature
temperature_label = tk.Label(window, font=FONT)
temperature_label.configure(bg='yellow')
temperature_label.pack(pady=20)

# Create a label to display the fan status
fan_labels = []
fan_pins = ["FAN 1", "FAN 2", "FAN 3", "FAN 4", "FAN 5"]

for pin in fan_pins:
    label = tk.Label(window, text=pin + ": ", bg="lightyellow", relief="groove", borderwidth=2, padx=10, pady=5)
    label.pack(expand=True, padx=10, pady=5)
    fan_labels.append(label)
    
# Create a file for data logging
LOG_FILE_PATH = "data_log.csv"
with open(LOG_FILE_PATH, "a") as log_file:
    if log_file.tell() == 0:  # Check if the file is empty
        log_file.write("Timestamp, Temperature, Fan 1, Fan 2, Fan 3, Fan 4, Fan 5\n")

# Function to save the logged data to a file
def save_data():
    log_data = ""
    with open(LOG_FILE_PATH, "r") as log_file:
        log_data = log_file.read()

    # Prompt the user to select the file location to save the data
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
    if file_path:
        with open(file_path, "w") as save_file:
            save_file.write(log_data)
        messagebox.showinfo("Data Saved", "Data has been saved to {}".format(file_path))


# Function to read the temperature from Arduino
def read_temperature():
    temperature_data = arduino.readline().decode().strip()
    temperature = temperature_data.split(": ")[-1].split("°")[0]
    return temperature


# Create a figure and subplot for the temperature graph
figure = Figure(figsize=(5,4), dpi=80)
subplot = figure.add_subplot(1, 1, 1)
subplot.set_xlabel("Time")
subplot.set_ylabel("Temperature(°C)")


# Create a canvas to display the temperature graph
canvas = FigureCanvasTkAgg(figure, master=window)
canvas.get_tk_widget().pack()

# Lists to store time and temperature data
time_data = []
temperature_data = []


# Function to update the temperature and fan status labels
def update_labels():
    temperature = read_temperature()
    temperature_label.config(text="Temperature: {}°C".format(temperature), image=icon_photo, compound='left')

    # Append current time and temperature to the data lists
    current_time = len(time_data)
    time_data.append(current_time)
    temperature_data.append(float(temperature))

    # Update the temperature graph
    subplot.clear()
    subplot.plot(time_data, temperature_data)
    canvas.draw()

    arduino.write(b"G")  # Send request for fan status to Arduino
    fan_status_data = arduino.readline().decode().strip()

    if fan_status_data:
        fan_status = [int(status) for status in fan_status_data.split(",")]

        for index, pin in enumerate(fan_pins):
            status_text = FAN_STATUS_TEXT.get(fan_status[index], "Unknown")
            fan_labels[index].config(text=pin + ": " + status_text)

    # Log the data to the file
    log_data = "{}, {}, {}, {}, {}, {}, {}\n".format(
        current_time, temperature, fan_status[0], fan_status[1], fan_status[2], fan_status[3], fan_status[4]
    )
    with open(LOG_FILE_PATH, "a") as log_file:
        log_file.write(log_data)
    window.after(2000, update_labels)  # Update every 2 seconds


# Function to handle the manual control buttons
def manual_control(fan_status):
    if fan_status:
        arduino.write(b'1')  # Send command to turn on fans
    else:
        arduino.write(b'0')  # Send command to turn off fans


# Function to switch to temperature sensing mode
def temperature_sensing_mode():
    arduino.write(b'T')  # Send command to switch to temperature sensing mode


# Create mode selection buttons
mode_selection_frame = ttk.Frame(window)
mode_selection_frame.pack(pady=20)

mode_var = tk.IntVar()
mode_var.set(0)

temperature_mode_button = ttk.Radiobutton(mode_selection_frame, text="Temperature Sensing Mode", variable=mode_var,value=0, command=temperature_sensing_mode)
temperature_mode_button.grid(row=0, column=0, padx=10)

manual_mode_button = ttk.Radiobutton(mode_selection_frame, text="Manual Control Mode", variable=mode_var, value=1,command=lambda: manual_control(False))
manual_mode_button.grid(row=0, column=1, padx=10)

# Create manual control buttons
manual_control_frame = ttk.Frame(window)
manual_control_frame.pack(pady=10)

fan_status = tk.IntVar()
fan_status.set(0)

fan_on_button = ttk.Radiobutton(manual_control_frame, text="Fan ON", variable=fan_status, value=1,command=lambda: manual_control(True))
fan_on_button.grid(row=0, column=0, padx=10)

fan_off_button = ttk.Radiobutton(manual_control_frame, text="Fan OFF", variable=fan_status, value=0,command=lambda: manual_control(False))
fan_off_button.grid(row=0, column=1, padx=10)


# Function to show the help message to mode selection
def show_help():
    instructions = "Instructions:\n\n" \
                   "1. Temperature Sensing Mode: Select this mode to automatically control the fans based on temperature.\n\n" \
                   "2. Manual Control Mode: Select this mode to manually control the fans.\n\n" \
                   "   - Fan ON: Click this button to turn on the fans.\n" \
                   "   - Fan OFF: Click this button to turn off the fans."
    messagebox.showinfo("Help", instructions)
    
# Function to show the help message to download data
def download_data():
    instructions = "Instructions:\n\n" \
                   "Download a report in CSV file format that includes temperature variation with time and the corresponding fan status for each case"
    messagebox.showinfo("Help", instructions)


# Create the menu bar
menu_bar = tk.Menu(window)
window.config(menu=menu_bar)

#Create the "File" menu
file_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="Download Data", command=save_data)

# Create the "Help" menu
help_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Help", menu=help_menu)
help_menu.add_command(label="Select Mode", command=show_help)
help_menu.add_command(label="Download Data", command=download_data)


# Start updating the labels
update_labels()

# Start the GUI event loop
window.mainloop()
