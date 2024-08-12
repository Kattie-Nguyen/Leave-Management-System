### IMPORT 
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import declarative_base, sessionmaker, relationship
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError
import streamlit as st
from datetime import datetime

### CONNECT SQLITE
# Database connection setup for SQLite
connection_url = 'sqlite:///leave_management.db'
engine = create_engine(connection_url)
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

class Manager(Base):
    __tablename__ = 'managers'
    id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)

class Employee(Base):
    __tablename__ = 'employees'
    id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True, nullable=False)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    manager_id = Column(Integer, ForeignKey('managers.id'))
    manager = relationship("Manager")

class LeaveRequest(Base):
    __tablename__ = 'leave_requests'
    id = Column(Integer, primary_key=True)
    employee_id = Column(Integer, ForeignKey('employees.id'), nullable=False)
    manager_id = Column(Integer, ForeignKey('managers.id'), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    leave_type = Column(String(255), nullable=False)
    comment = Column(String)
    status = Column(String(255), default='Pending')
    total_times_off = Column(Integer, default=0)
    employee = relationship("Employee")
    manager = relationship("Manager")

Base.metadata.create_all(engine)

## Registration Function
# def register_user(username, password, name, email, is_manager, manager_username=None):
#     hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
#     try:
#         if is_manager:
#             user = Manager(username=username, password=hashed_password, name=name, email=email)
#         else:
#             manager = session.query(Manager).filter_by(username=manager_username).first()
#             user = Employee(username=username, password=hashed_password, name=name, email=email, manager_id=manager.id)
#         session.add(user)
#         session.commit()
#         return user
#     except IntegrityError:
#         session.rollback()
#         st.error("Username or email already exists!")
#         return None

def register_user(username, password, name, email, is_manager, manager_username=None):
    hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
    try:
        if is_manager:
            user = Manager(username=username, password=hashed_password, name=name, email=email)
        else:
            manager = session.query(Manager).filter_by(username=manager_username).first()
            user = Employee(username=username, password=hashed_password, name=name, email=email, manager_id=manager.id)
        session.add(user)
        session.commit()
        return user
    except IntegrityError:
        session.rollback()
        st.error("Username or email already exists!")
        return None

## Login Function
def login_user(username, password):
    manager = session.query(Manager).filter_by(username=username).first()
    employee = session.query(Employee).filter_by(username=username).first()
    if manager and check_password_hash(manager.password, password):
        return 'manager', manager.id
    elif employee and check_password_hash(employee.password, password):
        return 'employee', employee.id
    else:
        return None, None

## Logout Function
def logout():
    st.session_state['role'] = None
    st.session_state['user_id'] = None
    st.rerun()

def refresh():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

## Manager Page
def manager_dashboard(manager_id):
    manager = session.query(Manager).filter_by(id=manager_id).first()
    st.markdown(
        f"""
        <div style='text-align: right; font-size: medium;'>
            👋 Hi, {manager.name}
        </div>
        """,
        unsafe_allow_html=True,
    )

    action = st.sidebar.radio("Select an action", ["All Pending Requests", "View All Requests"])
    
    if action == "All Pending Requests":
        st.markdown("## 📋 Pending Leave Requests")
        
        pending_requests = session.query(LeaveRequest).filter_by(manager_id=manager_id, status='Pending').all()

        col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
        col1.markdown("**Request ID**")
        col2.markdown("**Employee Name**")
        col3.markdown("**Start Date**")
        col4.markdown("**End Date**")
        col5.markdown("**Leave Type**")
        col6.markdown("**Comment**")
        col7.markdown("**Actions**")

        for request in pending_requests:
            employee = session.query(Employee).filter_by(id=request.employee_id).first()
            col1, col2, col3, col4, col5, col6, col7 = st.columns(7)
            col1.write(request.id)
            col2.write(employee.name)
            col3.write(request.start_date.strftime("%Y-%m-%d"))
            col4.write(request.end_date.strftime("%Y-%m-%d"))
            col5.write(request.leave_type)
            col6.write(request.comment if request.comment else "No comment")
            approve = col7.button('✅ Approve', key=f"approve_{request.id}")
            reject = col7.button('❌ Reject', key=f"reject_{request.id}")
            if approve:
                request.status = 'Approved'
                session.commit()
                st.rerun()
            if reject:
                request.status = 'Rejected'
                session.commit()
                st.rerun()
            
            st.markdown("<hr>", unsafe_allow_html=True)

    elif action == "View All Requests":
        st.markdown("## 📋 All Leave Requests")
        
        employees = session.query(Employee).filter_by(manager_id=manager_id).all()
        employee_names = ["All"] + [employee.name for employee in employees]

        employee_filter = st.selectbox("Filter by Employee", employee_names)
        status_filter = st.selectbox("Filter by Status", ["All", "Pending", "Approved", "Rejected"])

        query = session.query(LeaveRequest).filter_by(manager_id=manager_id)
        
        if employee_filter != "All":
            selected_employee = session.query(Employee).filter_by(name=employee_filter).first()
            query = query.filter_by(employee_id=selected_employee.id)
        
        if status_filter != "All":
            query = query.filter_by(status=status_filter)
        
        leave_requests = query.all()

        for request in leave_requests:
            employee = session.query(Employee).filter_by(id=request.employee_id).first()
            st.markdown(f"### 🧑 {employee.name}")
            st.markdown(f"**Email:** {employee.email}")

            col1, col2, col3, col4, col5, col6 = st.columns(6)
            col1.markdown("**Request ID**")
            col1.write(request.id)
            col2.markdown("**Start Date**")
            col2.write(request.start_date.strftime("%Y-%m-%d"))
            col3.markdown("**End Date**")
            col3.write(request.end_date.strftime("%Y-%m-%d"))
            col4.markdown("**Leave Type**")
            col4.write(request.leave_type)
            col5.markdown("**Comment**")
            col5.write(request.comment if request.comment else "No comment")
            col6.markdown("**Status**")
            status_color = "black"
            status_icon = "⏳"
            if request.status == "Approved":
                status_color = "green"
                status_icon = "✅"
            elif request.status == "Rejected":
                status_color = "red"
                status_icon = "❌"
            col6.markdown(f"<span style='color:{status_color};'>{status_icon} {request.status}</span>", unsafe_allow_html=True)

            st.markdown("<hr>", unsafe_allow_html=True)

## Employee Page
def employee_dashboard(employee_id):
    employee = session.query(Employee).filter_by(id=employee_id).first()
    st.markdown(
        f"""
        <div style='text-align: right; font-size: medium;'>
            👋 Hi, {employee.name}
        </div>
        """,
        unsafe_allow_html=True,
    )

    if 'submit_count' not in st.session_state:
        st.session_state['submit_count'] = 0
    
    action = st.sidebar.radio("Select an action", ["Apply for Leave", "Show Leave Requests"])
    
    if action == "Apply for Leave":
        st.markdown("## 📝 Leave Request Form")
        
        start_date = st.date_input("Start Date")
        end_date = st.date_input("End Date")
        leave_type = st.selectbox("Leave Type", ['Sick Leave', 'Vacation', 'Personal', 'Official'])
        comment = st.text_area("Comment")
        
        if st.button('Submit', key='submit_leave'):
            if st.session_state['submit_count'] >= 10:
                st.error("❗ You have reached the maximum number of submissions (10) for this session.")
            elif end_date < start_date:
                st.error("❗ End date must be equal to or after the start date.")
            else:
                manager_id = employee.manager_id
                leave_request = LeaveRequest(
                    employee_id=employee.id,
                    manager_id=manager_id,
                    start_date=start_date,
                    end_date=end_date,
                    leave_type=leave_type,
                    comment=comment
                )
                session.add(leave_request)
                session.commit()
                st.session_state['submit_count'] += 1
                st.success("✅ Leave request submitted!")
    
    elif action == "Show Leave Requests":
        st.markdown("## 📜 My Leave Requests")
        leave_requests = session.query(LeaveRequest).filter_by(employee_id=employee_id).all()
        for request in leave_requests:
            col1, col2, col3, col4, col5, col6 = st.columns(6)
            col1.write(request.id)
            col2.write(request.start_date.strftime("%Y-%m-%d"))
            col3.write(request.end_date.strftime("%Y-%m-%d"))
            col4.write(request.leave_type)
            col5.write(request.comment if request.comment else "No comment")
            
            status_color = "black"
            status_icon = "⏳"
            if request.status == "Approved":
                status_color = "green"
                status_icon = "✅"
            elif request.status == "Rejected":
                status_color = "red"
                status_icon = "❌"
            
            col6.markdown(f"<span style='color:{status_color};'>{status_icon} {request.status}</span>", unsafe_allow_html=True)


## Main Fucntion
def main():
    if 'role' not in st.session_state:
        st.session_state['role'] = None
    if 'user_id' not in st.session_state:
        st.session_state['user_id'] = None
    st.sidebar.title("Navigation")

    if st.sidebar.button("🔄 Refresh", key="refresh"):
        refresh()

    if st.session_state['role'] is None:
        choice = st.sidebar.radio("Go to", ["Login", "Register"], key="nav_choice")
    else:
        if st.sidebar.button("🚪 Logout", key="logout"):
            logout()

        if st.session_state['role'] == 'manager':
            manager_dashboard(st.session_state['user_id'])
        elif st.session_state['role'] == 'employee':
            employee_dashboard(st.session_state['user_id'])
        return

    if choice == "Login":
        st.title("Login")
        username = st.text_input("Username", key="login_username")
        password = st.text_input("Password", type="password", key="login_password")
        
        if st.button("Login", key="login_button"):
            role, user_id = login_user(username, password)
            if role == 'manager':
                st.session_state['role'] = 'manager'
                st.session_state['user_id'] = user_id
                st.rerun()
            elif role == 'employee':
                st.session_state['role'] = 'employee'
                st.session_state['user_id'] = user_id
                st.rerun()
            else:
                st.error("Invalid credentials")

    elif choice == "Register":
        st.title("Register")
        username = st.text_input("Username", key="register_username")
        password = st.text_input("Password", type="password", key="register_password")
        name = st.text_input("Name", key="register_name")
        email = st.text_input("Email", key="register_email")
        is_manager = st.checkbox("Register as Manager", key="register_is_manager")

        if not is_manager:
            managers = session.query(Manager).all()
            manager_usernames = [manager.username for manager in managers]
            manager_username = st.selectbox("Select Manager", manager_usernames, key="register_manager_username")
        else:
            manager_username = None

        if st.button("Register", key="register_button"):
            user = register_user(username, password, name, email, is_manager, manager_username)
            if user:
                st.success(f"User {user.username} registered successfully!")

if __name__ == "__main__":
    main()

