# PCBulacan - Django E-commerce Platform

A modern e-commerce platform for PC components built with Django, converted from PHP.

## Features

- **User Authentication**: Signup, login, and profile management with email-based authentication
- **Product Management**: Browse, search, and filter products by category
- **Shopping Cart**: Add products to cart, update quantities, and manage items
- **Order System**: Complete checkout process with order tracking
- **Admin Dashboard**: Comprehensive admin interface for managing:
  - Users
  - Products
  - Categories
  - Orders
  - Statistics and reports
- **Responsive Design**: Mobile-friendly interface with Bootstrap 5
- **Modern UI**: Clean, professional design with smooth animations

## Technology Stack

- **Backend**: Django 5.0+
- **Database**: MySQL
- **Frontend**: Bootstrap 5, Font Awesome 6, JavaScript/jQuery
- **Python**: 3.10+

## Project Structure

```
PCbulacan/
├── accounts/           # User authentication and management
├── products/           # Product catalog and management
├── orders/             # Shopping cart and checkout
├── dashboard/          # Admin dashboard
├── pcbulacan/          # Project settings
├── static/             # CSS, JS, images
├── templates/          # HTML templates
│   ├── accounts/       # Auth templates
│   ├── products/       # Product templates
│   ├── orders/         # Cart and checkout templates
│   ├── dashboard/      # Admin templates
│   └── includes/       # Header, footer, etc.
├── media/              # User-uploaded files
├── manage.py           # Django management script
└── requirements.txt    # Python dependencies
```

## Installation

### Prerequisites

- Python 3.10 or higher
- MySQL Server
- pip (Python package manager)

### Setup Steps

1. **Clone or navigate to the project directory**:
   ```bash
   cd "c:\xampp\htdocs\cyberzone - Copy\PCbulacan"
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**:
   - Windows (PowerShell):
     ```powershell
     .\venv\Scripts\Activate.ps1
     ```
   - Windows (CMD):
     ```cmd
     venv\Scripts\activate.bat
     ```

4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Create MySQL database**:
   ```sql
   CREATE DATABASE pcbulacan_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

6. **Configure environment variables**:
   - Copy `.env.example` to `.env`
   - Update the database settings:
   ```
   DB_NAME=pcbulacan_db
   DB_USER=root
   DB_PASSWORD=your_password
   DB_HOST=localhost
   DB_PORT=3306
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   ```

7. **Run migrations**:
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

8. **Create superuser**:
   ```bash
   python manage.py createsuperuser
   ```
   Follow the prompts to create an admin account.

9. **Collect static files**:
   ```bash
   python manage.py collectstatic --noinput
   ```

10. **Run the development server**:
    ```bash
    python manage.py runserver
    ```

11. **Access the application**:
    - Main site: http://localhost:8000
    - Admin panel: http://localhost:8000/admin
    - Login with your superuser credentials

## Usage

### Customer Access

1. **Register**: Create a new account at `/accounts/signup/`
2. **Login**: Sign in at `/accounts/login/`
3. **Browse Products**: View products on the homepage or products page
4. **Add to Cart**: Click the cart icon on product cards
5. **Checkout**: Go to cart and complete checkout process
6. **Track Orders**: View order history in "My Orders"

### Admin Access

1. **Login**: Use staff/superuser credentials
2. **Access Dashboard**: Navigate to `/dashboard/`
3. **Manage**:
   - Users: Activate/deactivate accounts
   - Products: Add, edit, delete products
   - Categories: Organize product categories
   - Orders: Update order status

### Django Admin Panel

Access the full Django admin at `/admin/` for complete control over:
- All models and data
- User permissions
- Groups and authentication
- Site configuration

## Key Apps

### Accounts
- Custom user model with email authentication
- Profile management
- User activation/deactivation

### Products
- Product catalog with categories
- Search and filtering
- Product ratings and reviews
- Featured/New/Sale badges

### Orders
- Shopping cart functionality
- Checkout process
- Order tracking
- Stock management

### Dashboard
- Sales statistics
- User management
- Product management
- Order management
- Reports and analytics

## Database Models

### User
- Email-based authentication
- Profile information (name, phone, address)
- Staff and superuser permissions

### Product
- Name, description, price
- Category association
- Stock tracking
- Images and badges (featured, new, sale)

### Category
- Product categorization
- Hierarchical structure
- Active/inactive status

### Order & OrderItem
- Customer information
- Order items and quantities
- Payment method
- Order status tracking

### Cart & CartItem
- Session-based cart
- Quantity management
- Price calculations

## Configuration

### Settings (`pcbulacan/settings.py`)

Key settings to configure:
- `SECRET_KEY`: Django secret key (set in .env)
- `DEBUG`: Debug mode (False in production)
- `ALLOWED_HOSTS`: Allowed domain names
- `DATABASES`: MySQL connection settings
- `STATIC_URL` & `MEDIA_URL`: Static and media file paths

### URL Configuration

- `/` - Homepage
- `/products/` - Product listing
- `/product/<slug>/` - Product detail
- `/accounts/` - Authentication
- `/orders/` - Cart and checkout
- `/dashboard/` - Admin dashboard
- `/admin/` - Django admin panel

## Development

### Adding New Products

1. Via Admin Dashboard:
   - Go to `/dashboard/products/`
   - Click "Add Product"
   - Fill in details and upload image

2. Via Django Admin:
   - Go to `/admin/products/product/`
   - Click "Add Product"

### Creating Categories

1. Via Dashboard:
   - Go to `/dashboard/categories/`
   - Click "Add Category"

2. Via Django Admin:
   - Go to `/admin/products/category/`

## Production Deployment

Before deploying to production:

1. Set `DEBUG = False` in settings
2. Configure `ALLOWED_HOSTS`
3. Use a strong `SECRET_KEY`
4. Configure static files serving
5. Set up proper database credentials
6. Use environment variables for sensitive data
7. Configure HTTPS/SSL
8. Set up proper logging
9. Configure email backend
10. Use production-grade server (Gunicorn, uWSGI)

## Troubleshooting

### Database Connection Issues
- Verify MySQL is running
- Check database credentials in `.env`
- Ensure database exists

### Static Files Not Loading
- Run `python manage.py collectstatic`
- Check `STATIC_URL` and `STATIC_ROOT` settings

### Import Errors
- Activate virtual environment
- Reinstall requirements: `pip install -r requirements.txt`

### Migration Issues
- Delete migration files (except `__init__.py`)
- Drop database and recreate
- Run migrations again

## License

This project is proprietary software for PCBulacan.

## Support

For support, please contact: info@pcbulacan.com

## Credits

- Developed with Django Framework
- UI: Bootstrap 5
- Icons: Font Awesome 6
- Converted from PHP to Django

---

**PCBulacan** - Your trusted source for quality PC components
