# Notification System Documentation

## Overview
The PCBulacan notification system provides real-time alerts to users about new products, order updates, and deals. Notifications appear in the navigation bar with a badge counter.

## Features

### 1. **Automatic Notifications** 🔔
The system automatically creates notifications when:
- **New Products** are added (visible to all users)
- **New Deals** are created or activated (visible to all users)
- **Orders** are created or status changes (visible to order owner only)

### 2. **Notification Types**
```python
NOTIFICATION_TYPES = [
    ('new_product', 'New Product'),      # Blue icon
    ('order_update', 'Order Update'),     # Green icon
    ('new_deal', 'New Deal'),            # Red icon
    ('order_shipped', 'Order Shipped'),   # Green icon
    ('order_delivered', 'Order Delivered'), # Green icon
    ('system', 'System Notification'),    # Purple icon
]
```

### 3. **Real-Time Updates** ⏱️
- Notifications are fetched on page load
- Auto-refresh every 30 seconds
- Manual refresh when opening dropdown
- Badge shows unread count

### 4. **User Actions**
- Click notification → Mark as read + redirect to link
- "Mark all as read" button
- Unread notifications highlighted in blue
- Read notifications appear gray

---

## Database Schema

### Notification Model
```python
class Notification(models.Model):
    user = ForeignKey(User)              # Notification recipient
    notification_type = CharField         # Type of notification
    title = CharField(max_length=200)    # Notification title
    message = TextField                   # Notification message
    link = CharField                      # URL to redirect
    is_read = BooleanField(default=False) # Read status
    created_at = DateTimeField            # Creation timestamp
    
    # Optional references
    product_id = IntegerField(blank=True)
    order_id = IntegerField(blank=True)
    deal_id = IntegerField(blank=True)
```

---

## Signal Handlers

### 1. New Product Notification
**Trigger:** When a new product is created and `is_active=True`

```python
@receiver(post_save, sender=Product)
def create_new_product_notification(sender, instance, created, **kwargs):
    if created and instance.is_active:
        # Create notification for ALL active users
        users = User.objects.filter(is_active=True, is_staff=False)
        # Bulk create notifications
```

**Notification Details:**
- Title: "New Product: {product_name}"
- Message: "Check out our new product: {name} at ₱{price}!"
- Link: `/product/{slug}/`
- Type: `new_product`

### 2. New Deal Notification
**Trigger:** When a new deal is created OR activated

```python
@receiver(post_save, sender=Deal)
def create_new_deal_notification(sender, instance, created, **kwargs):
    if (created or instance.status == 'active') and instance.is_active():
        # Create notification for ALL active users
```

**Notification Details:**
- Title: "New Deal: {deal_title}"
- Message: "{description} - {discount}"
- Link: `/deals/`
- Type: `new_deal`

### 3. Order Update Notification
**Trigger:** When order is created OR status changes

```python
@receiver(post_save, sender=Order)
def create_order_update_notification(sender, instance, created, update_fields, **kwargs):
    # For new orders or status updates
```

**Notification Details (Status Change):**
- **Pending:** "Your order is pending confirmation."
- **Processing:** "Your order is being processed!"
- **Shipped:** "Your order has been shipped! 📦"
- **Delivered:** "Your order has been delivered! 🎉"
- **Received:** "Thank you for confirming receipt!"
- **Cancelled:** "Your order has been cancelled."

---

## API Endpoints

### 1. Get Notifications
**Endpoint:** `GET /api/notifications/`  
**Auth:** Required  
**Description:** Fetch user's latest 20 notifications

**Response:**
```json
{
  "success": true,
  "notifications": [
    {
      "id": 1,
      "type": "new_product",
      "title": "New Product: AMD Ryzen 9",
      "message": "Check out our new product...",
      "link": "/products/",
      "icon": "fas fa-box",
      "is_read": false,
      "time_ago": "5 minutes ago",
      "created_at": "2025-10-27 14:00:00"
    }
  ],
  "unread_count": 3
}
```

### 2. Mark Notification as Read
**Endpoint:** `POST /api/notifications/<id>/read/`  
**Auth:** Required  
**Description:** Mark single notification as read

**Response:**
```json
{
  "success": true,
  "unread_count": 2
}
```

### 3. Mark All as Read
**Endpoint:** `POST /api/notifications/mark-all-read/`  
**Auth:** Required  
**Description:** Mark all user's notifications as read

**Response:**
```json
{
  "success": true,
  "unread_count": 0
}
```

---

## Frontend Implementation

### HTML Structure (in header.html)
```html
<div class="notification-container">
    <button class="icon-btn notification-btn" id="notificationBtn">
        <i class="fas fa-bell"></i>
        <span class="notification-count">5</span>
    </button>
    <div class="notification-dropdown" id="notificationDropdown">
        <div class="notification-header">
            <h4>Notifications</h4>
            <a href="#">See All</a>
        </div>
        <div class="notification-list" id="notificationList">
            <!-- Notifications dynamically inserted here -->
        </div>
        <div class="notification-footer">
            <a href="#" id="markAllRead">Mark all as read</a>
        </div>
    </div>
</div>
```

### JavaScript Functions

#### fetchNotifications()
Fetches notifications from API and displays them
```javascript
function fetchNotifications() {
    fetch('/api/notifications/')
        .then(response => response.json())
        .then(data => {
            updateNotificationCount(data.unread_count);
            displayNotifications(data.notifications);
        });
}
```

#### updateNotificationCount()
Updates the badge counter
```javascript
function updateNotificationCount(count) {
    if (count > 0) {
        notificationCount.textContent = count > 99 ? '99+' : count;
        notificationCount.style.display = 'flex';
    } else {
        notificationCount.style.display = 'none';
    }
}
```

#### displayNotifications()
Renders notifications in dropdown
```javascript
function displayNotifications(notifications) {
    notificationList.innerHTML = '';
    notifications.forEach(notif => {
        const notifElement = createNotificationElement(notif);
        notificationList.appendChild(notifElement);
    });
}
```

#### markAsRead()
Marks notification as read via API
```javascript
function markAsRead(notificationId) {
    fetch(`/api/notifications/${notificationId}/read/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        }
    });
}
```

---

## CSS Styling

### Notification Badge
```css
.notification-count {
    position: absolute;
    top: -5px;
    right: -5px;
    background-color: #ef4444;  /* Red */
    color: white;
    border-radius: 50%;
    width: 18px;
    height: 18px;
    font-size: 11px;
    display: flex;
    align-items: center;
    justify-content: center;
}
```

### Notification Item Icons (by Type)
```css
.notification-icon.new_product {
    background-color: #dbeafe;  /* Light blue */
    color: #2563eb;             /* Blue */
}

.notification-icon.order_update,
.notification-icon.order_shipped,
.notification-icon.order_delivered {
    background-color: #dcfce7;  /* Light green */
    color: #16a34a;             /* Green */
}

.notification-icon.new_deal {
    background-color: #fee2e2;  /* Light red */
    color: #dc2626;             /* Red */
}
```

### Unread Notification
```css
.notification-item.unread {
    background-color: #ebf8ff;  /* Light blue background */
}

.notification-item.unread .notification-title {
    font-weight: 700;           /* Bold title */
}
```

---

## Testing

### Create Sample Notifications
Run the provided script to create test notifications:
```bash
python create_sample_notifications.py
```

This creates 5 sample notifications for each non-staff user:
1. New Product: AMD Ryzen 9 7950X
2. Flash Sale: Up to 50% OFF!
3. Your order is being processed
4. New Product: NVIDIA RTX 4090
5. Your order has been shipped!

### Manual Testing Steps

#### Test 1: New Product Notification
1. Go to Django Admin → Products
2. Add a new product with `is_active=True`
3. Check notification bell in nav bar
4. Should see new notification with blue icon

#### Test 2: New Deal Notification
1. Go to Django Admin → Deals
2. Create a new deal with `status=active`
3. Check notification bell
4. Should see new notification with red icon

#### Test 3: Order Update Notification
1. Go to Django Admin → Orders
2. Change order status (e.g., pending → shipped)
3. Check notification for that user
4. Should see order update with green icon

#### Test 4: Mark as Read
1. Click on notification bell
2. Click on any unread notification
3. Badge count should decrease
4. Background should change from blue to white

#### Test 5: Mark All as Read
1. Click notification bell with unread notifications
2. Click "Mark all as read" button
3. Badge should disappear
4. All notifications should appear as read

---

## Configuration

### Auto-Refresh Interval
Change refresh frequency in header.html:
```javascript
// Refresh every 30 seconds (30000ms)
setInterval(fetchNotifications, 30000);

// Change to 60 seconds:
setInterval(fetchNotifications, 60000);
```

### Notification Limit
Change number of notifications fetched:
```python
# In accounts/views.py -> get_notifications()
notifications = Notification.objects.filter(user=request.user).order_by('-created_at')[:20]

# Change to 50:
notifications = Notification.objects.filter(user=request.user).order_by('-created_at')[:50]
```

### Notification Recipients
To change who receives notifications:

**All Users (including staff):**
```python
users = User.objects.filter(is_active=True)
```

**Only Premium Users (if you have premium field):**
```python
users = User.objects.filter(is_active=True, is_premium=True)
```

---

## Admin Management

### View Notifications
1. Go to Django Admin: http://127.0.0.1:8000/admin/
2. Click "Notifications" under ACCOUNTS
3. View all notifications with filters:
   - Type (new_product, order_update, etc.)
   - Read status
   - Date

### Bulk Actions
Select multiple notifications and:
- Mark as read
- Mark as unread
- Delete

### Create Manual Notification
1. Click "Add Notification"
2. Select user
3. Choose notification type
4. Enter title and message
5. Add optional link
6. Save

---

## Database Queries

### Get Unread Count
```python
unread_count = Notification.objects.filter(
    user=request.user,
    is_read=False
).count()
```

### Get Recent Notifications
```python
recent = Notification.objects.filter(
    user=request.user
).order_by('-created_at')[:10]
```

### Get Notifications by Type
```python
product_notifs = Notification.objects.filter(
    user=request.user,
    notification_type='new_product'
)
```

### Mark All as Read
```python
Notification.objects.filter(
    user=request.user,
    is_read=False
).update(is_read=True)
```

### Delete Old Notifications (30+ days)
```python
from django.utils import timezone
from datetime import timedelta

old_date = timezone.now() - timedelta(days=30)
Notification.objects.filter(created_at__lt=old_date).delete()
```

---

## Troubleshooting

### Badge Not Showing
**Issue:** Notification badge not visible  
**Solution:**
1. Check if user is authenticated
2. Check console for JavaScript errors
3. Verify API endpoint returns data
4. Clear browser cache

### Notifications Not Creating
**Issue:** No notifications when adding products/deals  
**Solution:**
1. Check if signals are registered in apps.py
2. Verify `ready()` method imports signals
3. Check product `is_active=True`
4. Check deal `status='active'`

### API Returns 403 Forbidden
**Issue:** API calls fail with 403  
**Solution:**
1. Check CSRF token in JavaScript
2. Verify user is logged in
3. Check URL paths match

### Dropdown Not Opening
**Issue:** Click on bell but dropdown doesn't appear  
**Solution:**
1. Check JavaScript loaded
2. Verify element IDs match
3. Check z-index of dropdown
4. Inspect browser console for errors

---

## Future Enhancements

### Planned Features
1. **Push Notifications** - Browser push notifications
2. **Email Notifications** - Send email for important updates
3. **Notification Preferences** - Let users choose what to receive
4. **Read Receipts** - Track when notifications are opened
5. **Action Buttons** - Quick actions in notifications (e.g., "View Order")
6. **Notification History** - Dedicated page for all notifications
7. **Mark as Important** - Pin important notifications
8. **Notification Categories** - Group by category (Orders, Products, Deals)

### Optimization Ideas
1. **Pagination** - Load more on scroll
2. **Caching** - Cache notification count
3. **WebSockets** - Real-time push without polling
4. **Batch Operations** - Delete multiple notifications
5. **Archive** - Archive old notifications instead of delete

---

## Files Modified

### New Files Created
- `accounts/signals.py` - Signal handlers for auto-notifications
- `accounts/migrations/0006_notification.py` - Notification model migration
- `create_sample_notifications.py` - Test data script

### Modified Files
- `accounts/models.py` - Added Notification model
- `accounts/admin.py` - Added NotificationAdmin
- `accounts/views.py` - Added API endpoints
- `accounts/urls.py` - Added notification routes
- `accounts/apps.py` - Registered signals
- `templates/includes/header.html` - Added notification UI & JavaScript
- `static/css/styles.css` - Added notification styles

---

## Summary

The notification system is now fully functional with:
✅ Automatic notifications for products, deals, and orders
✅ Real-time badge counter with unread count
✅ Dropdown with notification list
✅ Mark as read functionality
✅ Color-coded icons by type
✅ Admin panel management
✅ API endpoints for AJAX requests
✅ Auto-refresh every 30 seconds
✅ Sample data script for testing

**Test it by:**
1. Login as a regular user
2. Check the bell icon in navigation
3. Click to see notifications
4. Click on a notification to mark as read
5. Use "Mark all as read" button

**Or create new notifications by:**
- Adding a new product in admin
- Creating a new deal in admin
- Updating an order status
