# PCBulacan - First Time Setup

## ✅ Issues Fixed

1. **Template Error Fixed**: Moved `{% load static %}` to the top of base.html
2. **All templates are now working correctly**
3. **Server is running on**: http://localhost:8000

## 🚀 Getting Started (3 Simple Steps)

### Step 1: Access the Application

Open your browser and go to: **http://localhost:8000**

You'll be redirected to the login page since you need to be logged in.

### Step 2: Create Your First Account

1. Click **"Sign up here"** on the login page
2. Fill in the registration form:
   - First Name
   - Last Name
   - Email
   - Phone (optional)
   - Password
   - Confirm Password
3. Click **"Sign Up"**
4. You'll be automatically logged in and redirected to the home page

### Step 3: Create an Admin Account

To access the admin panel and dashboard, create a superuser:

```powershell
cd "c:\xampp\htdocs\cyberzone - Copy\PCbulacan"
& "C:/Users/John Carlo Gamayo/AppData/Local/Programs/Python/Python313/python.exe" manage.py createsuperuser
```

**Follow the prompts:**
```
Email address: admin@pcbulacan.com
First name: Admin
Last name: User
Password: ********
Password (again): ********
```

## 🎯 Access Points

| What | URL | Notes |
|------|-----|-------|
| **Login Page** | http://localhost:8000/accounts/login/ | Public access |
| **Sign Up** | http://localhost:8000/accounts/signup/ | Create new account |
| **Home Page** | http://localhost:8000/ | Requires login |
| **Products** | http://localhost:8000/products/ | Requires login |
| **Cart** | http://localhost:8000/orders/cart/ | Requires login |
| **My Profile** | http://localhost:8000/accounts/profile/ | Requires login |
| **My Orders** | http://localhost:8000/orders/orders/ | Requires login |
| **Admin Dashboard** | http://localhost:8000/dashboard/ | Staff only |
| **Django Admin** | http://localhost:8000/admin/ | Superuser only |

## 📦 Adding Your First Products

### Via Django Admin (Recommended for bulk import)

1. Go to http://localhost:8000/admin/
2. Login with superuser credentials
3. **Add Categories:**
   - Click "Categories" → "Add Category"
   - Add: Processors, Graphics Cards, Memory, Storage, etc.
4. **Add Products:**
   - Click "Products" → "Add Product"
   - Fill in: Name, Category, Description, Price, Stock
   - Upload product image
   - Set: Featured, New, or On Sale badges
   - Save

### Via Admin Dashboard (User-friendly interface)

1. Go to http://localhost:8000/dashboard/
2. Login with staff credentials
3. Navigate to **"Products"** → **"Add Product"**
4. Fill in product details and save

## 🛒 Testing the Full Workflow

1. **Sign up** as a customer
2. **Browse products** on home page
3. **View product details** by clicking a product
4. **Add to cart** using the cart button
5. **View cart** - adjust quantities
6. **Checkout** - fill in shipping details
7. **View order** in "My Orders"

## 📊 Admin Workflow

1. **Login as admin** to dashboard
2. **Add categories** for organization
3. **Add products** with details and images
4. **Manage orders** - update status
5. **View statistics** on dashboard home
6. **Manage users** - activate/deactivate accounts

## 🎨 Customization

### Change Site Branding
Edit these files:
- `templates/includes/header.html` - Change logo and navigation
- `templates/includes/footer.html` - Update footer content
- `static/css/styles.css` - Modify colors and styles

### Change Color Scheme
Edit `static/css/styles.css`:
```css
:root {
    --primary-color: #1e3a8a;  /* Change this */
    --secondary-color: #3b82f6;
    /* ... other colors */
}
```

### Add More Payment Methods
Edit `orders/models.py` - Order model:
```python
PAYMENT_CHOICES = [
    ('cod', 'Cash on Delivery'),
    ('card', 'Credit/Debit Card'),
    ('paypal', 'PayPal'),
    ('gcash', 'GCash'),
    # Add more here
]
```

## 🔧 Common Tasks

### Restart the Server
If you stopped the server, restart it:
```powershell
cd "c:\xampp\htdocs\cyberzone - Copy\PCbulacan"
& "C:/Users/John Carlo Gamayo/AppData/Local/Programs/Python/Python313/python.exe" manage.py runserver
```

### Clear All Data (Reset)
```powershell
# Delete database
Remove-Item db.sqlite3

# Recreate database
& "C:/Users/John Carlo Gamayo/AppData/Local/Programs/Python/Python313/python.exe" manage.py migrate

# Create new superuser
& "C:/Users/John Carlo Gamayo/AppData/Local/Programs/Python/Python313/python.exe" manage.py createsuperuser
```

### Backup Database
```powershell
# Copy the database file
Copy-Item db.sqlite3 db.sqlite3.backup
```

### Make Someone Staff
Via Django Admin:
1. Go to http://localhost:8000/admin/accounts/user/
2. Find the user
3. Check "Staff status"
4. Save

## ✅ Current Status

- ✅ Server running on port 8000
- ✅ All templates fixed and working
- ✅ Database migrations applied
- ✅ Ready to create users and add products
- ✅ Authentication system working
- ✅ Shopping cart functional
- ✅ Admin dashboard ready

## 🎉 You're All Set!

Your Django e-commerce platform is ready to use!

**Next step:** Go to http://localhost:8000/accounts/signup/ and create your first account!

---

Need help? Check:
- **QUICKSTART.md** - Detailed quick start guide  
- **README.md** - Complete documentation
- Django docs: https://docs.djangoproject.com/
