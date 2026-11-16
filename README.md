# Customer360 – Customer Relationship Management System

## Project Overview

Customer360 is a Python and MySQL-based Customer Relationship Management (CRM) application developed using Streamlit. It helps manage customer information, track purchases, record feedback, and analyze customer behavior through interactive dashboards.

## Technologies Used

- Python
- MySQL
- Streamlit
- Pandas
- Plotly
- Bcrypt
- Python-dotenv
- OpenPyXL

## Key Features

### 1. User Authentication
- Login using username or email.
- Secure password hashing using Bcrypt.
- Logout functionality.

### 2. Customer Management
- Add, update, search, and filter customers.
- Input validation.
- Bulk customer import using Excel/CSV.
- Archive and restore customers.
- View customer purchase history.

### 3. Order Management
- Create orders with multiple products.
- Calculate order totals automatically.
- Update payment and order statuses.
- Track customer orders and purchase history.

### 4. Feedback Management
- Record customer feedback and ratings.
- Import feedback in bulk using Excel/CSV.
- View feedback history.

### 5. Dashboard
- Total, active, and inactive customer statistics.
- Customer distribution by city.
- Customer registration trends.
- Interactive visualizations.

### 6. Customer Analytics
- RFM customer segmentation.
- Revenue analysis by city.
- Top five customers.
- Customer churn-risk analysis.

## Project Structure

```text
Customer_Management_Project/
│
├── app.py
├── create_admin.py
├── requirements.txt
├── database_structure.sql
├── export_database_structure.py
│
├── database/
│   └── db_connection.py
│
├── modules/
│   ├── customer_operation.py
│   ├── feedback_operations.py
│   ├── order_operations.py
│   ├── product_operations.py
│   └── user_operations.py
│
├── services/
│   ├── customer_segmentation.py
│   └── dashboard_service.py
│
└── utils/
    └── validators.py
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd Customer_Management_Project
```

### 2. Create and activate a virtual environment

```bash
python -m venv venv
```

Windows:

```cmd
venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure MySQL

- Install and start MySQL Server.
- Import `database_structure.sql` using MySQL Workbench.
- This file contains the database structure without customer records.

### 5. Configure environment variables

Create a `.env` file in the project root:

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=YOUR_MYSQL_PASSWORD
DB_NAME=customer_management
DB_PORT=3306
```

Replace the placeholder with your own MySQL password.

**Security:** Never upload your `.env` file or real database credentials to GitHub.

### 6. Create an admin account

```bash
python create_admin.py
```

Follow the prompts to create your login account.

### 7. Run the application

```bash
streamlit run app.py
```

## Project Objective

The objective of Customer360 is to demonstrate practical skills in Python development, SQL database management, data processing, customer analytics, and interactive dashboard development.

## Future Enhancements

- Role-based access control.
- Advanced customer retention analytics.
- Automated reporting.
- Cloud deployment.
