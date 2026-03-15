# Online Laptop & Desktop Rental Management System (LDRMS)

A comprehensive Django-based web application designed to manage laptop and desktop rentals efficiently. This system features user registration, product browsing, booking management, and a robust admin dashboard.

## 🚀 Features

### For Users
- **User Authentication**: Secure signup and login for customers.
- **Product Catalog**: Browse available laptops and desktops with detailed specifications.
- **Booking System**: Online booking with payment proof (screenshot) upload functionality.
- **Booking Tracking**: Real-time status updates on rental requests.
- **Profile Management**: Update personal information and change passwords.
- **Invoicing**: Generate and view invoices for rental bookings.

### For Administrators
- **Dashboard**: High-level overview of products, brands, and booking statuses.
- **Inventory Management**: Add, edit, and delete laptops, desktops, and brands.
- **Booking Control**: Approve or reject rental requests and update tracking history.
- **Reports**: Generate sales and booking reports based on specific date ranges.
- **User Management**: Monitor and manage registered users.

## 🛠️ Tech Stack
- **Backend**: Python, Django
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap
- **Database**: SQLite (default)
- **Templating**: Django Template Language (DTL)

## 📋 Prerequisites
- Python 3.10+
- Django 5.0+

## ⚙️ Installation & Setup

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Shabba-kausar/Online-Laptop-Desktop-Rental-Management-System.git
   cd Online-Laptop-Desktop-Rental-Management-System
   ```

2. **Create and activate a virtual environment**:
   ```bash
   python -m venv venv
   # On Windows:
   .\venv\Scripts\activate
   # On macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install django
   ```

4. **Apply migrations**:
   ```bash
   python manage.py migrate
   ```

5. **Create a superuser (for Admin access)**:
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**:
   ```bash
   python manage.py runserver
   ```
   Access the site at `http://127.0.0.1:8000/` and the admin panel at `http://127.0.0.1:8000/admin/`.

## 📁 Project Structure
- `LaptopDesktopRentalMgmt/`: Core project configuration (settings, URLs, WSGI/ASGI).
- `textapp/`: Main application containing views, models, and templates.
- `media/`: Storage for uploaded product images and payment screenshots.
- `static/`: Frontend assets (CSS, JS, Images).

---
Developed with ❤️ by [Shabba Kausar](https://github.com/Shabba-kausar)
