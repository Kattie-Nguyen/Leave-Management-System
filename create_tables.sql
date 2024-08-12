-- Create managers table
CREATE TABLE IF NOT EXISTS managers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

-- Create employees table
CREATE TABLE IF NOT EXISTS employees (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(255) UNIQUE NOT NULL,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    manager_id INTEGER,
    FOREIGN KEY (manager_id) REFERENCES managers(id)
);

-- Create leave_requests table
CREATE TABLE IF NOT EXISTS leave_requests (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id INTEGER,
    manager_id INTEGER,
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    leave_type VARCHAR(255) NOT NULL,
    comment TEXT,
    status VARCHAR(255) DEFAULT 'Pending',
    total_times_off INTEGER DEFAULT 0,
    FOREIGN KEY (employee_id) REFERENCES employees(id),
    FOREIGN KEY (manager_id) REFERENCES managers(id)
);
