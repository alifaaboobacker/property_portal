# Property Portal Setup Guide

## Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- SQLite (comes with Python)

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
cd property_portal
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Generate encryption key:
```bash
python generate_key.py
```

5. Initialize the database:
```bash
python app.py
```

## Configuration

1. Edit `app.py` to configure:
   - `SECRET_KEY`: Change to a secure random string
   - `SQLALCHEMY_DATABASE_URI`: Modify if using a different database

2. The application uses SQLite by default. The database file will be created at `property_portal.db`.

## Running the Application

1. Start the Flask application:
```bash
python app.py
```

2. Access the application at `http://127.0.0.1:5000`

## Features

1. **Admin Panel** (`/admin`)
   - Add new customers
   - View customer details
   - Track project status (Foundation, Framing, Finishing)
   - Secure password management

2. **Login System** (`/login`)
   - Username/password authentication
   - Password visibility toggle
   - Session management

3. **Dashboard** (`/dashboard`)
   - View project status
   - Customer information
   - Progress tracking

## Security Features

1. **Password Management**
   - Password encryption for admin viewing
   - Password hashing for authentication
   - Secure session management

2. **Data Protection**
   - Fernet encryption for sensitive data
   - Secure database connections
   - Input validation

## Troubleshooting

1. **Database Issues**
   - Ensure SQLite is installed
   - Check database permissions
   - Verify database URI

2. **Encryption Issues**
   - Ensure `key.key` file exists
   - Check encryption key permissions
   - Verify Fernet initialization

3. **Login Issues**
   - Check username/password format
   - Verify session configuration
   - Check database connection

## Directory Structure
```
property_portal/
├── app.py              # Main application file
├── generate_key.py     # Encryption key generator
├── static/
│   ├── css/
│   │   ├── admin.css
│   │   └── login.css
│   └── js/
│       ├── admin.js
│       └── login.js
├── templates/
│   ├── admin.html
│   ├── base.html
│   └── login.html
└── key.key            # Encryption key file
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
