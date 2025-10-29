# Instructions for Collaborators - Pull Latest Updates

## The Loading Screen Shows Black?

This means you need to pull the latest changes which include all media files (40+ MB).

## Steps to Fix:

### 1. Pull Latest Changes
```bash
git pull origin main
```

### 2. Verify Media Files Were Downloaded
Check if this file exists:
```bash
ls media/loading_screen/loading.mp4
```

Or on Windows:
```cmd
dir media\loading_screen\loading.mp4
```

### 3. Run Django Server
```bash
python manage.py runserver
```

### 4. Clear Browser Cache
- Press `Ctrl + Shift + Delete` (Chrome/Edge)
- Select "Cached images and files"
- Click "Clear data"
- Or use `Ctrl + F5` to hard refresh

## What Was Pushed (Latest Commits):

### Commit 36c44a5 - Media Files
✅ Loading screen video (28.7 MB)
✅ All product images
✅ Slideshow images
✅ Profile pictures
✅ Payment screenshots
✅ Updated .gitignore to track media

### Commit 3c725e9 - Features
✅ Video loading screen with sound
✅ Public access (guests can browse)
✅ Login modal for cart actions
✅ Fixed notification URLs

## Troubleshooting:

### If git pull shows conflicts:
```bash
git stash
git pull origin main
git stash pop
```

### If media folder is still empty:
```bash
# Check .gitignore doesn't ignore media
cat .gitignore | grep media

# Should NOT show "/media" in output
```

### If video still doesn't play:
1. Check browser console (F12) for errors
2. Verify file path: `/media/loading_screen/loading.mp4`
3. Check file size: should be ~28.7 MB
4. Try different browser (Chrome, Edge, Firefox)

## Need Help?
Contact the main developer or check the commit history:
```bash
git log --oneline -5
```

Expected output should show:
- `36c44a5 Add all media files (loading screen, products, slideshow) and update .gitignore`
- `3c725e9 Add loading screen, public access, login modal, and notification URL fix`
