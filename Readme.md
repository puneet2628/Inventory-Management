# Stoxy - Inventory Management System

A robust inventory management system built with Django and Python.

## Features

- Real-time inventory tracking
- Product management
- Stock alerts and notifications
- User authentication and role-based access
- Reporting and analytics
- Order management
- Supplier management

## Requirements

- Python 3.8+
- Django 4.0+
- PostgreSQL/SQLite

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/stoxy.git
cd stoxy
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Create superuser:
```bash
python manage.py createsuperuser
```

6. Run the development server:
```bash
python manage.py runserver
```

## Usage

Access the admin interface at `http://localhost:8000/admin` to manage:
- Products
- Categories
- Stock levels
- Users
- Orders

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License.