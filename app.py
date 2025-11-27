from flask import Flask, render_template, redirect, url_for, request, flash, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
import os
import json

from models import db, User, Recipe, GameReview, MovieReview, MusicTrack

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')

# Handle DATABASE_URL (Render uses postgresql:// but SQLAlchemy needs postgresql+psycopg2://)
database_url = os.environ.get('DATABASE_URL', 'sqlite:///zjadowrealm.db')
if database_url.startswith('postgres://'):
    database_url = database_url.replace('postgres://', 'postgresql://', 1)
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Create tables on startup
with app.app_context():
    db.create_all()
    # Create admin user if it doesn't exist
    admin = User.query.filter_by(username='ZjadowPotato').first()
    if not admin:
        # Check if email already exists (from old admin account)
        old_admin = User.query.filter_by(email='admin@zjadowrealm.com').first()
        if old_admin and old_admin.username != 'ZjadowPotato':
            # Delete old admin account
            db.session.delete(old_admin)
            db.session.commit()
        
        admin = User(
            username='ZjadowPotato',
            email='admin@zjadowrealm.com',
            is_admin=True,
            is_approved=True
        )
        admin.set_password('ZjadowPotato')
        db.session.add(admin)
        db.session.commit()
        print("Admin user created: username='ZjadowPotato', password='ZjadowPotato'")

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Updated: Force deployment refresh with authentication v3.0
print("Starting Zjadow Realm Flask application v3.0 with authentication...")

# Authentication routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = request.form.get('remember', False)
        
        user = User.query.filter_by(username=username).first()
        
        if user and user.check_password(password):
            if not user.is_approved:
                flash('Your account is pending approval. Please wait for admin approval.', 'warning')
                return redirect(url_for('login'))
            
            login_user(user, remember=remember)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Invalid username or password', 'danger')
    
    return render_template('login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """Signup page"""
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        
        # Validation
        if password != confirm_password:
            flash('Passwords do not match', 'danger')
            return redirect(url_for('signup'))
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'danger')
            return redirect(url_for('signup'))
        
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'danger')
            return redirect(url_for('signup'))
        
        # Create new user (pending approval)
        new_user = User(username=username, email=email, is_approved=False)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        
        flash('Account created! Please wait for admin approval before logging in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('signup.html')

@app.route('/logout')
@login_required
def logout():
    """Logout current user"""
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('home'))

@app.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    """Change user password"""
    if request.method == 'POST':
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        # Verify current password
        if not current_user.check_password(current_password):
            flash('Current password is incorrect', 'danger')
            return redirect(url_for('change_password'))
        
        # Verify new passwords match
        if new_password != confirm_password:
            flash('New passwords do not match', 'danger')
            return redirect(url_for('change_password'))
        
        # Update password
        current_user.set_password(new_password)
        db.session.commit()
        
        flash('Password changed successfully!', 'success')
        return redirect(url_for('home'))
    
    return render_template('change_password.html')

# Admin routes
@app.route('/admin')
@login_required
def admin_dashboard():
    """Admin dashboard - only accessible to admin users"""
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('home'))
    
    # Get pending users
    pending_users = User.query.filter_by(is_approved=False, is_admin=False).all()
    
    # Get approved users (excluding admin)
    approved_users = User.query.filter_by(is_approved=True, is_admin=False).all()
    
    # Get all content counts
    recipes_count = Recipe.query.count()
    game_reviews_count = GameReview.query.count()
    movie_reviews_count = MovieReview.query.count()
    music_tracks_count = MusicTrack.query.count()
    
    return render_template('admin_dashboard.html', 
                         pending_users=pending_users,
                         approved_users=approved_users,
                         recipes_count=recipes_count,
                         game_reviews_count=game_reviews_count,
                         movie_reviews_count=movie_reviews_count,
                         music_tracks_count=music_tracks_count)

@app.route('/admin/approve-user/<int:user_id>')
@login_required
def approve_user(user_id):
    """Approve a pending user"""
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('home'))
    
    user = User.query.get_or_404(user_id)
    user.is_approved = True
    db.session.commit()
    
    flash(f'User {user.username} has been approved!', 'success')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/reject-user/<int:user_id>')
@login_required
def reject_user(user_id):
    """Reject and delete a pending user"""
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('home'))
    
    user = User.query.get_or_404(user_id)
    username = user.username
    db.session.delete(user)
    db.session.commit()
    
    flash(f'User {username} has been rejected and removed.', 'info')
    return redirect(url_for('admin_dashboard'))

@app.route('/admin/delete-user/<int:user_id>')
@login_required
def delete_user(user_id):
    """Delete an approved user"""
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('home'))
    
    user = User.query.get_or_404(user_id)
    
    # Prevent deleting admin users
    if user.is_admin:
        flash('Cannot delete admin users.', 'danger')
        return redirect(url_for('admin_dashboard'))
    
    username = user.username
    db.session.delete(user)
    db.session.commit()
    
    flash(f'User {username} has been deleted.', 'success')
    return redirect(url_for('admin_dashboard'))

# Admin content management routes
@app.route('/admin/recipes')
@login_required
def admin_recipes():
    """Manage recipes"""
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('home'))
    
    recipes = Recipe.query.order_by(Recipe.created_at.desc()).all()
    return render_template('admin_recipes.html', recipes=recipes)

@app.route('/admin/recipes/add', methods=['GET', 'POST'])
@login_required
def admin_add_recipe():
    """Add new recipe"""
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        title = request.form.get('title')
        icon = request.form.get('icon', 'utensils')
        color = request.form.get('color', 'primary')
        prep_time = request.form.get('prep_time')
        cook_time = request.form.get('cook_time')
        servings = request.form.get('servings')
        ingredients = request.form.get('ingredients')
        instructions = request.form.get('instructions')
        
        recipe = Recipe(
            title=title,
            icon=icon,
            color=color,
            prep_time=prep_time,
            cook_time=cook_time,
            servings=servings,
            ingredients=ingredients,
            instructions=instructions,
            created_by=current_user.id
        )
        db.session.add(recipe)
        db.session.commit()
        
        flash(f'Recipe "{title}" added successfully!', 'success')
        return redirect(url_for('admin_recipes'))
    
    return render_template('admin_add_recipe.html')

@app.route('/admin/recipes/edit/<int:recipe_id>', methods=['GET', 'POST'])
@login_required
def admin_edit_recipe(recipe_id):
    """Edit existing recipe"""
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('home'))
    
    recipe = Recipe.query.get_or_404(recipe_id)
    
    if request.method == 'POST':
        recipe.title = request.form.get('title')
        recipe.icon = request.form.get('icon', 'utensils')
        recipe.color = request.form.get('color', 'primary')
        recipe.prep_time = request.form.get('prep_time')
        recipe.cook_time = request.form.get('cook_time')
        recipe.servings = request.form.get('servings')
        recipe.ingredients = request.form.get('ingredients')
        recipe.instructions = request.form.get('instructions')
        
        db.session.commit()
        
        flash(f'Recipe "{recipe.title}" updated successfully!', 'success')
        return redirect(url_for('admin_recipes'))
    
    return render_template('admin_edit_recipe.html', recipe=recipe)

@app.route('/admin/recipes/delete/<int:recipe_id>')
@login_required
def admin_delete_recipe(recipe_id):
    """Delete recipe"""
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('home'))
    
    recipe = Recipe.query.get_or_404(recipe_id)
    title = recipe.title
    db.session.delete(recipe)
    db.session.commit()
    
    flash(f'Recipe "{title}" deleted successfully!', 'info')
    return redirect(url_for('admin_recipes'))

@app.route('/admin/game-reviews')
@login_required
def admin_game_reviews():
    """Manage game reviews"""
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('home'))
    
    reviews = GameReview.query.order_by(GameReview.created_at.desc()).all()
    return render_template('admin_game_reviews.html', reviews=reviews)

@app.route('/admin/game-reviews/add', methods=['GET', 'POST'])
@login_required
def admin_add_game_review():
    """Add new game review"""
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        review = GameReview(
            title=request.form.get('title'),
            rating=float(request.form.get('rating')),
            review_text=request.form.get('review_text'),
            image_url=request.form.get('image_url'),
            platform=request.form.get('platform'),
            genre=request.form.get('genre'),
            created_by=current_user.id
        )
        db.session.add(review)
        db.session.commit()
        
        flash(f'Game review for "{review.title}" added successfully!', 'success')
        return redirect(url_for('admin_game_reviews'))
    
    return render_template('admin_add_game_review.html')

@app.route('/admin/game-reviews/edit/<int:review_id>', methods=['GET', 'POST'])
@login_required
def admin_edit_game_review(review_id):
    """Edit game review"""
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('home'))
    
    review = GameReview.query.get_or_404(review_id)
    
    if request.method == 'POST':
        review.title = request.form.get('title')
        review.rating = float(request.form.get('rating'))
        review.review_text = request.form.get('review_text')
        review.image_url = request.form.get('image_url')
        review.platform = request.form.get('platform')
        review.genre = request.form.get('genre')
        
        db.session.commit()
        
        flash(f'Game review for "{review.title}" updated successfully!', 'success')
        return redirect(url_for('admin_game_reviews'))
    
    return render_template('admin_edit_game_review.html', review=review)

@app.route('/admin/game-reviews/delete/<int:review_id>')
@login_required
def admin_delete_game_review(review_id):
    """Delete game review"""
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('home'))
    
    review = GameReview.query.get_or_404(review_id)
    title = review.title
    db.session.delete(review)
    db.session.commit()
    
    flash(f'Game review for "{title}" deleted successfully!', 'info')
    return redirect(url_for('admin_game_reviews'))

@app.route('/admin/movie-reviews')
@login_required
def admin_movie_reviews():
    """Manage movie reviews"""
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('home'))
    
    reviews = MovieReview.query.order_by(MovieReview.created_at.desc()).all()
    return render_template('admin_movie_reviews.html', reviews=reviews)

@app.route('/admin/movie-reviews/add', methods=['GET', 'POST'])
@login_required
def admin_add_movie_review():
    """Add new movie review"""
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        review = MovieReview(
            title=request.form.get('title'),
            rating=float(request.form.get('rating')),
            review_text=request.form.get('review_text'),
            image_url=request.form.get('image_url'),
            year=int(request.form.get('year')) if request.form.get('year') else None,
            genre=request.form.get('genre'),
            created_by=current_user.id
        )
        db.session.add(review)
        db.session.commit()
        
        flash(f'Movie review for "{review.title}" added successfully!', 'success')
        return redirect(url_for('admin_movie_reviews'))
    
    return render_template('admin_add_movie_review.html')

@app.route('/admin/movie-reviews/edit/<int:review_id>', methods=['GET', 'POST'])
@login_required
def admin_edit_movie_review(review_id):
    """Edit movie review"""
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('home'))
    
    review = MovieReview.query.get_or_404(review_id)
    
    if request.method == 'POST':
        review.title = request.form.get('title')
        review.rating = float(request.form.get('rating'))
        review.review_text = request.form.get('review_text')
        review.image_url = request.form.get('image_url')
        review.year = int(request.form.get('year')) if request.form.get('year') else None
        review.genre = request.form.get('genre')
        
        db.session.commit()
        
        flash(f'Movie review for "{review.title}" updated successfully!', 'success')
        return redirect(url_for('admin_movie_reviews'))
    
    return render_template('admin_edit_movie_review.html', review=review)

@app.route('/admin/movie-reviews/delete/<int:review_id>')
@login_required
def admin_delete_movie_review(review_id):
    """Delete movie review"""
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('home'))
    
    review = MovieReview.query.get_or_404(review_id)
    title = review.title
    db.session.delete(review)
    db.session.commit()
    
    flash(f'Movie review for "{title}" deleted successfully!', 'info')
    return redirect(url_for('admin_movie_reviews'))

@app.route('/admin/music')
@login_required
def admin_music():
    """Manage music tracks"""
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('home'))
    
    tracks = MusicTrack.query.order_by(MusicTrack.created_at.desc()).all()
    return render_template('admin_music.html', tracks=tracks)

@app.route('/admin/music/add', methods=['GET', 'POST'])
@login_required
def admin_add_music():
    """Add new music track"""
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('home'))
    
    if request.method == 'POST':
        track = MusicTrack(
            title=request.form.get('title'),
            video_id=request.form.get('video_id'),
            description=request.form.get('description'),
            artist=request.form.get('artist', '-bAStIAN-'),
            created_by=current_user.id
        )
        db.session.add(track)
        db.session.commit()
        
        flash(f'Music track "{track.title}" added successfully!', 'success')
        return redirect(url_for('admin_music'))
    
    return render_template('admin_add_music.html')

@app.route('/admin/music/edit/<int:track_id>', methods=['GET', 'POST'])
@login_required
def admin_edit_music(track_id):
    """Edit music track"""
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('home'))
    
    track = MusicTrack.query.get_or_404(track_id)
    
    if request.method == 'POST':
        track.title = request.form.get('title')
        track.video_id = request.form.get('video_id')
        track.description = request.form.get('description')
        track.artist = request.form.get('artist', '-bAStIAN-')
        
        db.session.commit()
        
        flash(f'Music track "{track.title}" updated successfully!', 'success')
        return redirect(url_for('admin_music'))
    
    return render_template('admin_edit_music.html', track=track)

@app.route('/admin/music/delete/<int:track_id>')
@login_required
def admin_delete_music(track_id):
    """Delete music track"""
    if not current_user.is_admin:
        flash('Access denied. Admin privileges required.', 'danger')
        return redirect(url_for('home'))
    
    track = MusicTrack.query.get_or_404(track_id)
    title = track.title
    db.session.delete(track)
    db.session.commit()
    
    flash(f'Music track "{title}" deleted successfully!', 'info')
    return redirect(url_for('admin_music'))

# Public routes (all require login)
@app.route('/')
@login_required
def home():
    """Home page with overview"""
    return render_template('index.html')

@app.route('/about')
@login_required
def about():
    """Personal description page"""
    return render_template('about.html')

@app.route('/discord')
@login_required
def discord():
    """Discord community and server information page"""
    return render_template('discord.html')

@app.route('/steam')
@login_required
def steam():
    """Steam profile page"""
    return render_template('steam.html')

@app.route('/game-reviews')
@login_required
def game_reviews():
    """Game reviews page"""
    return render_template('game_reviews.html')

@app.route('/movie-reviews')
@login_required
def movie_reviews():
    """Movie reviews page"""
    return render_template('movie_reviews.html')

@app.route('/music')
@login_required
def music():
    """Music page"""
    return render_template('music.html')

@app.route('/games')
@login_required
def games():
    """Games hub page"""
    return render_template('games_hub.html')

@app.route('/games/snake')
@login_required
def game_snake():
    """Snake game"""
    return render_template('game_snake.html')

@app.route('/games/pong')
@login_required
def game_pong():
    """Pong game"""
    return render_template('game_pong.html')

@app.route('/games/memory')
@login_required
def game_memory():
    """Memory game"""
    return render_template('game_memory.html')

@app.route('/games/tetris')
@login_required
def game_tetris():
    """Zjadow Block Drop game"""
    return render_template('game_tetris.html')
@app.route('/games/blockdrop')

@app.route('/games/platformer')
@login_required
def game_platformer():
    """Infinite Rhythm Platformer"""
    return render_template('game_platformer.html')

@app.route('/games/pirates')
@login_required
def game_pirates():
    """Pirate Adventure game"""
    return render_template('game_pirates.html')

@app.route('/games/chess')
@login_required
def game_chess():
    """Chess game"""
    return render_template('game_chess.html')

@app.route('/games/tictactoe')
@login_required
def game_tictactoe():
    """Tic Tac Toe game"""
    return render_template('game_tictactoe.html')

@app.route('/games/wordguess')
@login_required
def game_wordguess():
    """Word Guess game"""
    return render_template('game_wordguess.html')

@app.route('/games/strands')
@login_required
def game_strands():
    """Strands game"""
    return render_template('game_strands.html')

@app.route('/training')
@login_required
def training():
    """Training programs and fitness routines"""
    return render_template('training.html')

@app.route('/food')
@login_required
def food():
    """Nutrition and dietary recommendations"""
    return render_template('food.html')

@app.route('/tutorials')
@login_required
def tutorials():
    """Educational tutorials on various subjects"""
    return render_template('tutorials.html')

@app.route('/tools')
@login_required
def tools():
    """Utility tools and calculators"""
    return render_template('tools.html')

@app.route('/game-blog')
@login_required
def game_blog():
    """Game development blog and documentation"""
    return render_template('game_blog.html')

@app.route('/minecraft')
@login_required
def minecraft():
    """Minecraft blog page"""
    return render_template('minecraft.html')

@app.route('/dinner-recipes')
@login_required
def dinner_recipes():
    """Simple dinner recipes for everyday cooking"""
    return render_template('dinner_recipes.html')

if __name__ == '__main__':
    # For deployment, use environment variables
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV', 'development') == 'development'
    app.run(debug=True, host='0.0.0.0', port=port)  # Always use debug=True for local development