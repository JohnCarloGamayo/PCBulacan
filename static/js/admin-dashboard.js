// Admin Dashboard JavaScript

// Sidebar toggle
document.getElementById('sidebarToggle')?.addEventListener('click', function() {
    document.querySelector('.admin-sidebar').classList.toggle('active');
});

// Mobile menu toggle
document.getElementById('mobileMenuToggle')?.addEventListener('click', function() {
    const sidebar = document.querySelector('.admin-sidebar');
    const overlay = document.getElementById('sidebarOverlay');
    sidebar.classList.toggle('active');
    overlay.classList.toggle('active');
});

// Close sidebar when clicking overlay
document.getElementById('sidebarOverlay')?.addEventListener('click', function() {
    const sidebar = document.querySelector('.admin-sidebar');
    const overlay = document.getElementById('sidebarOverlay');
    sidebar.classList.remove('active');
    overlay.classList.remove('active');
});

// Close sidebar when clicking a menu item on mobile
document.querySelectorAll('.menu-item').forEach(item => {
    item.addEventListener('click', function() {
        if (window.innerWidth <= 992) {
            const sidebar = document.querySelector('.admin-sidebar');
            const overlay = document.getElementById('sidebarOverlay');
            sidebar.classList.remove('active');
            overlay.classList.remove('active');
        }
    });
});

// Global chart variables
let salesChart;
let categoryChart;

// Document ready
document.addEventListener('DOMContentLoaded', function() {
    // Load all dashboard data
    loadDashboardData();
    
    // Refresh dashboard data when refresh button is clicked
    document.getElementById('refreshDashboard')?.addEventListener('click', function() {
        loadDashboardData();
        updateLastUpdated();
    });
    
    // Date range filter change
    document.getElementById('dateRangeFilter')?.addEventListener('change', function() {
        loadDashboardData();
        updateLastUpdated();
    });
    
    // Auto refresh dashboard data every 5 minutes
    setInterval(function() {
        loadDashboardData();
        updateLastUpdated();
    }, 300000); // 5 minutes
});

// Function to load all dashboard data
function loadDashboardData() {
    // Load metrics
    loadMetrics();
    
    // Load sales overview chart
    loadSalesOverviewChart();
    
    // Load sales by category chart
    loadSalesByCategoryChart();
    
    // Load recent orders
    loadRecentOrders();
    
    // Load top products
    loadTopProducts();
    
    // Check products data
    checkProductsData();
}

// Function to load metrics
function loadMetrics() {
    fetch('/dashboard/ajax/metrics/')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                // Update total sales
                const totalSalesEl = document.querySelector('.stat-card:nth-child(1) .stat-value');
                if (totalSalesEl) {
                    totalSalesEl.textContent = '₱' + numberWithCommas(data.data.totalSales.toFixed(2));
                }
                
                // Update total orders
                const totalOrdersEl = document.querySelector('.stat-card:nth-child(2) .stat-value');
                if (totalOrdersEl) {
                    totalOrdersEl.textContent = data.data.totalOrders;
                }
                
                // Update pending orders
                const pendingOrdersEl = document.querySelector('.stat-card:nth-child(3) .stat-value');
                if (pendingOrdersEl) {
                    pendingOrdersEl.textContent = data.data.pendingOrders;
                }
                
                // Update low stock items
                const lowStockEl = document.querySelector('.stat-card:nth-child(4) .stat-value');
                if (lowStockEl) {
                    lowStockEl.textContent = data.data.lowStockItems;
                }
            }
        })
        .catch(error => console.error('Error loading metrics:', error));
}

// Function to load sales overview chart
function loadSalesOverviewChart() {
    fetch('/dashboard/ajax/sales-overview/')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                renderSalesOverviewChart(data.data);
            }
        })
        .catch(error => console.error('Error loading sales overview:', error));
}

// Function to render sales overview chart
function renderSalesOverviewChart(data) {
    const ctx = document.getElementById('salesChart');
    if (!ctx) return;
    
    // Destroy existing chart if it exists
    if (salesChart) {
        salesChart.destroy();
    }
    
    salesChart = new Chart(ctx.getContext('2d'), {
        type: 'line',
        data: {
            labels: data.labels,
            datasets: [
                {
                    label: 'This Week',
                    data: data.currentWeek,
                    borderColor: '#2563eb',
                    backgroundColor: 'rgba(37, 99, 235, 0.1)',
                    tension: 0.4,
                    fill: true
                },
                {
                    label: 'Last Week',
                    data: data.prevWeek,
                    borderColor: '#94a3b8',
                    backgroundColor: 'rgba(148, 163, 184, 0.1)',
                    tension: 0.4,
                    fill: true
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'top'
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            let label = context.dataset.label || '';
                            if (label) {
                                label += ': ';
                            }
                            if (context.parsed.y !== null) {
                                label += '₱' + numberWithCommas(context.parsed.y.toFixed(2));
                            }
                            return label;
                        }
                    }
                }
            },
            scales: {
                y: {
                    beginAtZero: true,
                    ticks: {
                        callback: function(value) {
                            return '₱' + (value / 1000) + 'k';
                        }
                    }
                }
            }
        }
    });
}

// Function to load sales by category chart
function loadSalesByCategoryChart() {
    fetch('/dashboard/ajax/sales-by-category/')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                renderSalesByCategoryChart(data.data);
            }
        })
        .catch(error => console.error('Error loading sales by category:', error));
}

// Function to render sales by category chart
function renderSalesByCategoryChart(data) {
    const ctx = document.getElementById('categoryChart');
    if (!ctx) return;
    
    // Destroy existing chart if it exists
    if (categoryChart) {
        categoryChart.destroy();
    }
    
    categoryChart = new Chart(ctx.getContext('2d'), {
        type: 'doughnut',
        data: data,
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
                legend: {
                    position: 'right'
                },
                tooltip: {
                    callbacks: {
                        label: function(context) {
                            const label = context.label || '';
                            const value = context.raw || 0;
                            const total = context.dataset.data.reduce((a, b) => a + b, 0);
                            const percentage = Math.round((value / total) * 100);
                            return `${label}: ₱${numberWithCommas(value.toFixed(2))} (${percentage}%)`;
                        }
                    }
                }
            },
            cutout: '70%'
        }
    });
}

// Function to load recent orders
function loadRecentOrders() {
    fetch('/dashboard/ajax/recent-orders/')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                renderRecentOrders(data.data);
            }
        })
        .catch(error => console.error('Error loading recent orders:', error));
}

// Function to render recent orders
function renderRecentOrders(data) {
    const tbody = document.querySelector('#recentOrdersTable');
    if (!tbody) return;
    
    let html = '';
    
    if (data.length === 0) {
        html = '<tr><td colspan="5" style="text-align: center; color: #64748b;">No pending orders found</td></tr>';
    } else {
        data.forEach(order => {
            html += `
                <tr>
                    <td>#${order.id}</td>
                    <td>${order.customer}</td>
                    <td>₱${order.amount}</td>
                    <td>
                        <span class="status-badge ${order.status.toLowerCase()}">
                            ${order.status}
                        </span>
                    </td>
                    <td>${order.date}</td>
                </tr>
            `;
        });
    }
    
    tbody.innerHTML = html;
}

// Function to load top products
function loadTopProducts() {
    fetch('/dashboard/ajax/top-products/')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                renderTopProducts(data.data);
            }
        })
        .catch(error => console.error('Error loading top products:', error));
}

// Function to render top products
function renderTopProducts(data) {
    const tbody = document.querySelector('#topProductsTable');
    if (!tbody) return;
    
    let html = '';
    
    if (!data || data.length === 0) {
        html = '<tr><td colspan="4" style="text-align: center; color: #64748b;">No products found</td></tr>';
    } else {
        data.forEach(product => {
            html += `
                <tr>
                    <td>${product.product_name}</td>
                    <td>${product.category || 'Uncategorized'}</td>
                    <td>${product.quantity_sold}</td>
                    <td>₱${numberWithCommas(parseFloat(product.revenue).toFixed(2))}</td>
                </tr>
            `;
        });
    }
    
    tbody.innerHTML = html;
}

// Function to check products data and show low stock notification
function checkProductsData() {
    fetch('/dashboard/ajax/products-check/')
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                console.log('Products data loaded successfully');
                console.log('Total products:', data.data.totalProducts);
                console.log('Low stock items:', data.data.lowStockItems);
                
                // If there are low stock items, show a notification
                if (data.data.lowStockItems > 0) {
                    showLowStockNotification(data.data.lowStockItems, data.data.lowStockProducts);
                }
            }
        })
        .catch(error => console.error('Error checking products data:', error));
}

// Function to show low stock notification
function showLowStockNotification(count, products) {
    // Create notification if it doesn't exist
    if (document.getElementById('lowStockNotification')) {
        return; // Already showing
    }
    
    const notification = document.createElement('div');
    notification.id = 'lowStockNotification';
    notification.className = 'low-stock-notification';
    
    let productsList = '';
    products.slice(0, 3).forEach(product => {
        productsList += `
            <li>
                <span class="product-name">${product.name}</span>
                <span class="product-stock">Stock: ${product.stock}</span>
            </li>
        `;
    });
    
    if (products.length > 3) {
        productsList += `<li class="more-items">+${products.length - 3} more items</li>`;
    }
    
    notification.innerHTML = `
        <div class="notification-header">
            <i class="fas fa-exclamation-triangle"></i>
            <span>Low Stock Alert</span>
            <button class="close-notification"><i class="fas fa-times"></i></button>
        </div>
        <div class="notification-body">
            <p>You have <strong>${count}</strong> products with low stock.</p>
            <ul class="low-stock-list">
                ${productsList}
            </ul>
            <a href="/dashboard/products/?filter=low_stock" class="view-all-btn">View All</a>
        </div>
    `;
    
    document.body.appendChild(notification);
    
    // Add event listener to close button
    notification.querySelector('.close-notification').addEventListener('click', function() {
        notification.classList.add('notification-hiding');
        setTimeout(() => {
            notification.remove();
        }, 300);
    });
    
    // Show notification with animation
    setTimeout(() => {
        notification.classList.add('notification-visible');
    }, 500);
    
    // Auto hide after 10 seconds
    setTimeout(() => {
        if (notification.classList.contains('notification-visible')) {
            notification.querySelector('.close-notification').click();
        }
    }, 10000);
}

// Helper function to format numbers with commas
function numberWithCommas(x) {
    return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

// Function to update last updated text
function updateLastUpdated() {
    const el = document.getElementById('lastUpdated');
    if (!el) return;
    
    const now = new Date();
    const hours = now.getHours().toString().padStart(2, '0');
    const minutes = now.getMinutes().toString().padStart(2, '0');
    const seconds = now.getSeconds().toString().padStart(2, '0');
    const timeString = `${hours}:${minutes}:${seconds}`;
    
    el.textContent = `Last updated: ${timeString}`;
}

// Low stock notification styles
const notificationStyles = `
.low-stock-notification {
    position: fixed;
    bottom: 20px;
    right: 20px;
    width: 320px;
    background-color: white;
    border-radius: 8px;
    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
    z-index: 10000;
    transform: translateY(100%);
    opacity: 0;
    transition: transform 0.3s ease, opacity 0.3s ease;
    overflow: hidden;
}

.notification-visible {
    transform: translateY(0);
    opacity: 1;
}

.notification-hiding {
    transform: translateY(10px);
    opacity: 0;
}

.notification-header {
    display: flex;
    align-items: center;
    padding: 12px 15px;
    background-color: #f97316;
    color: white;
    font-weight: 600;
}

.notification-header i {
    margin-right: 8px;
}

.notification-header .close-notification {
    margin-left: auto;
    background: none;
    border: none;
    color: white;
    cursor: pointer;
    padding: 0;
    font-size: 14px;
}

.notification-body {
    padding: 15px;
}

.notification-body p {
    margin-top: 0;
    margin-bottom: 10px;
    color: #334155;
}

.low-stock-list {
    list-style: none;
    padding: 0;
    margin: 0 0 15px 0;
}

.low-stock-list li {
    padding: 8px 0;
    border-bottom: 1px solid #e2e8f0;
    display: flex;
    justify-content: space-between;
    font-size: 0.875rem;
}

.low-stock-list li:last-child {
    border-bottom: none;
}

.product-name {
    color: #334155;
    font-weight: 500;
}

.product-stock {
    color: #ef4444;
    font-weight: 600;
}

.more-items {
    text-align: center;
    color: #64748b;
    font-style: italic;
}

.view-all-btn {
    display: block;
    text-align: center;
    padding: 8px;
    background-color: #f1f5f9;
    color: #0f172a;
    border-radius: 4px;
    text-decoration: none;
    transition: background-color 0.2s ease;
    font-weight: 500;
}

.view-all-btn:hover {
    background-color: #e2e8f0;
}
`;

// Add notification styles to page
const styleEl = document.createElement('style');
styleEl.textContent = notificationStyles;
document.head.appendChild(styleEl);
