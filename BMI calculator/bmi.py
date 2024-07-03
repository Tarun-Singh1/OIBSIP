import tkinter as tk
from tkinter import messagebox
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

# Global variable for storing user data
user_data = pd.DataFrame(columns=['Name', 'Date', 'Height', 'Weight', 'BMI'])


def calculate_bmi(height, weight):
    try:
        height = float(height)
        weight = float(weight)
        bmi = weight / (height * height)
        return bmi
    except ValueError:
        return None
    except ZeroDivisionError:
        return None


def add_user_data(name, date, height, weight, bmi):
    global user_data
    new_data = pd.DataFrame({'Name': [name], 'Date': [date], 'Height': [height], 'Weight': [weight], 'BMI': [bmi]})
    user_data = pd.concat([user_data, new_data], ignore_index=True)


def save_data():
    global user_data
    user_data.to_csv('user_data.csv', index=False)


def load_data():
    global user_data
    try:
        user_data = pd.read_csv('user_data.csv')
    except FileNotFoundError:
        user_data = pd.DataFrame(columns=['Name', 'Date', 'Height', 'Weight', 'BMI'])


def plot_bmi_trend():
    global user_data
    if user_data.empty:
        messagebox.showinfo("Info", "No data to plot.")
        return

    user_name = name_entry.get()
    user_specific_data = user_data[user_data['Name'] == user_name].copy()

    if user_specific_data.empty:
        messagebox.showinfo("Info", "No data found for the given user.")
        return

    user_specific_data['Date'] = pd.to_datetime(user_specific_data['Date'])
    user_specific_data.sort_values('Date', inplace=True)

    plt.figure(figsize=(10, 5))
    plt.plot(user_specific_data['Date'], user_specific_data['BMI'], marker='o')
    plt.xlabel('Date')
    plt.ylabel('BMI')
    plt.title(f'BMI Trend for {user_name}')
    plt.grid(True)
    plt.show()


def on_calculate():
    try:
        # Fetch input values as floats
        height = float(height_entry.get())
        weight = float(weight_entry.get())

        # Debugging prints
        print(f"Height: {height}, Weight: {weight}")

        # Ensure valid height and weight inputs
        if height <= 0 or weight <= 0:
            raise ValueError("Height and weight must be greater than zero.")

        name = name_entry.get()
        date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Calculate BMI
        bmi = calculate_bmi(height, weight)

        # Debugging print
        print(f"BMI calculated: {bmi}")

        # Check if BMI calculation was successful
        if bmi is None:
            result_label.config(text="Error calculating BMI. Please check your inputs.")
        else:
            # Display BMI and category
            bmi_category = get_bmi_category(bmi)
            result_label.config(text=f"Your BMI is {bmi:.2f}, you are {bmi_category}.")

            # Add data to user_data and save
            add_user_data(name, date, height, weight, bmi)
            save_data()

    except ValueError as ve:
        result_label.config(text=str(ve))

    except Exception as e:
        result_label.config(text=f"An error occurred: {str(e)}")


def get_bmi_category(bmi):
    if bmi < 18.5:
        return "underweight"
    elif 18.5 <= bmi < 25:
        return "normal weight"
    elif 25 <= bmi < 30:
        return "overweight"
    elif 30 <= bmi < 35:
        return "obese"
    elif bmi >= 35:
        return "clinically obese"
    else:
        return "unknown"


# Load existing data
load_data()

# Create the main application window
root = tk.Tk()
root.title("BMI Calculator")

# Create and place widgets
tk.Label(root, text="Name:").grid(row=0, column=0)
name_entry = tk.Entry(root)
name_entry.grid(row=0, column=1)

tk.Label(root, text="Height (m):").grid(row=1, column=0)
height_entry = tk.Entry(root)
height_entry.grid(row=1, column=1)

tk.Label(root, text="Weight (kg):").grid(row=2, column=0)
weight_entry = tk.Entry(root)
weight_entry.grid(row=2, column=1)

calculate_button = tk.Button(root, text="Calculate BMI", command=on_calculate)
calculate_button.grid(row=3, columnspan=2)

result_label = tk.Label(root, text="")
result_label.grid(row=4, columnspan=2)

plot_button = tk.Button(root, text="Show BMI Trend", command=plot_bmi_trend)
plot_button.grid(row=5, columnspan=2)

# Run the application
root.mainloop()
