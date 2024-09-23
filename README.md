# Leave Management System

This is a Streamlit-based Leave Management System that allows managers and employees to manage leave requests.

This application is deployed on Streamlit Cloud. You can access it [here](https://leave-management-system-qqzzww4n8o5uq3ckpxgogn.streamlit.app/).

## Features

- **User Authentication**: Register and log in as a manager or employee.
- **Leave Requests**: Employees can apply for leave, and managers can approve or reject requests.
- **Dashboard**: Separate dashboards for managers and employees to manage and view leave requests.

## Folder Structure
```plaintext
Leave-Management-System/
├── README.md           # Project documentation and setup instructions
├── create_tables.sql   # Database schema script 
├── leave_management.db # SQLite database file
├── main.py             # Main application code
└── requirements.txt    # List of neccessary dependencies
```

## Tools Used

- **Streamlit**: For building the web application.
- **SQLite**: For the database.
- **Python**: 3.10.11.

## Installation

1. **Clone the repository**:
    ```sh
    git clone https://github.com/Kattie-Nguyen/Leave-Management-System.git
    cd Leave-Management-System
    ```

2. **Set up a virtual environment**:
    ```sh
    python3 -m venv venv
    source venv/bin/activate  # On Windows: .\venv\Scripts\activate
    ```

3. **Install the dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

4. **Create the database** using `create_tables.sql` with SQLite:
    ```sh
    sqlite3 leave_management.db < create_tables.sql
    ```

5. **Run the application**:
    ```sh
    streamlit run main.py
    ```

## Usage

1. Open the application in your browser. The URL will be displayed in the terminal after running the app.
2. Register as a manager or employee.
3. Log in to access the respective dashboard.
4. Employees can apply for leave, and managers can approve or reject leave requests.

## Deployment

This application is deployed on Streamlit Cloud. You can access it [here](https://leave-management-system-qqzzww4n8o5uq3ckpxgogn.streamlit.app/).

