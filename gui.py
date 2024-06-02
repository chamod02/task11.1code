import tkinter as tk
from tkinter import messagebox
from main import control_pump, get_latest_data, should_water, MOISTURE_THRESHOLD_LOW

# Function to manually water the plants
def manual_water():
    try:
        duration = int(duration_entry.get())
        control_pump(True, duration)
        messagebox.showinfo("Manual Watering", f"Watered plants for {duration} seconds")
    except ValueError:
        messagebox.showerror("Input Error", "Please enter a valid number for duration")

# Function to update thresholds
def update_thresholds():
    global MOISTURE_THRESHOLD_LOW
    try:
        MOISTURE_THRESHOLD_LOW = int(moisture_threshold_entry.get())
        messagebox.showinfo("Threshold Update", "Threshold values updated successfully")
    except ValueError:
        messagebox.showerror("Input Error", "Please enter a valid number for the moisture threshold")

# Function to check and water automatically
def auto_water():
    data = get_latest_data()
    if data:
        temperature, humidity, soil_moisture, sunlight = data
        action, duration = should_water(temperature, humidity, soil_moisture, sunlight)
        control_pump(action, duration)
        messagebox.showinfo("Auto Watering", f"Auto watering check completed. Action: {'Watered' if action else 'Not Watered'}")

# Create the GUI
root = tk.Tk()
root.title("Irrigation System Control")

# Threshold Controls
tk.Label(root, text="Moisture Threshold:").grid(row=0, column=0)
moisture_threshold_entry = tk.Entry(root)
moisture_threshold_entry.grid(row=0, column=1)
moisture_threshold_entry.insert(0, str(MOISTURE_THRESHOLD_LOW))

tk.Button(root, text="Update Thresholds", command=update_thresholds).grid(row=1, columnspan=2)

# Manual Control
tk.Label(root, text="Manual Watering Duration (seconds):").grid(row=2, column=0)
duration_entry = tk.Entry(root)
duration_entry.grid(row=2, column=1)
duration_entry.insert(0, "10")

tk.Button(root, text="Manual Water", command=manual_water).grid(row=3, columnspan=2)

# Auto Control
tk.Button(root, text="Check and Auto Water", command=auto_water).grid(row=4, columnspan=2)

# Start the GUI
root.mainloop()