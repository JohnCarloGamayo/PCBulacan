#!/usr/bin/env python
"""Clean up invalid notifications"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'pcbulacan.settings')
django.setup()

from accounts.models import Notification

# Delete notifications with invalid links
deleted_count = Notification.objects.filter(link__in=['', 'null', None]).delete()[0]
print(f'Cleared {deleted_count} invalid notifications')

# Show remaining notifications
total = Notification.objects.count()
print(f'Total notifications remaining: {total}')
