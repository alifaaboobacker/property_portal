from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from flask_session import Session
from cryptography.fernet import Fernet
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'  # Change this in production
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///property_portal.db'
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    username = db.Column(db.String(80), unique=True, nullable=False)
    encrypted_password = db.Column(db.String(500), nullable=False)  # Increased size for encrypted data
    password_hash = db.Column(db.String(128), nullable=False)
    foundation_status = db.Column(db.String(20), default='Not Started')
    framing_status = db.Column(db.String(20), default='Not Started')
    finishing_status = db.Column(db.String(20), default='Not Started')

    def set_password(self, password):
        if not password:
            raise ValueError("Password cannot be empty")
        
        try:
            # Encrypt the password for admin panel viewing
            self.encrypted_password = fernet.encrypt(password.encode()).decode()
            
            # Hash the password for authentication
            self.password_hash = generate_password_hash(password)
        except Exception as e:
            print(f"Error encrypting password: {str(e)}")
            raise

    def get_decrypted_password(self):
        if not self.encrypted_password:
            return None
            
        try:
            return fernet.decrypt(self.encrypted_password.encode()).decode()
        except Exception as e:
            print(f"Error decrypting password: {str(e)}")
            return None

    def check_password(self, password):
        if not self.password_hash:
            return False
        return check_password_hash(self.password_hash, password)

def init_fernet():
    key_file = 'key.key'
    if not os.path.exists(key_file):
        key = Fernet.generate_key()
        with open(key_file, 'wb') as f:
            f.write(key)
    else:
        with open(key_file, 'rb') as f:
            key = f.read()
    return Fernet(key)

# Initialize Fernet globally
fernet = init_fernet()

with app.app_context():
    try:
        # Create tables if they don't exist
        db.create_all()
    except Exception as e:
        print(f"Error initializing database: {str(e)}")
        raise

def generate_username(name):
    base = name.lower().replace(' ', '_')
    count = 1
    username = base
    while User.query.filter_by(username=username).first():
        username = f"{base}_{count}"
        count += 1
    return username

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/admin', methods=['GET', 'POST'])
def admin():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        foundation_status = request.form['foundation_status']
        framing_status = request.form['framing_status']
        finishing_status = request.form['finishing_status']
        
        # Check if email already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email already exists. Please use a different email.', 'error')
            return redirect(url_for('admin'))
        
        # Generate username
        username = generate_username(name)
        
        # Generate password
        password = f"{name.lower().replace(' ', '')}_{datetime.now().strftime('%Y%m%d')}"
        
        # Create new user
        new_user = User(
            name=name,
            email=email,
            username=username,
            foundation_status=foundation_status,
            framing_status=framing_status,
            finishing_status=finishing_status
        )
        
        # Set password (this will store both encrypted and hashed versions)
        new_user.set_password(password)
        
        db.session.add(new_user)
        db.session.commit()
        
        flash(f'User created successfully! Username: {username}, Password: {password}', 'success')
        
    users = User.query.all()
    return render_template('admin.html', users=users, get_original_password=get_original_password)

# Function to get original password
def get_original_password(password_hash):
    user = User.query.filter_by(password_hash=password_hash).first()
    if user and user.encrypted_password:
        return fernet.decrypt(user.encrypted_password.encode()).decode()
    return None

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            session['user_id'] = user.id
            return redirect(url_for('dashboard', user_id=user.id))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@app.route('/dashboard/<int:user_id>')
def dashboard(user_id):
    # Verify session
    if 'user_id' not in session or session['user_id'] != user_id:
        return redirect(url_for('login'))
    
    user = User.query.get_or_404(user_id)
    return render_template('dashboard.html', user=user)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
