from flask import Flask, render_template
from datetime import datetime
import os

app = Flask(__name__)

@app.route('/')
def home():
    """Home page with overview"""
    return render_template('index.html')

@app.route('/about')
def about():
    """Personal description page"""
    return render_template('about.html')

@app.route('/discord')
def discord():
    """Discord community and server information page"""
    return render_template('discord.html')

@app.route('/steam')
def steam():
    """Steam profile page"""
    return render_template('steam.html')

@app.route('/game-reviews')
def game_reviews():
    """Game reviews page"""
    return render_template('game_reviews.html')

@app.route('/movie-reviews')
def movie_reviews():
    """Movie reviews page"""
    return render_template('movie_reviews.html')

@app.route('/music')
def music():
    """Music page"""
    return render_template('music.html')

@app.route('/games')
def games():
    """Browser games page"""
    return render_template('games.html')

@app.route('/training')
def training():
    """Training programs and fitness routines"""
    return render_template('training.html')

@app.route('/food')
def food():
    """Nutrition and dietary recommendations"""
    return render_template('food.html')

@app.route('/tutorials')
def tutorials():
    """Educational tutorials on various subjects"""
    return render_template('tutorials.html')

@app.route('/tools')
def tools():
    """Utility tools and calculators"""
    return render_template('tools.html')

@app.route('/game-blog')
def game_blog():
    """Game development blog and documentation"""
    return render_template('game_blog.html')

@app.route('/minecraft')
def minecraft():
    """Minecraft blog page"""
    return render_template('minecraft.html')

if __name__ == '__main__':
    # For deployment, use environment variables
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    app.run(debug=debug, host='0.0.0.0', port=port)