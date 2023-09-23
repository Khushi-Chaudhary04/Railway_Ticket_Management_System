import os
import tkinter as tk
from tkinter import ttk
import pandas as pd
import csv
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tempfile

def display_train_schedule():
    train_schedule_window = tk.Toplevel(root)
    train_schedule_window.title("Train Schedule")
    
    train_schedule = pd.read_csv("C:\\Users\\lenovo\\Desktop\\RTMS\\Train schedule.csv")
    
    text_widget = tk.Text(train_schedule_window, wrap=tk.WORD, width=50, height=20)
    text_widget.insert(tk.END, train_schedule.to_string(index=False))
    text_widget.pack()

def check_availability_by_destination():
    availability_window = tk.Toplevel(root)
    availability_window.title("Availability by Destination")
    
    label = tk.Label(availability_window, text="Enter Your Destination:")
    label.pack()
    
    destination_entry = tk.Entry(availability_window)
    destination_entry.pack()
    
    result_text = tk.Text(availability_window, wrap=tk.WORD, width=50, height=10)
    result_text.pack()
    
    def check_availability():
        destination = destination_entry.get()
        with open("C:\\Users\\lenovo\\Desktop\\RTMS\\Train schedule.csv", 'r', newline='\r\n') as file:
            reader = csv.reader(file)
            availability_info = []
            for rec in reader:
                if rec[2] == destination:
                    availability_info.append(f"TRAIN NO: {rec[0]}, TRAIN NAME: {rec[1]}, DESTINATION: {rec[2]}, DURATION: {rec[3]}")
            result_text.delete(1.0, tk.END)
            result_text.insert(tk.END, "\n".join(availability_info))
    
    check_button = tk.Button(availability_window, text="Check Availability", command=check_availability)
    check_button.pack()

def book_ticket():
    booking_window = tk.Toplevel(root)
    booking_window.title("Booking")
    
    destination_label = tk.Label(booking_window, text="Enter Your Destination:")
    destination_label.pack()
    
    destination_entry = tk.Entry(booking_window)
    destination_entry.pack()
    
    name_label = tk.Label(booking_window, text="Enter Your Name:")
    name_label.pack()
    
    name_entry = tk.Entry(booking_window)
    name_entry.pack()
    
    age_label = tk.Label(booking_window, text="Enter Your Age:")
    age_label.pack()
    
    age_entry = tk.Entry(booking_window)
    age_entry.pack()
    
    gender_label = tk.Label(booking_window, text="Enter Your Gender (M/F):")
    gender_label.pack()
    
    gender_entry = tk.Entry(booking_window)
    gender_entry.pack()
    
    class_label = tk.Label(booking_window, text="Enter Your Seat Class (1AC/2AC/Sleeper):")
    class_label.pack()
    
    class_entry = tk.Entry(booking_window)
    class_entry.pack()
    
    phone_label = tk.Label(booking_window, text="Enter Your Mobile Number:")
    phone_label.pack()
    
    phone_entry = tk.Entry(booking_window)
    phone_entry.pack()

def book_ticket_action():
    destination = destination_entry.get()
    name = name_entry.get()
    age = age_entry.get()
    gender = gender_entry.get()
    seat_class = class_entry.get()
    phone_number = phone_entry.get()

    # Define the path to the CSV file where you want to save the booking details
    csv_file_path = "C:\\Users\\lenovo\\Desktop\\RTMS\\List.csv"

    # Create a list with the booking details
    booking_info = [destination, name, age, gender, seat_class, phone_number]

    # Open the CSV file in append mode and write the booking details
    with open(csv_file_path, 'a', newline='\r\n') as file:
        writer = csv.writer(file)
        writer.writerow(booking_info)

    # Display a booking confirmation message
    booking_confirmation = tk.Label(booking_window, text="Successfully Booked")
    booking_confirmation.pack()

    # Optionally, you can send further details to the mobile number here


def cancel_booking_action():
    phone_number_to_cancel = phone_entry.get()

    # Define the path to the CSV file containing booking records
    csv_file_path = "C:\\Users\\lenovo\\Desktop\\RTMS\\List.csv"

    # Create a temporary file to store updated booking records
    temp_dir = tempfile.gettempdir()
    temp_file_path = os.path.join(temp_dir, 'temp.csv')

    # Open the original CSV file for reading and the temporary file for writing
    with open(temp_file_path, 'w', newline='\r\n') as temp_file, open(csv_file_path, 'r', newline='\r\n') as file:
        reader = csv.reader(file)
        writer = csv.writer(temp_file)
        booking_cancelled = False  # To track if the booking was successfully canceled

        for rec in reader:
            if rec[5] == phone_number_to_cancel:
                print("Destination=", rec[0])
                print("Name=", rec[1])
                print("Class=", rec[4])
                print("Phone Number=", rec[5])
                choice = input("Do you want to cancel the booking(y/n): ")
                if choice.lower() == 'y':
                    print("Booking Cancelled")
                    booking_cancelled = True
                else:
                    writer.writerow(rec)
            else:
                writer.writerow(rec)

    if booking_cancelled:
        # Replace the original CSV file with the updated temporary file
        os.remove(csv_file_path)
        os.rename(temp_file_path, csv_file_path)
    else:
        print("Booking with phone number", phone_number_to_cancel, "not found.")

    # Optionally, you can add code to send confirmation to the user

def plot_train_destination():
    graph_window = tk.Toplevel(root)
    graph_window.title("Graphical Representation (No. of trains destination wise)")
    
    Destination = ["Howrah", "Chennai", "Delhi", "Lucknow", "Amritsar", "Bengaluru"]
    Number = [2, 1, 2, 3, 1, 1]
    
    # Create a figure for the bar chart
    fig, ax = plt.subplots()
    ax.bar(Destination, Number, color='pink')
    ax.set_xlabel("Destination")
    ax.set_ylabel("Number Of Trains")
    ax.set_title("Number Of Trains (Destination wise)")
    
    # Create a Tkinter canvas to display the matplotlib figure
    canvas = FigureCanvasTkAgg(fig, master=graph_window)
    canvas.draw()
    canvas.get_tk_widget().pack()

def main():
    global root
    root = tk.Tk()
    root.title("Railway Ticket Management System")
    
    notebook = ttk.Notebook(root)
    notebook.pack(fill=tk.BOTH, expand=True)
    
    tab_schedule = ttk.Frame(notebook)
    tab_availability = ttk.Frame(notebook)
    tab_booking = ttk.Frame(notebook)
    tab_cancellation = ttk.Frame(notebook)
    tab_graph = ttk.Frame(notebook)
    
    notebook.add(tab_schedule, text="Train Schedule")
    notebook.add(tab_availability, text="Availability")
    notebook.add(tab_booking, text="Booking")
    notebook.add(tab_cancellation, text="Cancellation")
    notebook.add(tab_graph, text="Graph")
    
    schedule_button = tk.Button(tab_schedule, text="Display Train Schedule", command=display_train_schedule)
    schedule_button.pack()
    
    availability_button = tk.Button(tab_availability, text="Check Availability", command=check_availability_by_destination)
    availability_button.pack()
    
    booking_button = tk.Button(tab_booking, text="Book Ticket", command=book_ticket)
    booking_button.pack()
    
    cancellation_button = tk.Button(tab_cancellation, text="Cancel Booking", command=cancel_booking_action)
    cancellation_button.pack()
    
    graph_button = tk.Button(tab_graph, text="Show Graph", command=plot_train_destination)
    graph_button.pack()
    
    root.mainloop()

if __name__ == "__main__":
    main()
