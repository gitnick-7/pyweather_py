import tkinter as tk
from tkinter import messagebox
import requests
from PIL import Image, ImageTk 
import io
from datetime import datetime


API_KEY = "a7c717748563576cbf587bfdb40e3156"  
BASE_URL = "http://api.openweathermap.org/data/2.5/weather?"

def get_weather():
    city = city_entry.get()
    if not city:
        messagebox.showwarning("Warning", "Please enter a city name.")
        return

    url = f"{BASE_URL}q={city}&appid={API_KEY}&units=metric"

    try:
        response = requests.get(url)
        data = response.json()

        if response.status_code == 200:
            update_ui(data)
        elif response.status_code == 404:
            messagebox.showerror("Error", "City not found.")
        else:
            messagebox.showerror("Error", "Unable to fetch data.")

    except requests.exceptions.RequestException:
        messagebox.showerror("Error", "No internet connection.")

def update_ui(data):
    """Parses JSON data and updates the GUI elements."""
    
    
    city_name = data['name']
    country = data['sys']['country']
    temp = data['main']['temp']
    feels_like = data['main']['feels_like']
    humidity = data['main']['humidity']
    wind_speed = data['wind']['speed']
    desc = data['weather'][0]['description'].title()
    icon_code = data['weather'][0]['icon']
    
    
    sunrise = datetime.fromtimestamp(data['sys']['sunrise']).strftime('%H:%M')
    sunset = datetime.fromtimestamp(data['sys']['sunset']).strftime('%H:%M')

    
    location_label.config(text=f"{city_name}, {country}")
    temp_label.config(text=f"{int(temp)}°C")
    feels_label.config(text=f"Feels like {int(feels_like)}°C")
    desc_label.config(text=desc)
    stats_label.config(text=f"💧 Humidity: {humidity}%  |  💨 Wind: {wind_speed} m/s\n☀️ Rise: {sunrise}  |  🌑 Set: {sunset}")

    
    icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
    try:
        raw_data = requests.get(icon_url).content
        image = Image.open(io.BytesIO(raw_data))
        photo = ImageTk.PhotoImage(image)
        
        icon_label.config(image=photo)
        icon_label.image = photo 
    except:
        icon_label.config(image='', text="[No Icon]")

    
    if "rain" in desc.lower() or "drizzle" in desc.lower():
        bg_color = "#3568a1" 
    elif "clear" in desc.lower():
        bg_color = "#c2a92a" 
    elif "cloud" in desc.lower():
        bg_color = "#38a6ad" 
    else:
        bg_color = "#d69bd6"
        
    root.configure(bg=bg_color)
    for widget in root.winfo_children():
        widget.configure(bg=bg_color)
    
    
    city_entry.configure(bg="white")
    search_btn.configure(bg="#1ec25d")



root = tk.Tk()
root.title("Pro Weather App")
root.geometry("400x550")
root.configure(bg="white")


search_frame = tk.Frame(root, bg="white")
search_frame.pack(pady=20)

city_entry = tk.Entry(search_frame, font=("Arial", 14), width=20, justify='center', bg="#f0f0f0", bd=0)
city_entry.grid(row=0, column=0, ipady=5, padx=5)
city_entry.focus()

search_btn = tk.Button(search_frame, text="🔍", command=get_weather, font=("Arial", 12), bg="#4a90e2", fg="white", width=4, relief='flat')
search_btn.grid(row=0, column=1, padx=5)


icon_label = tk.Label(root, bg="white")
icon_label.pack()

location_label = tk.Label(root, text="Enter City", font=("Arial", 22, "bold"), bg="white", fg="#333")
location_label.pack()

temp_label = tk.Label(root, text="--°C", font=("Arial", 50, "bold"), bg="white", fg="#333")
temp_label.pack()

feels_label = tk.Label(root, text="Feels like --°C", font=("Arial", 12), bg="white", fg="#666")
feels_label.pack()

desc_label = tk.Label(root, text="---", font=("Arial", 16, "italic"), bg="white", fg="#444")
desc_label.pack(pady=5)

stats_label = tk.Label(root, text="", font=("Consolas", 10), bg="white", fg="#555", justify="center")
stats_label.pack(pady=20)


root.bind('<Return>', lambda event: get_weather())

root.mainloop()