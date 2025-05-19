import random               #  Used to generate a random 6-digit OTP.
import smtplib              # Allows sending emails via SMTP (Simple Mail Transfer Protocol).
import ssl                  # Ensures the connection to the SMTP server is secure.
from email.message import EmailMessage        # Helps create a properly formatted email (To, From, Subject, Body).
import tkinter as tk                          # Standard GUI library in Python for creating windows, buttons, inputs, etc.
from tkinter import messagebox                # Provides pop-up windows for messages (like warnings or success).
import time                                   # Used for delays (optional but here for completeness).

# Import email credentials from separate config file
from email_credentials import SENDER_EMAIL, SENDER_PASSWORD

# Global variables
generated_otp = None         #generated_otp: Will store the random OTP.
attempts_left = 3            #attempts_left: Tracks how many tries the user has left (starts with 3).

# Function to generate a 6-digit OTP
def generate_otp():                            #This function generates a random 6-digit number (from 100000 to 999999) and str():Returns it as a string for easier comparison and input handling.
    return str(random.randint(100000, 999999))

# Function to send the OTP via email
def send_otp_email(receiver_email, otp):      #receiver_email: The email address the user inputs.
    subject = "Your OTP Verification Code"
    body = f"Your OTP is: {otp}"              #Sets the subject and body of the email.

    em = EmailMessage()
    em['From'] = SENDER_EMAIL
    em['To'] = receiver_email                #Constructs the email using EmailMessage.
    em['Subject'] = subject
    em.set_content(body)

    context = ssl.create_default_context()          #Connects securely to Gmail’s SMTP server.
    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:   # open a secure connection to Gmail's mail server using SSL on port 465.”
            smtp.login(SENDER_EMAIL, SENDER_PASSWORD)                 #authenticates our app with Gmail using the credentials we defined earlier
            smtp.send_message(em)                                     #this line sends the actual email 
        return True
    except Exception as e:
        print("Error sending email:", e)                #Catches and prints errors if the email fails to send, returns False.
        return False

# GUI Function to request OTP
def request_otp():
    global generated_otp, attempts_left            #Gets the email address entered by the user.
    email = email_entry.get().strip()

    if not email:
        messagebox.showwarning("Warning", "Please enter an email address.")  #Warns if no email is entered.
        return

    generated_otp = generate_otp()                   #Generates a new OTP and resets the attempt counter.
    attempts_left = 3
    success = send_otp_email(email, generated_otp)     #Calls send_otp_email() to send the OTP.

    if success:
        messagebox.showinfo("Success", f"OTP sent to {email}. You have 3 attempts to verify.")
    else:
        messagebox.showerror("Error", "Failed to send OTP. Check console for errors.")

# GUI Function to verify OTP
def verify_user_otp():
    global generated_otp, attempts_left
    user_input = otp_entry.get().strip()  #reads the otp entered by user and removes the spaces

    if not generated_otp:
        messagebox.showerror("Error", "Please request an OTP first.")    #Ensures that OTP is generated before checking.
        return

    if user_input == generated_otp:
        messagebox.showinfo("Access Granted", " OTP Verified. Access Granted!")       #If OTP matches, shows success message.
    else:
        attempts_left -= 1
        if attempts_left > 0:
            messagebox.showwarning("Incorrect OTP", f" Incorrect OTP. You have {attempts_left} attempts left.")   #Reduces attempt count.
        else:
            messagebox.showerror("Access Denied", " You have used all attempts. Access Denied in 5 seconds...")
            root.after(5000, root.destroy)                                   #If 0 attempts left: shows error and closes app after 5 seconds

# GUI Setup
root = tk.Tk()                                    #Creates the main app window.
root.title("OTP Verification System")
root.geometry("400x250")
root.resizable(False, False)

# Email Input
tk.Label(root, text="Enter your email:", font=('Arial', 12)).pack(pady=10)
email_entry = tk.Entry(root, width=40)
email_entry.pack(pady=5)

send_btn = tk.Button(root, text="Send OTP", command=request_otp, bg="#4CAF50", fg="white", width=20)
send_btn.pack(pady=10)

# OTP Input
tk.Label(root, text="Enter OTP received:", font=('Arial', 12)).pack(pady=10)
otp_entry = tk.Entry(root, width=20)
otp_entry.pack(pady=5)

verify_btn = tk.Button(root, text="Verify OTP", command=verify_user_otp, bg="#2196F3", fg="white", width=20)
verify_btn.pack(pady=10)

root.mainloop()
