import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import psycopg2
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
import os

# ===================== DATABASE CONNECTION =====================
def get_connection():
    return psycopg2.connect(
        host="localhost",
        database="Car rental",
        user="postgres",
        password="Qwerty@123"
    )

# ===================== EMAIL FUNCTION =====================
def send_verification_email(name, email, licence_file):
    sender_email = "aaryashaparia09@gmail.com"
    sender_password = "ekcr rzyy sduo eozc"
    receiver_email = "124aarya2022@sjcem.edu.in"

    subject = "New License Verification Request"
    body = f"""
New customer verification request:

Name: {name}
Email: {email}

Please find the attached license image for verification.
"""

    msg = MIMEMultipart()
    msg["From"] = sender_email
    msg["To"] = receiver_email
    msg["Subject"] = subject
    msg.attach(MIMEText(body, "plain"))

    if os.path.exists(licence_file):
        with open(licence_file, "rb") as f:
            part = MIMEBase("application", "octet-stream")
            part.set_payload(f.read())
        encoders.encode_base64(part)
        part.add_header("Content-Disposition", f"attachment; filename={os.path.basename(licence_file)}")
        msg.attach(part)

    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()
        messagebox.showinfo("Success", "License sent for verification!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed to send email: {str(e)}")

# ===================== ADMIN FUNCTIONS =====================
def add_car_to_db(model, rent, quantity):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO car (model, rent, quantity) VALUES (%s, %s, %s)", (model, rent, quantity))
        conn.commit()
        cur.close()
        conn.close()
        messagebox.showinfo("Success", "Car added successfully!")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def view_cars():
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT cid, model, rent, quantity FROM car")
        rows = cur.fetchall()
        cur.close()
        conn.close()

        view_win = tk.Toplevel()
        view_win.title("Available Cars")
        view_win.geometry("400x300")

        tk.Label(view_win, text="Car ID | Model | Rent | Available", font=("Arial", 12, "bold")).pack(pady=5)
        for row in rows:
            tk.Label(view_win, text=f"{row[0]} | {row[1]} | Rs.{row[2]} | {row[3]}").pack(anchor="w")

    except Exception as e:
        messagebox.showerror("Error", str(e))

# ===================== CUSTOMER DATA FUNCTIONS =====================
def save_customer_details(name, dob=None, licence=None, email=None, car_id=None, days=None):
    try:
        conn = get_connection()
        cur = conn.cursor()
        if car_id and days:
            cur.execute(
                "INSERT INTO custt (name, dob, licence, email, car_id, days) VALUES (%s, %s, %s, %s, %s, %s)",
                (name, dob, licence, email, car_id, days)
            )
            # Reduce car quantity
            cur.execute("UPDATE car SET quantity = quantity - 1 WHERE cid = %s", (car_id,))
        else:
            # Check if customer already exists
            cur.execute("SELECT * FROM custt WHERE name=%s AND licence=%s", (name, licence))
            if cur.fetchone():
                messagebox.showwarning("Exists", "You have already submitted a verification request!")
                return
            cur.execute(
                "INSERT INTO custt (name, dob, licence, email, verified) VALUES (%s, %s, %s, %s, FALSE)",
                (name, dob, licence, email)
            )
        conn.commit()
        cur.close()
        conn.close()
    except Exception as e:
        messagebox.showerror("Error", str(e))

# ===================== CUSTOMER VERIFICATION =====================
def open_customer_panel():
    cust_panel = tk.Toplevel(root)
    cust_panel.title("Customer Verification")
    cust_panel.geometry("400x600")

    tk.Label(cust_panel, text="Customer Verification Page", font=("Arial", 14)).pack(pady=10)

    tk.Label(cust_panel, text="Name").pack()
    name_entry = tk.Entry(cust_panel)
    name_entry.pack()

    tk.Label(cust_panel, text="Email").pack()
    email_entry = tk.Entry(cust_panel)
    email_entry.pack()

    tk.Label(cust_panel, text="Date of Birth").pack()
    dob_entry = tk.Entry(cust_panel)
    dob_entry.pack()

    tk.Label(cust_panel, text="Licence Number").pack()
    licence_entry = tk.Entry(cust_panel)
    licence_entry.pack()

    tk.Label(cust_panel, text="Upload Licence Image").pack()
    licence_path_var = tk.StringVar()
    file_label = tk.Label(cust_panel, text="")
    file_label.pack()

    def upload_file():
        file_path = filedialog.askopenfilename(title="Select Licence Photo", filetypes=[("Images", "*.jpg *.jpeg *.png")])
        if file_path:
            licence_path_var.set(file_path)
            file_label.config(text=os.path.basename(file_path))

    tk.Button(cust_panel, text="Upload", command=upload_file).pack(pady=5)

    def send_for_verification():
        name = name_entry.get()
        email = email_entry.get()
        dob = dob_entry.get()
        licence = licence_entry.get()
        licence_file = licence_path_var.get()

        if not name or not email or not dob or not licence or not licence_file:
            messagebox.showerror("Error", "Please fill all fields and upload licence image!")
            return

        save_customer_details(name, dob, licence, email)
        send_verification_email(name, email, licence_file)
        cust_panel.destroy()

    tk.Button(cust_panel, text="Send for Verification", command=send_for_verification).pack(pady=10)

# ===================== CUSTOMER BOOKING PANEL =====================
def open_booking_panel(customer_name):
    booking_panel = tk.Toplevel(root)
    booking_panel.title("Book a Car")
    booking_panel.geometry("400x300")

    tk.Label(booking_panel, text=f"Welcome, {customer_name}", font=("Arial", 14)).pack(pady=10)

    tk.Label(booking_panel, text="Select Car").pack()
    car_var = tk.StringVar(booking_panel)
    car_dropdown = tk.OptionMenu(booking_panel, car_var, "Loading cars...")
    car_dropdown.pack()

    tk.Label(booking_panel, text="Rent (Rs.)").pack()
    rent_label = tk.Label(booking_panel, text="0")
    rent_label.pack()

    tk.Label(booking_panel, text="Days").pack()
    days_entry = tk.Entry(booking_panel)
    days_entry.pack()

    car_dict = {}
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT cid, model, rent FROM car WHERE quantity > 0")
        cars = cur.fetchall()
        cur.close()
        conn.close()

        if cars:
            car_var.set(f"{cars[0][0]} - {cars[0][1]}")
            rent_label.config(text=f"{cars[0][2]}")
            menu = car_dropdown["menu"]
            menu.delete(0, "end")
            for cid, model, rent in cars:
                car_dict[cid] = rent
                menu.add_command(label=f"{cid} - {model}",
                                 command=lambda v=f"{cid} - {model}": [car_var.set(v),
                                                                       rent_label.config(text=str(car_dict[int(v.split(' - ')[0])]))])
        else:
            car_var.set("No cars available")
            rent_label.config(text="0")
    except Exception as e:
        messagebox.showerror("Error", str(e))

    def save_booking():
        days = days_entry.get()
        car_selection = car_var.get()

        if not car_selection or car_selection == "No cars available":
            messagebox.showerror("Error", "Please select a valid car!")
            return

        if days.isdigit():
            car_id = int(car_selection.split(" - ")[0])
            save_customer_details(customer_name, car_id=car_id, days=int(days))
            booking_panel.destroy()
            total_rent = car_dict[car_id] * int(days)

            success_win = tk.Toplevel(root)
            success_win.title("Booking Successful")
            success_win.geometry("300x200")
            tk.Label(success_win, text="Booking Successful!", font=("Arial", 16)).pack(pady=20)
            tk.Label(success_win, text=f"Car: {car_selection}\nDays: {days}\nTotal Rent: Rs.{total_rent}").pack(pady=10)
            tk.Button(success_win, text="OK", command=success_win.destroy).pack(pady=10)
        else:
            messagebox.showerror("Error", "Enter valid number of days!")

    tk.Button(booking_panel, text="Book Car", command=save_booking).pack(pady=15)

# ===================== CUSTOMER LOGIN =====================
def open_customer_login():
    login_win = tk.Toplevel(root)
    login_win.title("Customer Login")
    login_win.geometry("350x250")

    tk.Label(login_win, text="Customer Login", font=("Arial", 14)).pack(pady=10)

    tk.Label(login_win, text="Name").pack()
    name_entry = tk.Entry(login_win)
    name_entry.pack()

    tk.Label(login_win, text="Licence Number").pack()
    licence_entry = tk.Entry(login_win)
    licence_entry.pack()

    def check_login():
        name = name_entry.get()
        licence = licence_entry.get()

        if not name or not licence:
            messagebox.showerror("Error", "Please enter both fields!")
            return

        try:
            conn = get_connection()
            cur = conn.cursor()
            cur.execute("SELECT verified FROM custt WHERE name=%s AND licence=%s", (name, licence))
            row = cur.fetchone()
            cur.close()
            conn.close()

            if row is None:
                messagebox.showerror("Error", "User not found!")
            elif row[0] is True:
                messagebox.showinfo("Login Success", "Welcome! You are verified.")
                login_win.destroy()
                open_booking_panel(name)
            else:
                messagebox.showerror("Not Verified", "Your account is not verified by admin yet!")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    tk.Button(login_win, text="Login", command=check_login, bg="#2ECC71", fg="white").pack(pady=15)
    tk.Button(login_win, text="Customer Verification", command=open_customer_panel, bg="#3498DB", fg="white").pack(side="bottom", pady=10)

# ===================== ADMIN VERIFICATION =====================
def open_verification_window():
    window = tk.Toplevel()
    window.title("Customer Verification Panel")
    window.geometry("700x400")
    window.configure(bg="#f4f4f4")

    tk.Label(window, text="Pending Customer Verifications",
             font=("Arial", 14, "bold"), bg="#f4f4f4").pack(pady=10)

    tree = ttk.Treeview(window, columns=("cust_id", "name", "licence", "email"),
                        show="headings", height=10)
    tree.pack(pady=10, fill="both", expand=True)

    tree.heading("cust_id", text="Customer ID")
    tree.heading("name", text="Name")
    tree.heading("licence", text="Licence No.")
    tree.heading("email", text="Email")

    tree.column("cust_id", width=100, anchor="center")
    tree.column("name", width=150)
    tree.column("licence", width=150)
    tree.column("email", width=200)

    def load_pending_customers():
        for row in tree.get_children():
            tree.delete(row)
        try:
            con = get_connection()
            cur = con.cursor()
            cur.execute("SELECT cust_id, name, licence, email FROM custt WHERE verified IS NULL OR verified = FALSE")
            rows = cur.fetchall()
            for r in rows:
                tree.insert("", "end", values=r)
            con.close()
        except Exception as e:
            messagebox.showerror("Error", f"Database error: {e}")

    load_pending_customers()

    def verify_customer():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Select", "Please select a customer to verify.")
            return
        cust_id = tree.item(selected[0])['values'][0]
        try:
            con = get_connection()
            cur = con.cursor()
            cur.execute("UPDATE custt SET verified = TRUE WHERE cust_id = %s", (cust_id,))
            con.commit()
            con.close()
            messagebox.showinfo("Success", "Customer verified successfully.")
            load_pending_customers()  # Reload dynamically
        except Exception as e:
            messagebox.showerror("Error", f"Failed to verify: {e}")

    def reject_customer():
        selected = tree.selection()
        if not selected:
            messagebox.showwarning("Select", "Please select a customer to reject.")
            return
        cust_id = tree.item(selected[0])['values'][0]
        try:
            con = get_connection()
            cur = con.cursor()
            cur.execute("UPDATE custt SET verified = FALSE WHERE cust_id = %s", (cust_id,))
            con.commit()
            con.close()
            messagebox.showinfo("Rejected", "Customer rejected successfully.")
            load_pending_customers()  # Reload dynamically
        except Exception as e:
            messagebox.showerror("Error", f"Failed to reject: {e}")

    button_frame = tk.Frame(window, bg="#f4f4f4")
    button_frame.pack(pady=10)

    tk.Button(button_frame, text="Verify", command=verify_customer,
              bg="#4CAF50", fg="white", width=12).grid(row=0, column=0, padx=10)
    tk.Button(button_frame, text="Reject", command=reject_customer,
              bg="#E74C3C", fg="white", width=12).grid(row=0, column=1, padx=10)
    tk.Button(button_frame, text="Refresh", command=load_pending_customers,
              bg="#3498DB", fg="white", width=12).grid(row=0, column=2, padx=10)

# ===================== ADMIN PANEL =====================
def open_admin_panel():
    admin_panel = tk.Toplevel(root)
    admin_panel.title("Admin Panel")
    admin_panel.geometry("400x400")

    tk.Label(admin_panel, text="Admin Panel", font=("Arial", 16)).pack(pady=10)
    tk.Button(admin_panel, text="Add Car", command=open_add_car).pack(pady=10)
    tk.Button(admin_panel, text="View Cars", command=view_cars).pack(pady=10)
    tk.Button(admin_panel, text="Verify Customers", command=open_verification_window).pack(pady=10)

def open_add_car():
    win = tk.Toplevel(root)
    win.title("Add Car")
    win.geometry("350x300")

    tk.Label(win, text="Model").pack()
    model_entry = tk.Entry(win)
    model_entry.pack()

    tk.Label(win, text="Rent").pack()
    rent_entry = tk.Entry(win)
    rent_entry.pack()

    tk.Label(win, text="Quantity").pack()
    qty_entry = tk.Entry(win)
    qty_entry.pack()

    def save():
        m = model_entry.get()
        r = rent_entry.get()
        q = qty_entry.get()
        if m and r.isdigit() and q.isdigit():
            add_car_to_db(m, int(r), int(q))
        else:
            messagebox.showerror("Error", "Enter valid details!")

    tk.Button(win, text="Save", command=save).pack(pady=10)

# ===================== ADMIN LOGIN =====================
def open_admin_login():
    login_window = tk.Toplevel(root)
    login_window.title("Admin Login")
    login_window.geometry("300x200")

    tk.Label(login_window, text="Admin Login", font=("Arial", 14)).pack(pady=10)
    tk.Label(login_window, text="Username").pack()
    username_entry = tk.Entry(login_window)
    username_entry.pack()

    tk.Label(login_window, text="Password").pack()
    password_entry = tk.Entry(login_window, show="*")
    password_entry.pack()

    def check_login():
        if username_entry.get() == "aarya" and password_entry.get() == "1234":
            messagebox.showinfo("Login", "Admin Logged In!")
            login_window.destroy()
            open_admin_panel()
        else:
            messagebox.showerror("Error", "Invalid credentials!")

    tk.Button(login_window, text="Login", command=check_login).pack(pady=10)

# ===================== MAIN WINDOW =====================
root = tk.Tk()
root.title("Car Rental System")
root.geometry("400x300")

tk.Label(root, text="Welcome to Car Rental System", font=("Arial", 16)).pack(pady=30)
tk.Button(root, text="Admin Login", font=("Arial", 12), width=15, command=open_admin_login).pack(pady=10)
tk.Button(root, text="Customer Login", font=("Arial", 12), width=15, command=open_customer_login).pack(pady=10)

root.mainloop()
