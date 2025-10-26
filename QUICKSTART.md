# PCBulacan - Quick Start Guide

## ✅ Project Successfully Created!

Your Django e-commerce application has been successfully converted from PHP and is now running!

## 🚀 Current Status

- ✅ Django 5.2.7 installed
- ✅ All apps created (accounts, products, orders, dashboard)
- ✅ Database configured (SQLite for development)
- ✅ All migrations applied
- ✅ Development server running on http://localhost:8000

## 🔐 Next Steps

### 1. Create a Superuser Account

To access the admin panel, create a superuser:

```powershell
cd "c:\xampp\htdocs\cyberzone - Copy\PCbulacan"
& "C:/Users/John Carlo Gamayo/AppData/Local/Programs/Python/Python313/python.exe" manage.py createsuperuser
```

Follow the prompts to enter:
- Email address
- First name
- Last name
- Password (twice)

### 2. Access the Application

**Main Site**: http://localhost:8000
- You'll need to sign up first as a regular user
- After signup, you'll be redirected to the home page

**Django Admin Panel**: http://localhost:8000/admin
- Login with your superuser credentials
- Manage all data from here

**Admin Dashboard**: http://localhost:8000/dashboard/
- Login as staff user to access
- Custom dashboard for managing products, users, orders

### 3. Add Sample Data

#### Option A: Via Django Admin Panel
1. Go to http://localhost:8000/admin
2. Add Categories (e.g., "Processors", "Graphics Cards", "Memory")
3. Add Products with images and details
4. Add Carousel Slides for homepage

#### Option B: Via Admin Dashboard
1. Go to http://localhost:8000/dashboard/
2. Use the custom interface to manage:
   - Categories
   - Products
   - Orders
   - Users

## 📁 Project Structure

```
PCbulacan/
├── accounts/           # User authentication
├── products/           # Product catalog
├── orders/             # Cart and checkout
├── dashboard/          # Admin dashboard
├── templates/          # HTML templates
├── static/             # CSS, JS files
├── media/              # Uploaded images
├── db.sqlite3          # Database file
└── manage.py           # Django CLI
```

## 🎨 Features Implemented

### Customer Features
- ✅ Email-based authentication
- ✅ User registration and login
- ✅ Profile management
- ✅ Browse products by category
- ✅ Search and filter products
- ✅ Shopping cart
- ✅ Checkout process
- ✅ Order tracking
- ✅ Product ratings and reviews (display)

### Admin Features
- ✅ Dashboard with statistics
- ✅ User management
- ✅ Product management (CRUD)
- ✅ Category management
- ✅ Order management
- ✅ Stock tracking
- ✅ Sales reports

### Technical Features
- ✅ Custom User model (email-based)
- ✅ Django admin customization
- ✅ Context processors for cart
- ✅ Form validation
- ✅ Session management
- ✅ CSRF protection
- ✅ Responsive design

## 🛠️ Common Commands

### Start Development Server
```powershell
cd "c:\xampp\htdocs\cyberzone - Copy\PCbulacan"
& "C:/Users/John Carlo Gamayo/AppData/Local/Programs/Python/Python313/python.exe" manage.py runserver
```

### Create Migrations
```powershell
& "C:/Users/John Carlo Gamayo/AppData/Local/Programs/Python/Python313/python.exe" manage.py makemigrations
```

### Apply Migrations
```powershell
& "C:/Users/John Carlo Gamayo/AppData/Local/Programs/Python/Python313/python.exe" manage.py migrate
```

### Collect Static Files
```powershell
& "C:/Users/John Carlo Gamayo/AppData/Local/Programs/Python/Python313/python.exe" manage.py collectstatic
```

### Create Superuser
```powershell
& "C:/Users/John Carlo Gamayo/AppData/Local/Programs/Python/Python313/python.exe" manage.py createsuperuser
```

## 🔄 Switching to MySQL

To use MySQL instead of SQLite:

1. **Install mysqlclient**:
   ```powershell
   pip install mysqlclient
   ```

2. **Create MySQL database**:
   ```sql
   CREATE DATABASE pcbulacan_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

3. **Update `.env` file**:
   ```
   DB_NAME=pcbulacan_db
   DB_USER=root
   DB_PASSWORD=your_password
   DB_HOST=localhost
   DB_PORT=3306
   ```

4. **Update `settings.py`**:
   - Comment out SQLite configuration
   - Uncomment MySQL configuration

5. **Run migrations**:
   ```powershell
   & "C:/Users/John Carlo Gamayo/AppData/Local/Programs/Python/Python313/python.exe" manage.py migrate
   ```

## 📝 Default URLs

| Page | URL | Login Required |
|------|-----|----------------|
| Home | `/` | Yes |
| Products | `/products/` | Yes |
| Product Detail | `/product/<slug>/` | Yes |
| Cart | `/orders/cart/` | Yes |
| Checkout | `/orders/checkout/` | Yes |
| My Orders | `/orders/orders/` | Yes |
| Login | `/accounts/login/` | No |
| Signup | `/accounts/signup/` | No |
| Profile | `/accounts/profile/` | Yes |
| Dashboard | `/dashboard/` | Staff Only |
| Django Admin | `/admin/` | Superuser |

## 🎯 Testing the Application

1. **Sign up** as a new user at http://localhost:8000/accounts/signup/
2. **Add categories** via Django admin
3. **Add products** via Django admin or dashboard
4. **Browse products** on the home page
5. **Add to cart** and complete checkout
6. **View orders** in "My Orders"

## 🐛 Troubleshooting

### Server not starting?
- Check if port 8000 is already in use
- Try: `python manage.py runserver 8080`

### Static files not loading?
- Run: `python manage.py collectstatic`
- Check STATIC_URL in settings.py

### Database errors?
- Delete `db.sqlite3` and run migrations again
- Check database configuration in settings.py

### Import errors?
- Activate virtual environment if using one
- Reinstall requirements: `pip install -r requirements.txt`

## 📚 Additional Resources

- Django Documentation: https://docs.djangoproject.com/
- Bootstrap 5: https://getbootstrap.com/docs/5.3/
- Font Awesome: https://fontawesome.com/icons

## 🎉 Success!

Your PHP application has been successfully converted to Django!

**Development server is running at**: http://localhost:8000

Start by creating a superuser account and adding sample data.

---

**Need Help?** Check the README.md for detailed documentation.
