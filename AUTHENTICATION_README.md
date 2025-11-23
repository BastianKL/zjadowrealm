# ZjadowRealm Authentication System

## 🚀 New Features

Your ZjadowRealm website now includes a complete authentication system with user management and admin capabilities!

### ✨ Key Features

1. **User Authentication**
   - Login/Signup system with secure password hashing
   - Remember me functionality
   - Session management
   - Flash messages for user feedback

2. **Admin Approval Workflow**
   - New users must be approved by admin before accessing the site
   - Pending users cannot log in until approved
   - Admin can approve or reject user registrations

3. **Admin Dashboard**
   - Exclusive admin-only access
   - View and manage pending user approvals
   - Overview of all content (recipes, game reviews, movie reviews, music tracks)
   - Future: Add/edit/delete content directly from the dashboard

4. **Database Models**
   - User model with authentication
   - Recipe model for dinner recipes
   - GameReview model for game reviews
   - MovieReview model for movie reviews
   - MusicTrack model for music tracks

### 🔐 Admin Account

**Username:** `ZjadowPotato`  
**Password:** `ZjadowPotato`

You can change your password at any time through the user menu → "Change Password"

## 🎯 How to Use

### For Regular Users

1. **Sign Up**
   - Click "Sign Up" in the navigation bar
   - Fill in username, email, and password
   - Submit the form
   - Wait for admin approval

2. **Login**
   - After admin approval, click "Login"
   - Enter your username and password
   - Check "Remember me" to stay logged in
   - Access all site features

3. **Logout**
   - Click your username dropdown in the navbar
   - Select "Logout"

### For Admin Users

1. **Access Admin Dashboard**
   - Login with admin credentials
   - Click your username dropdown → "Admin Dashboard"

2. **Approve/Reject Users**
   - View pending user registrations
   - Click "Approve" to grant access
   - Click "Reject" to deny and remove user

3. **Manage Content** ✅
   - Add/edit/delete recipes through web interface
   - Add/edit/delete game reviews
   - Add/edit/delete movie reviews
   - Add/edit/delete music tracks

## 📁 Project Structure

```
ZjadowSide/
├── app.py                 # Main Flask application with authentication routes
├── models.py             # Database models (User, Recipe, etc.)
├── requirements.txt      # Python dependencies
├── zjadowrealm.db       # SQLite database (auto-created)
├── templates/
│   ├── base.html        # Updated with auth navbar links
│   ├── login.html       # Login page
│   ├── signup.html      # Registration page
│   ├── admin_dashboard.html  # Admin control panel
│   └── ... (other templates)
└── static/
    ├── css/
    ├── js/
    └── images/
```

## 🛠️ Technical Details

### Dependencies

```
flask==2.3.3              # Web framework
flask-login==0.6.3        # User session management
flask-sqlalchemy==3.0.5   # Database ORM
flask-wtf==1.2.1          # Form handling
wtforms==3.1.1            # Form validation
werkzeug==2.3.7           # Password hashing
email-validator==2.1.0    # Email validation
gunicorn==21.2.0          # Production server
```

### Database Schema

#### User Model
- `id` - Primary key
- `username` - Unique username
- `email` - Unique email address
- `password_hash` - Bcrypt hashed password
- `is_admin` - Admin privilege flag
- `is_approved` - Approval status flag
- `created_at` - Registration timestamp

#### Recipe Model
- `id` - Primary key
- `title` - Recipe name
- `icon` - FontAwesome icon
- `color` - Bootstrap color theme
- `prep_time` - Preparation time
- `cook_time` - Cooking time
- `servings` - Number of servings
- `ingredients` - JSON string of ingredients
- `instructions` - JSON string of steps
- `created_by` - Foreign key to User
- `created_at` / `updated_at` - Timestamps

#### GameReview Model
- `id` - Primary key
- `title` - Game title
- `rating` - Numeric rating
- `review_text` - Review content
- `image_url` - Game image
- `platform` - Gaming platform
- `genre` - Game genre
- `created_by` - Foreign key to User
- `created_at` / `updated_at` - Timestamps

#### MovieReview Model
- Similar to GameReview with movie-specific fields

#### MusicTrack Model
- `id` - Primary key
- `title` - Track title
- `video_id` - YouTube video ID
- `description` - Track description
- `artist` - Artist name
- `created_by` - Foreign key to User
- `created_at` / `updated_at` - Timestamps

## 🚀 Running Locally

1. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Application**
   ```bash
   python app.py
   ```

3. **Access the Site**
   - Open browser to `http://localhost:5000`
   - Database will be auto-created on first run
   - Admin user will be auto-created

## 🌐 Deployment to Render

The application is ready for deployment! The authentication system works seamlessly on Render.

### Environment Variables (Optional)

For production, set these environment variables:

- `SECRET_KEY` - Flask secret key (auto-generated if not set)
- `DATABASE_URL` - Database connection string (defaults to SQLite)

### Deployment Steps

1. **Commit Changes**
   ```bash
   git add .
   git commit -m "Added authentication system"
   git push origin main
   ```

2. **Render Auto-Deploy**
   - Render will automatically detect changes
   - Build and deploy with new dependencies
   - Database will be created on first deploy

## 🔒 Security Features

- **Password Hashing**: Werkzeug PBKDF2 SHA-256 hashing
- **Session Management**: Flask-Login secure sessions
- **CSRF Protection**: Flask-WTF CSRF tokens
- **SQL Injection Prevention**: SQLAlchemy parameterized queries
- **Admin Authorization**: Route decorators for access control

## 📝 Future Enhancements

### Phase 1 ✅ (Complete)
- ✅ User registration and login
- ✅ Admin approval workflow
- ✅ Admin dashboard
- ✅ Database models for content

### Phase 2 (Next Steps)
- 🔄 Recipe management interface (CRUD)
- 🔄 Game review management
- 🔄 Movie review management
- 🔄 Music track management
- 🔄 User profile pages
- 🔄 User settings/preferences

### Phase 3 (Future)
- Password reset functionality
- Email notifications for approvals
- User roles (moderator, contributor)
- Content moderation system
- File upload for images
- Rich text editor for reviews

## 🐛 Troubleshooting

### Database Issues

If you encounter database errors:

```bash
# Delete the database file
rm zjadowrealm.db

# Restart the application (will recreate DB)
python app.py
```

### Package Installation Issues

```bash
# Upgrade pip first
python -m pip install --upgrade pip

# Install packages individually if bulk install fails
pip install Flask-Login==0.6.3
pip install Flask-SQLAlchemy==3.0.5
pip install Flask-WTF==1.2.1
```

### Admin Login Issues

If admin account wasn't created:

1. Delete `zjadowrealm.db`
2. Restart `python app.py`
3. Admin user will be recreated

## 🎨 UI Customization

### Login/Signup Pages
- Beautiful gradient backgrounds
- Responsive card layouts
- FontAwesome icons
- Bootstrap styling
- Smooth animations on hover

### Admin Dashboard
- Statistics cards with icons
- Pending user table with actions
- Content management links
- Modern, professional design

### Navigation Bar
- Authentication status aware
- User dropdown menu
- Admin badge for admin users
- Login/Signup links for guests

## 📊 Database Statistics

Access admin dashboard to view:
- Total number of recipes
- Total number of game reviews
- Total number of movie reviews
- Total number of music tracks
- Pending user approvals

## 🤝 Contributing

To add new features:

1. Create new database models in `models.py`
2. Add routes in `app.py`
3. Create templates in `templates/`
4. Update admin dashboard for management

## 📄 License

All rights reserved © 2025 ZjadowRealm

---

## Quick Reference

| Page | URL | Access |
|------|-----|--------|
| Home | `/` | Public |
| Login | `/login` | Public |
| Signup | `/signup` | Public |
| Logout | `/logout` | Authenticated |
| Admin Dashboard | `/admin` | Admin Only |
| Approve User | `/admin/approve-user/<id>` | Admin Only |
| Reject User | `/admin/reject-user/<id>` | Admin Only |

---

**Need Help?** Check the admin dashboard or contact the site administrator!
