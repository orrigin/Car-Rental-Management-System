# 🚗 Car Rental Management System

A desktop-based **Car Rental Management System** developed using Python to simplify and manage car rental operations through a graphical user interface. The application integrates database management and email verification to provide a more organized and user-friendly rental management experience.

## 📌 Project Overview

The Car Rental Management System is designed to streamline the process of managing car rental information. It provides a graphical interface for users to interact with the system while storing relevant information in a PostgreSQL database.

The project demonstrates the integration of Python GUI development, relational database management, and email automation in a desktop application.

## ✨ Features

- **User-Friendly Interface:** Interactive desktop GUI built using Python Tkinter.
- **Database Integration:** PostgreSQL database for storing and managing application data.
- **Email Verification:** SMTP integration for email-based verification.
- **Rental Management:** Supports car rental operations through the application interface.
- **Data Management:** Organizes application information using a relational database.

*Note: The features above describe the intended functionality; adjust them to match the functions implemented in your code.*

## 🛠️ Technologies Used

| Technology | Purpose |
|---|---|
| Python | Core application logic |
| Tkinter | Graphical user interface |
| PostgreSQL | Database management |
| SMTP | Email verification |
| psycopg2 / PostgreSQL driver | Python–database connectivity, if used |

## ⚙️ Prerequisites

Before running the project, make sure you have:

- Python 3 installed
- PostgreSQL installed and running
- A code editor such as Visual Studio Code
- Required Python libraries
- SMTP email credentials, if email verification is enabled

## 🚀 Installation and Setup

### 1. Clone the repository

```bash
git clone https://github.com/orrigin/Car-Rental-Management-System.git
```

### 2. Navigate to the project directory

```bash
cd Car-Rental-Management-System
```

### 3. Install dependencies

Install the libraries required by the project. For example, if the code uses `psycopg2`:

```bash
pip install psycopg2-binary
```

Tkinter is included with many Python installations. Install it separately if your operating system requires it.

### 4. Configure PostgreSQL

1. Start your PostgreSQL server.
2. Create a database for the application.
3. Configure the database connection details in the Python source code.
4. Create the tables required by the application.

Use the database name, username, password, and port that match your local setup.

### 5. Configure email verification

If SMTP verification is enabled, configure the appropriate SMTP server and email credentials.

**Security note:** Do not upload passwords, email credentials, or other secrets directly to GitHub. Use environment variables or a local configuration file excluded from version control.

### 6. Run the application

Run the main Python file:

```bash
python "IMPROVED MINI PROJECT1.py"
```

## 📂 Project Structure

```text
Car-Rental-Management-System/
│
├── IMPROVED MINI PROJECT1.py
└── README.md
```

The repository currently contains the main Python application file. Additional database scripts or configuration files can be added as the project develops.

## 🎯 Learning Outcomes

Through this project, the following concepts can be explored:

- Desktop application development using Python Tkinter
- Relational database design and PostgreSQL integration
- Connecting Python applications to databases
- Email automation using SMTP
- Input validation and application workflow management
- Organizing and maintaining a software project

## 🔮 Future Enhancements

- Add car availability tracking and advanced search.
- Implement booking history and rental status management.
- Introduce billing and payment tracking.
- Add role-based access for administrators and customers.
- Improve error handling and input validation.
- Add reports and dashboards for rental activity.

## 👨‍💻 Author

**Aarya Shaparia**

Computer Engineering Student

GitHub: [@orrigin](https://github.com/orrigin)

---

⭐ If you find this project useful, consider giving the repository a star!
