# Django Marketplace

A modern e-commerce marketplace application built with Django, migrated and upgraded from a Flask application.

## 🚀 Features

### ✅ Completed Features
- **User Management**: Custom user model with buyer/seller roles
- **Product Catalog**: Advanced product management with categories, images, and stock tracking
- **Shopping Cart**: Session-based cart with item management
- **Order System**: Complete order lifecycle management
- **Payment Processing**: Integrated payment gateway support (Paystack)
- **Admin Interface**: Professional Django admin with custom configurations
- **Database Models**: PostgreSQL-ready with SQLite fallback
- **Security**: Django's built-in security features + CSRF protection

### 🔄 Migration Improvements from Flask
- **Better Architecture**: Modular Django apps vs monolithic Flask
- **Advanced ORM**: Django ORM vs raw SQL queries
- **Built-in Admin**: Professional admin interface vs custom-built
- **User Authentication**: Django-allauth vs basic session management
- **Model Relationships**: Proper foreign keys and constraints
- **Migrations**: Automatic database schema management
- **Security**: Built-in CSRF, XSS, and SQL injection protection

## 📁 Project Structure

```
django_marketplace/
├── accounts/           # User management
├── products/          # Product catalog
├── cart/             # Shopping cart functionality
├── orders/           # Order management
├── payments/         # Payment processing
├── templates/        # HTML templates
├── static/          # CSS, JS, images
├── media/           # User uploads
└── marketplace/     # Django project settings
```

## 🛠️ Setup Instructions

1. **Activate Virtual Environment**:
   ```bash
   .\venv\Scripts\Activate.ps1
   ```

2. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Environment Setup**:
   - Copy `.env` file and update values
   - For development: Set `USE_SQLITE=True`
   - For production: Configure PostgreSQL settings

4. **Database Setup**:
   ```bash
   python manage.py migrate
   ```

5. **Create Superuser**:
   ```bash
   python manage.py createsuperuser
   ```

6. **Run Development Server**:
   ```bash
   python manage.py runserver
   ```

## 🌐 URLs

- **Homepage**: http://127.0.0.1:8000/
- **Admin Panel**: http://127.0.0.1:8000/admin/
- **Authentication**: http://127.0.0.1:8000/accounts/

## 📦 Key Technologies

- **Backend**: Django 5.2.4
- **Database**: PostgreSQL (SQLite for development)
- **Authentication**: django-allauth
- **API**: Django REST Framework
- **Frontend**: Bootstrap 5
- **Payment**: Paystack integration
- **Image Processing**: Pillow

## 🔧 Configuration

### Environment Variables (.env)
```env
DJANGO_SECRET_KEY=your-secret-key
DEBUG=True
USE_SQLITE=True  # For development

# Database (PostgreSQL)
DB_NAME=marketplace_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432

# Paystack
PAYSTACK_PUBLIC_KEY=pk_test_...
PAYSTACK_SECRET_KEY=sk_test_...
```

## 🎯 Next Steps

1. **Create Superuser**: `python manage.py createsuperuser`
2. **Add Sample Data**: Use admin panel to add categories and products
3. **Customize Templates**: Update templates for your brand
4. **Add API Endpoints**: Implement REST API views
5. **Frontend Enhancement**: Add JavaScript functionality
6. **Payment Integration**: Complete Paystack webhook setup
7. **Deploy**: Configure for production deployment

## 📚 Learning Django

As you work with this application, you'll learn:
- Django models and ORM
- Django admin customization
- URL routing and views
- Template system
- User authentication
- Database migrations
- Django REST Framework

## 🆚 Flask vs Django Comparison

| Feature | Flask (Old) | Django (New) |
|---------|-------------|--------------|
| Architecture | Monolithic | Modular Apps |
| Database | Raw SQL + SQLite | Django ORM + PostgreSQL |
| Admin | Custom built | Built-in professional admin |
| Security | Manual implementation | Built-in protections |
| User Auth | Basic sessions | django-allauth |
| API | Manual routes | Django REST Framework |
| File Structure | Single app.py | Organized app modules |

Your Django marketplace is now ready for development! 🎉