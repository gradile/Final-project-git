import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import io
import requests

API_KEY = 'b842877a99171f6d11bfc64a15bf0c1b'
BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

# Store the latest weather result globally for saving
weather_result = ""

def get_weather():
    global weather_result

    city = city_entry.get()
    unit = unit_var.get()
    if unit == "Celsius":
        units = "metric"
    else:
        units = "imperial"

    params = {
        "q": city,
        "appid": API_KEY,
        "units": units
    }

    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()

        city_name = data['name']
        temp = data['main']['temp']
        feels_like = data['main']['feels_like']
        weather = data['weather'][0]['description']
        icon_code = data['weather'][0]['icon']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']
        unit_symbol = "°C" if units == "metric" else "°F"

        # Compose weather result
        weather_result = (
            f"Weather in {city_name}:\n"
            f"Temperature: {temp}{unit_symbol}\n"
            f"Feels like: {feels_like}{unit_symbol}\n"
            f"Description: {weather}\n"
            f"Humidity: {humidity}%\n"
            f"Wind Speed: {wind_speed} m/s"
        )

        output_label.config(text=weather_result)

        # Load and display icon
        icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
        icon_response = requests.get(icon_url)
        image_data = icon_response.content
        image = Image.open(io.BytesIO(image_data))
        photo = ImageTk.PhotoImage(image)

        icon_label.image = photo  # prevent image from being garbage collected
        icon_label.config(image=photo)

    except requests.exceptions.HTTPError:
        messagebox.showerror("Error", "City not found or API error.")
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Network error: {e}")

def save_to_file():
    if not weather_result:
        messagebox.showinfo("Info", "Please get weather data first.")
        return
    try:
        with open("weather_report.txt", "w") as file:
            file.write(weather_result)
        messagebox.showinfo("Saved", "Weather data saved to 'weather_report.txt'")
    except Exception as e:
        messagebox.showerror("Error", f"Could not save file: {e}")

# Setup GUI
root = tk.Tk()
root.title("🌦️ Weather App")
root.geometry("420x380")

frame = tk.Frame(root, bg="#e6f2ff", padx=20, pady=20, bd=3, relief="groove")
frame.pack(expand=True)

# City input
ttk.Label(frame, text="Enter City:").grid(row=0, column=0, sticky="w")
city_entry = ttk.Entry(frame, width=30)
city_entry.grid(row=0, column=1, padx=10, pady=5)

# Unit selector
unit_var = tk.StringVar(value="Celsius")
ttk.Label(frame, text="Unit:").grid(row=1, column=0, sticky="w")
unit_menu = ttk.Combobox(frame, textvariable=unit_var, values=["Celsius", "Fahrenheit"], state="readonly")
unit_menu.grid(row=1, column=1, padx=10, pady=5)

# Button to get weather
search_button = ttk.Button(frame, text="Get Weather", command=get_weather)
search_button.grid(row=2, column=0, columnspan=2, pady=10)

# Frame to hold icon and weather text
result_frame = tk.Frame(frame, bg="#f0f0ff", bd=2, relief="ridge")
result_frame.grid(row=3, column=0, columnspan=2, pady=10)

icon_label = tk.Label(result_frame)
icon_label.pack(side="left", padx=10)

# output_label = tk.Label(result_frame, text="", justify="left", anchor="w", wraplength=250, font=("Segoe UI Emoji", 10))
output_label = tk.Label(
    result_frame,
    text="",
    justify="left",
    anchor="w",
    wraplength=250,
    font=("Segoe UI", 12, "bold"),   # Font family, size, and weight
    fg="#333366",                    # Text color
    bg="#f0f0ff",                    # Background color
    padx=10,
    pady=10
)
output_label.pack(side="left")

# Save to file button
save_button = ttk.Button(frame, text="Save to File", command=save_to_file)
save_button.grid(row=4, column=0, columnspan=2, pady=10)

root.mainloop()