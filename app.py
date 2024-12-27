import mysql.connector
import customtkinter as ctk
from tkinter import messagebox
from PIL import Image, ImageTk

# Database setup
def initialize_db():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="mma_event"
    )
    cursor = conn.cursor()

    # Create Fighters table
    cursor.execute('''CREATE TABLE IF NOT EXISTS Fighters (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        weight_class VARCHAR(255) NOT NULL,
        record VARCHAR(50) NOT NULL
    )''')

    # Create Events table
    cursor.execute('''CREATE TABLE IF NOT EXISTS Events (
        id INT AUTO_INCREMENT PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        date DATE NOT NULL,
        location VARCHAR(255) NOT NULL
    )''')

    # Create Matches table
    cursor.execute('''CREATE TABLE IF NOT EXISTS Matches (
        id INT AUTO_INCREMENT PRIMARY KEY,
        event_id INT,
        fighter1_id INT,
        fighter2_id INT,
        result VARCHAR(255),
        FOREIGN KEY (event_id) REFERENCES Events(id),
        FOREIGN KEY (fighter1_id) REFERENCES Fighters(id),
        FOREIGN KEY (fighter2_id) REFERENCES Fighters(id)
    )''')

    conn.commit()
    conn.close()

# Add Fighter Functionality
def add_fighter(name, weight_class, record):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="mma_event"
    )
    cursor = conn.cursor()
    cursor.execute("INSERT INTO Fighters (name, weight_class, record) VALUES (%s, %s, %s)", (name, weight_class, record))
    conn.commit()
    conn.close()

# Function to add background and logo to any window
def add_background_and_logo(window):
    # Load the background image using PIL
    bg_image = Image.open(r"C:\Users\SHC\Desktop\MMA\MMA Organization AFC Afghan Fighting Championship logo.png")
    bg_image_resized = bg_image.resize((800, 650))  # Resize the image to fit the window
    bg_image = ImageTk.PhotoImage(bg_image_resized)

    # Create a label to display the background image
    bg_label = ctk.CTkLabel(window, image=bg_image)
    bg_label.image = bg_image  # Keep a reference to avoid garbage collection
    bg_label.place(relwidth=1, relheight=1)  # Make it cover the entire window

    # Display the logo image (on top of the background) in the top-right corner
    logo_image = Image.open(r"C:\Users\SHC\Desktop\MMA\MMA Organization AFC Afghan Fighting Championship logo.png")
    logo_image_resized = logo_image.resize((180, 90))  # Resize the logo smaller
    logo_image = ImageTk.PhotoImage(logo_image_resized)

    logo_label = ctk.CTkLabel(window, image=logo_image, text="AFC Logo", compound="top", font=("Arial", 16, "bold"))
    logo_label.image = logo_image  # Keep a reference to avoid garbage collection
    logo_label.place(relx=1, rely=0, anchor="ne")  # Position the logo at the top-right corner

    return window

# GUI Setup
def main_gui():
    app = ctk.CTk()
    app.title("AFC Management System")
    app.geometry("800x650")  # Set window size to 800x650
    app.configure(bg='white')  # Optional: Set the main window background to white

    # Add background and logo to the main window
    app = add_background_and_logo(app)

    # Title text below the logo
    title_label = ctk.CTkLabel(app, text="AFC (Afghan Fighting Championship)", font=("Arial", 22, "bold"))
    title_label.place(relx=0.5, rely=0.1, anchor="center")  # Position title above the logo

    # Create a frame to hold the buttons and position them more centrally
    button_frame = ctk.CTkFrame(app)
    button_frame.place(relx=0.5, rely=0.45, anchor="center")  # Position the frame centrally

    menu_options = [
        ("Add Fighter", add_fighter_gui),
        ("Add Event", add_event_gui),
        ("Schedule Match", schedule_match_gui),
        ("View Fighters", view_fighters_gui),
        ("View Events", view_events_gui),
        ("View Matches", view_matches_gui),  # New button to view matches
    ]

    # Create the buttons inside the button frame
    for text, command in menu_options:
        ctk.CTkButton(button_frame, text=text, command=command, width=200, height=40).pack(pady=10)

    # Exit button positioned separately at the bottom of the window
    ctk.CTkButton(app, text="Exit", command=app.quit, width=200, height=40).place(relx=0.5, rely=0.85, anchor="center")

    app.mainloop()

def add_fighter_gui():
    def submit_fighter():
        name = name_entry.get()
        weight_class = weight_class_entry.get()
        win = win_entry.get()
        loss = loss_entry.get()
        draw = draw_entry.get()
        if name and weight_class and win.isdigit() and loss.isdigit() and draw.isdigit():
            record = f"{win}-{loss}-{draw}"
            add_fighter(name, weight_class, record)
            messagebox.showinfo("Success", "Fighter added successfully!")
            add_fighter_window.destroy()
        else:
            messagebox.showerror("Error", "Please provide valid inputs.")

    # Create "Add Fighter" window with background and logo
    add_fighter_window = ctk.CTkToplevel()
    add_fighter_window.title("Add Fighter")
    add_fighter_window.geometry("800x650")  # Set window size to 800x650
    add_fighter_window.attributes('-top', 1)  # Ensure the new window stays on top

    # Add background and logo to the new window
    add_fighter_window = add_background_and_logo(add_fighter_window)

    ctk.CTkLabel(add_fighter_window, text="Fighter Name:").pack(pady=10)
    name_entry = ctk.CTkEntry(add_fighter_window)
    name_entry.pack(pady=10)

    ctk.CTkLabel(add_fighter_window, text="Weight Class:").pack(pady=10)
    weight_class_entry = ctk.CTkEntry(add_fighter_window)
    weight_class_entry.pack(pady=10)

    ctk.CTkLabel(add_fighter_window, text="Wins:").pack(pady=10)
    win_entry = ctk.CTkEntry(add_fighter_window)
    win_entry.pack(pady=10)

    ctk.CTkLabel(add_fighter_window, text="Losses:").pack(pady=10)
    loss_entry = ctk.CTkEntry(add_fighter_window)
    loss_entry.pack(pady=10)

    ctk.CTkLabel(add_fighter_window, text="Draws:").pack(pady=10)
    draw_entry = ctk.CTkEntry(add_fighter_window)
    draw_entry.pack(pady=10)

    # Save button
    ctk.CTkButton(add_fighter_window, text="Save", command=submit_fighter).pack(pady=30)

def view_fighters_gui():
    view_fighters_window = ctk.CTkToplevel()
    view_fighters_window.title("View Fighters")
    view_fighters_window.geometry("800x650")  # Set window size to 800x650
    view_fighters_window.attributes('-top', 1)  # Ensure the new window stays on top

    # Add background and logo to the new window
    view_fighters_window = add_background_and_logo(view_fighters_window)

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="mma_event"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Fighters")
    fighters = cursor.fetchall()
    conn.close()

    if not fighters:
        ctk.CTkLabel(view_fighters_window, text="No fighters found.").pack(pady=20)
    else:
        for fighter in fighters:
            fighter_info = f"ID: {fighter[0]}, Name: {fighter[1]}, Weight Class: {fighter[2]}, Record: {fighter[3]}"
            ctk.CTkLabel(view_fighters_window, text=fighter_info).pack(pady=10)

def add_event_gui():
    def submit_event():
        name = name_entry.get()
        date = date_entry.get()
        location = location_entry.get()
        if name and date and location:
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="mma_event"
            )
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Events (name, date, location) VALUES (%s, %s, %s)", (name, date, location))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Event added successfully!")
            add_event_window.destroy()
        else:
            messagebox.showerror("Error", "Please fill all fields.")

    add_event_window = ctk.CTkToplevel()
    add_event_window.title("Add Event")
    add_event_window.geometry("800x650")  # Set window size to 800x650
    add_event_window.attributes('-top', 1)  # Ensure the new window stays on top

    # Add background and logo to the new window
    add_event_window = add_background_and_logo(add_event_window)

    ctk.CTkLabel(add_event_window, text="Event Name:").pack(pady=10)
    name_entry = ctk.CTkEntry(add_event_window)
    name_entry.pack(pady=10)

    ctk.CTkLabel(add_event_window, text="Event Date (YYYY-MM-DD):").pack(pady=10)
    date_entry = ctk.CTkEntry(add_event_window)
    date_entry.pack(pady=10)

    ctk.CTkLabel(add_event_window, text="Location:").pack(pady=10)
    location_entry = ctk.CTkEntry(add_event_window)
    location_entry.pack(pady=10)

    # Save button
    ctk.CTkButton(add_event_window, text="Save", command=submit_event).pack(pady=30)

def view_events_gui():
    view_events_window = ctk.CTkToplevel()
    view_events_window.title("View Events")
    view_events_window.geometry("800x650")  # Set window size to 800x650
    view_events_window.attributes('-top', 1)  # Ensure the new window stays on top

    # Add background and logo to the new window
    view_events_window = add_background_and_logo(view_events_window)

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="mma_event"
    )
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Events")
    events = cursor.fetchall()
    conn.close()

    if not events:
        ctk.CTkLabel(view_events_window, text="No events found.").pack(pady=20)
    else:
        for event in events:
            event_info = f"ID: {event[0]}, Name: {event[1]}, Date: {event[2]}, Location: {event[3]}"
            ctk.CTkLabel(view_events_window, text=event_info).pack(pady=10)

def view_matches_gui():
    view_matches_window = ctk.CTkToplevel()
    view_matches_window.title("View Matches")
    view_matches_window.geometry("800x650")
    view_matches_window.attributes('-top', 1)

    view_matches_window = add_background_and_logo(view_matches_window)

    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="mma_event"
    )
    cursor = conn.cursor()
    cursor.execute('''SELECT m.id, e.name AS event_name, f1.name AS fighter1_name, f2.name AS fighter2_name, m.result
                      FROM Matches m
                      JOIN Events e ON m.event_id = e.id
                      JOIN Fighters f1 ON m.fighter1_id = f1.id
                      JOIN Fighters f2 ON m.fighter2_id = f2.id''')
    matches = cursor.fetchall()
    conn.close()

    if not matches:
        ctk.CTkLabel(view_matches_window, text="No matches found.").pack(pady=20)
    else:
        for match in matches:
            match_info = f"Match ID: {match[0]}, Event: {match[1]}, Fighters: {match[2]} vs {match[3]}, Result: {match[4]}"
            ctk.CTkLabel(view_matches_window, text=match_info).pack(pady=10)

def schedule_match_gui():
    def submit_match():
        event_id = event_id_entry.get()
        fighter1_id = fighter1_id_entry.get()
        fighter2_id = fighter2_id_entry.get()
        result = result_entry.get()

        if event_id.isdigit() and fighter1_id.isdigit() and fighter2_id.isdigit():
            conn = mysql.connector.connect(
                host="localhost",
                user="root",
                password="",
                database="mma_event"
            )
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Matches (event_id, fighter1_id, fighter2_id, result) VALUES (%s, %s, %s, %s)", 
                           (event_id, fighter1_id, fighter2_id, result))
            conn.commit()
            conn.close()
            messagebox.showinfo("Success", "Match scheduled successfully!")
            schedule_match_window.destroy()
        else:
            messagebox.showerror("Error", "Please enter valid match details.")

    schedule_match_window = ctk.CTkToplevel()
    schedule_match_window.title("Schedule Match")
    schedule_match_window.geometry("800x650")  # Set window size to 800x650
    schedule_match_window.attributes('-top', 1)  # Ensure the new window stays on top

    # Add background and logo to the new window
    schedule_match_window = add_background_and_logo(schedule_match_window)

    ctk.CTkLabel(schedule_match_window, text="Event ID:").pack(pady=10)
    event_id_entry = ctk.CTkEntry(schedule_match_window)
    event_id_entry.pack(pady=10)

    ctk.CTkLabel(schedule_match_window, text="Fighter 1 ID:").pack(pady=10)
    fighter1_id_entry = ctk.CTkEntry(schedule_match_window)
    fighter1_id_entry.pack(pady=10)

    ctk.CTkLabel(schedule_match_window, text="Fighter 2 ID:").pack(pady=10)
    fighter2_id_entry = ctk.CTkEntry(schedule_match_window)
    fighter2_id_entry.pack(pady=10)

    ctk.CTkLabel(schedule_match_window, text="Result:").pack(pady=10)
    result_entry = ctk.CTkEntry(schedule_match_window)
    result_entry.pack(pady=10)

    # Save button
    ctk.CTkButton(schedule_match_window, text="Save", command=submit_match).pack(pady=30)

# Main function to initialize the application
if __name__ == "__main__":
    initialize_db()
    main_gui()
#freeview