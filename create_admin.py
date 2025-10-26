import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pcbulacan.settings')
django.setup()

from accounts.models import User

# Create superuser
email = 'admin@pcbulacan.com'
first_name = 'Admin'
last_name = 'User'
password = 'admin123'

# Check if user already exists
if User.objects.filter(email=email).exists():
    print(f'User with email {email} already exists!')
    user = User.objects.get(email=email)
    user.is_staff = True
    user.is_superuser = True
    user.save()
    print('User updated to superuser!')
else:
    user = User.objects.create_superuser(
        email=email,
        first_name=first_name,
        last_name=last_name,
        password=password
    )
    print(f'Superuser created successfully!')
    print(f'Email: {email}')
    print(f'Password: admin123')
