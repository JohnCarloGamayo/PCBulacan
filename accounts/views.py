from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .forms import SignUpForm, LoginForm, UserProfileForm
from .models import UserAddress
from orders.models import Order, OrderItem
from products.models import ProductReview
import os


def signup_view(request):
    """Handle user registration"""
    if request.user.is_authenticated:
        # Redirect based on user role
        if request.user.is_staff or request.user.is_superuser:
            return redirect('dashboard:home')
        return redirect('products:home')
    
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Account created successfully! Welcome to PCBulacan.')
            return redirect('products:home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = SignUpForm()
    
    return render(request, 'accounts/signup.html', {'form': form})


def login_view(request):
    """Handle user login"""
    if request.user.is_authenticated:
        # Redirect based on user role
        if request.user.is_staff or request.user.is_superuser:
            return redirect('dashboard:home')
        return redirect('products:home')
    
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            if user is not None:
                login(request, user)
                
                # Redirect based on user role
                if user.is_staff or user.is_superuser:
                    messages.success(request, f'Welcome back, Admin {user.get_full_name()}!')
                    return redirect('dashboard:home')
                else:
                    messages.success(request, f'Welcome back, {user.get_full_name()}!')
                    next_url = request.GET.get('next', 'products:home')
                    return redirect(next_url)
            else:
                messages.error(request, 'Invalid email or password.')
        else:
            messages.error(request, 'Invalid email or password.')
    else:
        form = LoginForm()
    
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    """Handle user logout"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('accounts:login')


@login_required
def profile_view(request):
    """Display and update user profile"""
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('accounts:profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    return render(request, 'accounts/profile.html', {'form': form})


@login_required
def account_view(request):
    """User account page with profile, addresses, and orders"""
    user = request.user
    
    # Handle form submissions
    if request.method == 'POST':
        form_type = request.POST.get('form_type')
        
        # Profile update
        if form_type == 'profile_update':
            first_name = request.POST.get('first_name', '').strip()
            last_name = request.POST.get('last_name', '').strip()
            email = request.POST.get('email', '').strip()
            phone = request.POST.get('phone', '').strip()
            
            # Validate
            if not first_name or not last_name or not email:
                messages.error(request, 'First name, last name, and email are required.')
            else:
                user.first_name = first_name
                user.last_name = last_name
                user.email = email
                user.phone = phone
                
                # Handle profile picture upload
                if 'profile_picture' in request.FILES:
                    # Delete old profile picture if exists
                    if user.profile_picture:
                        old_path = user.profile_picture.path
                        if os.path.exists(old_path):
                            os.remove(old_path)
                    user.profile_picture = request.FILES['profile_picture']
                
                user.save()
                messages.success(request, 'Profile updated successfully!')
                return redirect('accounts:account')
        
        # Password change
        elif form_type == 'password_change':
            current_password = request.POST.get('current_password', '')
            new_password = request.POST.get('new_password', '')
            confirm_password = request.POST.get('confirm_password', '')
            
            if not user.check_password(current_password):
                messages.error(request, 'Current password is incorrect.')
            elif len(new_password) < 8:
                messages.error(request, 'New password must be at least 8 characters long.')
            elif new_password != confirm_password:
                messages.error(request, 'New passwords do not match.')
            else:
                user.set_password(new_password)
                user.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'Password changed successfully!')
                return redirect('accounts:account')
        
        # Address update/add
        elif form_type == 'address_update':
            address_id = request.POST.get('address_id', 0)
            address_line1 = request.POST.get('address_line1', '').strip()
            address_line2 = request.POST.get('address_line2', '').strip()
            city = request.POST.get('city', '').strip()
            state = request.POST.get('state', '').strip()
            postal_code = request.POST.get('postal_code', '').strip()
            is_primary = request.POST.get('is_primary') == 'on'
            
            if not address_line1 or not city or not state or not postal_code:
                messages.error(request, 'Address line 1, city, state, and postal code are required.')
            else:
                try:
                    if int(address_id) > 0:
                        # Update existing address
                        address = UserAddress.objects.get(id=address_id, user=user)
                        address.address_line1 = address_line1
                        address.address_line2 = address_line2
                        address.city = city
                        address.state = state
                        address.postal_code = postal_code
                        address.is_primary = is_primary
                        address.save()
                        messages.success(request, 'Address updated successfully!')
                    else:
                        # Add new address
                        UserAddress.objects.create(
                            user=user,
                            address_line1=address_line1,
                            address_line2=address_line2,
                            city=city,
                            state=state,
                            postal_code=postal_code,
                            is_primary=is_primary
                        )
                        messages.success(request, 'Address added successfully!')
                    return redirect('accounts:account')
                except UserAddress.DoesNotExist:
                    messages.error(request, 'Address not found.')
        
        # Address delete
        elif form_type == 'address_delete':
            address_id = request.POST.get('address_id', 0)
            try:
                address = UserAddress.objects.get(id=address_id, user=user)
                address.delete()
                messages.success(request, 'Address deleted successfully!')
                return redirect('accounts:account')
            except UserAddress.DoesNotExist:
                messages.error(request, 'Address not found.')
    
    # Get user addresses
    addresses = UserAddress.objects.filter(user=user).order_by('-is_primary', '-created_at')
    
    # Get user orders with related items
    orders = Order.objects.filter(user=user).prefetch_related('items__product').order_by('-created_at')
    
    context = {
        'user': user,
        'addresses': addresses,
        'orders': orders,
    }
    
    return render(request, 'accounts/account.html', context)


@login_required
@require_POST
def cancel_order(request):
    """AJAX endpoint to cancel an order"""
    order_id = request.POST.get('order_id')
    
    try:
        order = Order.objects.get(id=order_id, user=request.user, status='pending')
        order.status = 'cancelled'
        order.save()
        
        return JsonResponse({
            'success': True,
            'message': f'Order #{order.order_number} has been cancelled successfully!'
        })
    except Order.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Order not found or cannot be cancelled.'
        })


@login_required
@require_POST
def mark_received(request):
    """AJAX endpoint to mark order as received"""
    order_id = request.POST.get('order_id')
    
    try:
        order = Order.objects.get(id=order_id, user=request.user, status='delivered')
        order.status = 'received'
        order.save()
        
        return JsonResponse({
            'success': True,
            'message': f'Order #{order.order_number} has been marked as received. Thank you!'
        })
    except Order.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Order not found or cannot be marked as received.'
        })


@login_required
def get_order_address(request):
    """AJAX endpoint to get order shipping address"""
    order_id = request.GET.get('order_id')
    
    try:
        order = Order.objects.get(id=order_id, user=request.user)
        
        if order.shipping_address:
            address = order.shipping_address
            address_data = {
                'address_line1': address.address_line1,
                'address_line2': address.address_line2 or '',
                'city': address.city,
                'state': address.state,
                'postal_code': address.postal_code,
            }
        else:
            # Fallback to order's direct address fields
            address_data = {
                'address_line1': order.address,
                'address_line2': '',
                'city': order.city,
                'state': order.state,
                'postal_code': order.zip_code,
            }
        
        return JsonResponse({
            'success': True,
            'address': address_data
        })
    except Order.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Order not found.'
        })


def send_reset_code(request):
    """Send 6-digit reset code to user's email"""
    import random
    from django.core.mail import send_mail
    from django.utils import timezone
    from datetime import timedelta
    from .models import User, PasswordResetCode
    
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        
        if not email:
            return JsonResponse({
                'success': False,
                'message': 'Please enter your email address.'
            })
        
        # Check if user exists
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'No account found with this email address.'
            })
        
        # Generate 6-digit code
        code = ''.join([str(random.randint(0, 9)) for _ in range(6)])
        
        # Set expiration time (10 minutes from now)
        expires_at = timezone.now() + timedelta(minutes=10)
        
        # Delete old unused codes for this email
        PasswordResetCode.objects.filter(email=email, is_used=False).delete()
        
        # Save new code
        reset_code = PasswordResetCode.objects.create(
            email=email,
            code=code,
            expires_at=expires_at
        )
        
        # Send email
        try:
            subject = 'PCBulacan - Password Reset Code'
            message = f'''Hello {user.get_full_name()},

You requested to reset your password for PCBulacan.

Your verification code is: {code}

This code will expire in 10 minutes.

If you didn't request this code, please ignore this email.

Best regards,
PCBulacan Team'''
            
            send_mail(
                subject,
                message,
                'PCBulacan <johncarlogamayo@gmail.com>',
                [email],
                fail_silently=False,
            )
            
            return JsonResponse({
                'success': True,
                'message': 'Verification code sent to your email.'
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'message': f'Failed to send email: {str(e)}'
            })
    
    return JsonResponse({
        'success': False,
        'message': 'Invalid request method.'
    })


def verify_reset_code(request):
    """Verify the 6-digit reset code"""
    from .models import PasswordResetCode
    
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        code = request.POST.get('code', '').strip()
        
        if not email or not code:
            return JsonResponse({
                'success': False,
                'message': 'Please enter the verification code.'
            })
        
        try:
            reset_code = PasswordResetCode.objects.get(
                email=email,
                code=code,
                is_used=False
            )
            
            if reset_code.is_valid():
                return JsonResponse({
                    'success': True,
                    'message': 'Code verified successfully.'
                })
            else:
                return JsonResponse({
                    'success': False,
                    'message': 'This code has expired. Please request a new one.'
                })
        except PasswordResetCode.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Invalid verification code.'
            })
    
    return JsonResponse({
        'success': False,
        'message': 'Invalid request method.'
    })


def reset_password(request):
    """Reset user password after code verification"""
    from .models import User, PasswordResetCode
    
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        code = request.POST.get('code', '').strip()
        new_password = request.POST.get('new_password', '').strip()
        confirm_password = request.POST.get('confirm_password', '').strip()
        
        if not all([email, code, new_password, confirm_password]):
            return JsonResponse({
                'success': False,
                'message': 'All fields are required.'
            })
        
        if new_password != confirm_password:
            return JsonResponse({
                'success': False,
                'message': 'Passwords do not match.'
            })
        
        if len(new_password) < 8:
            return JsonResponse({
                'success': False,
                'message': 'Password must be at least 8 characters long.'
            })
        
        try:
            # Verify code is still valid
            reset_code = PasswordResetCode.objects.get(
                email=email,
                code=code,
                is_used=False
            )
            
            if not reset_code.is_valid():
                return JsonResponse({
                    'success': False,
                    'message': 'This code has expired. Please request a new one.'
                })
            
            # Get user and update password
            user = User.objects.get(email=email)
            user.set_password(new_password)
            user.save()
            
            # Mark code as used
            reset_code.is_used = True
            reset_code.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Password reset successfully. You can now login with your new password.'
            })
        except PasswordResetCode.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Invalid verification code.'
            })
        except User.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'User not found.'
            })
    
    return JsonResponse({
        'success': False,
        'message': 'Invalid request method.'
    })


@login_required
@require_POST
def submit_product_ratings(request):
    """Submit product ratings after order is received"""
    try:
        order_id = request.POST.get('order_id')
        order = Order.objects.get(id=order_id, user=request.user)
        
        if order.status != 'received':
            return JsonResponse({
                'success': False,
                'message': 'You can only rate products from received orders.'
            })
        
        # Check if already rated
        existing_reviews = ProductReview.objects.filter(order=order, user=request.user)
        if existing_reviews.exists():
            return JsonResponse({
                'success': False,
                'message': 'You have already rated products from this order.'
            })
        
        # Get ratings from POST data
        ratings_submitted = 0
        for item in order.items.all():
            rating_key = f'rating_{item.product.id}'
            comment_key = f'comment_{item.product.id}'
            
            rating = request.POST.get(rating_key)
            comment = request.POST.get(comment_key, '')
            
            if rating:
                ProductReview.objects.create(
                    product=item.product,
                    user=request.user,
                    order=order,
                    rating=int(rating),
                    comment=comment
                )
                ratings_submitted += 1
        
        if ratings_submitted > 0:
            return JsonResponse({
                'success': True,
                'message': f'Thank you for rating {ratings_submitted} product(s)!'
            })
        else:
            return JsonResponse({
                'success': False,
                'message': 'No ratings were submitted.'
            })
    except Order.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Order not found.'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error submitting ratings: {str(e)}'
        })


@login_required
def get_order_items_for_rating(request):
    """Get order items for rating modal"""
    try:
        order_id = request.GET.get('order_id')
        order = Order.objects.get(id=order_id, user=request.user)
        
        # Check if already rated
        existing_reviews = ProductReview.objects.filter(order=order, user=request.user)
        if existing_reviews.exists():
            return JsonResponse({
                'success': False,
                'message': 'You have already rated products from this order.'
            })
        
        items = []
        for item in order.items.all():
            items.append({
                'id': item.product.id,
                'name': item.product.name,
                'image': item.product.image.url if item.product.image else '',
                'price': str(item.price),
                'quantity': item.quantity
            })
        
        return JsonResponse({
            'success': True,
            'order_number': order.order_number,
            'items': items
        })
    except Order.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Order not found.'
        })


@login_required
def get_notifications(request):
    """API endpoint to fetch user notifications"""
    from .models import Notification
    from django.utils.timesince import timesince
    from django.urls import reverse
    
    notifications = Notification.objects.filter(user=request.user).order_by('-created_at')[:20]
    unread_count = Notification.objects.filter(user=request.user, is_read=False).count()
    
    notifications_data = []
    for notif in notifications:
        # Get icon based on notification type
        icon_map = {
            'new_product': 'fas fa-box',
            'order_update': 'fas fa-shopping-bag',
            'new_deal': 'fas fa-tags',
            'order_shipped': 'fas fa-truck',
            'order_delivered': 'fas fa-check-circle',
            'system': 'fas fa-info-circle',
        }
        
        # Fix notification link - ensure it's a proper URL
        link = notif.link or '#'
        if link and link != '#':
            # Fix common URL mistakes
            if link == '/account/':
                link = reverse('accounts:account')
            elif link == '/profile/':
                link = reverse('accounts:profile')
            elif not link.startswith('/'):
                link = '/' + link
        
        notifications_data.append({
            'id': notif.id,
            'type': notif.notification_type,
            'title': notif.title,
            'message': notif.message,
            'link': link,
            'icon': icon_map.get(notif.notification_type, 'fas fa-bell'),
            'is_read': notif.is_read,
            'time_ago': timesince(notif.created_at) + ' ago',
            'created_at': notif.created_at.strftime('%Y-%m-%d %H:%M:%S')
        })
    
    return JsonResponse({
        'success': True,
        'notifications': notifications_data,
        'unread_count': unread_count
    })


@login_required
@require_POST
def mark_notification_read(request, notification_id):
    """Mark a notification as read"""
    from .models import Notification
    
    try:
        notification = Notification.objects.get(id=notification_id, user=request.user)
        notification.is_read = True
        notification.save()
        
        unread_count = Notification.objects.filter(user=request.user, is_read=False).count()
        
        return JsonResponse({
            'success': True,
            'unread_count': unread_count
        })
    except Notification.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Notification not found.'
        })


@login_required
@require_POST
def mark_all_notifications_read(request):
    """Mark all notifications as read"""
    from .models import Notification
    
    Notification.objects.filter(user=request.user, is_read=False).update(is_read=True)
    
    return JsonResponse({
        'success': True,
        'unread_count': 0
    })
