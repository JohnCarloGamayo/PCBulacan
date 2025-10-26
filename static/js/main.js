// PCBulacan Main JavaScript

document.addEventListener('DOMContentLoaded', function() {
    console.log('PCBulacan loaded successfully!');

    // Mobile menu toggle for admin
    const mobileMenuToggle = document.getElementById('mobileMenuToggle');
    const sidebar = document.querySelector('.admin-sidebar');
    const sidebarOverlay = document.getElementById('sidebarOverlay');

    if (mobileMenuToggle) {
        mobileMenuToggle.addEventListener('click', function() {
            sidebar?.classList.toggle('active');
            sidebarOverlay?.classList.toggle('active');
        });
    }

    // Close sidebar when clicking overlay
    if (sidebarOverlay) {
        sidebarOverlay.addEventListener('click', function() {
            sidebar?.classList.remove('active');
            sidebarOverlay?.classList.remove('active');
        });
    }

    // Close sidebar when clicking a menu item on mobile
    document.querySelectorAll('.menu-item').forEach(item => {
        item.addEventListener('click', function() {
            if (window.innerWidth <= 992) {
                sidebar?.classList.remove('active');
                sidebarOverlay?.classList.remove('active');
            }
        });
    });

    // Auto-hide messages after 5 seconds
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        setTimeout(() => {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        }, 5000);
    });

    // Confirm before deleting
    const deleteButtons = document.querySelectorAll('[data-confirm-delete]');
    deleteButtons.forEach(button => {
        button.addEventListener('click', function(e) {
            if (!confirm('Are you sure you want to delete this item?')) {
                e.preventDefault();
            }
        });
    });

    // User dropdown: show on hover (mouseenter/mouseleave)
    document.querySelectorAll('.dropdown').forEach(dropdown => {
        dropdown.addEventListener('mouseenter', function() {
            this.classList.add('active');
        });
        dropdown.addEventListener('mouseleave', function() {
            this.classList.remove('active');
        });
    });
});
