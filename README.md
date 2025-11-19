# Portfolio Website

A modern, responsive Flask-based portfolio website featuring multiple sections for showcasing your personal brand, gaming profile, reviews, music, diary, and daily thoughts.

## 🚀 Features

- **Multi-page Portfolio Layout**: Home, About, Links, Steam Profile, Reviews, Music, Diary, and Thought of the Day
- **Responsive Design**: Built with Bootstrap 5 for mobile-first responsiveness
- **Interactive Elements**: Custom JavaScript animations and interactions
- **Modern UI/UX**: Clean, professional design with smooth animations
- **Social Integration**: Links to all your social media and gaming profiles
- **Review Systems**: Dedicated pages for game and movie reviews
- **Personal Content**: Diary entries and daily thought sharing
- **Music Integration**: Showcase your music taste and playlists

## 🛠 Technology Stack

- **Backend**: Python Flask
- **Frontend**: HTML5, CSS3, JavaScript
- **Framework**: Bootstrap 5
- **Icons**: Font Awesome 6
- **Template Engine**: Jinja2

## 📂 Project Structure

```
ZjadowSide/
├── .github/
│   └── copilot-instructions.md
├── .venv/                    # Python virtual environment
├── static/
│   ├── css/
│   │   └── style.css        # Custom styles
│   ├── js/
│   │   └── script.js        # Custom JavaScript
│   └── images/              # Image assets (placeholder)
├── templates/
│   ├── base.html            # Base template
│   ├── index.html           # Home page
│   ├── about.html           # About page
│   ├── links.html           # Social links
│   ├── steam.html           # Steam profile
│   ├── game_reviews.html    # Game reviews
│   ├── movie_reviews.html   # Movie reviews
│   ├── music.html           # Music page
│   ├── diary.html           # Personal diary
│   └── thought_of_day.html  # Daily thoughts
├── app.py                   # Main Flask application
├── requirements.txt         # Python dependencies
└── README.md               # This file
```

## 🚦 Getting Started

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. **Clone or navigate to the project directory**:
   ```bash
   cd ZjadowSide
   ```

2. **Activate the virtual environment** (already configured):
   ```bash
   .venv\\Scripts\\activate  # Windows
   # or
   source .venv/bin/activate  # macOS/Linux
   ```

3. **Install dependencies** (already installed):
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   python app.py
   ```

5. **Open your browser** and navigate to:
   ```
   http://localhost:5000
   ```

## 🎨 Customization

### Personal Information

1. **Update About Page** (`templates/about.html`):
   - Replace placeholder text with your actual bio
   - Update personal facts and information
   - Add your real location, occupation, etc.

2. **Social Links** (`templates/links.html`):
   - Replace all placeholder links with your actual profiles
   - Update usernames and profile names
   - Remove sections you don't use

3. **Steam Profile** (`templates/steam.html`):
   - Update with your actual Steam username
   - Replace placeholder game statistics
   - Add your real favorite games

### Content Updates

- **Game Reviews**: Add your actual game reviews in `game_reviews.html`
- **Movie Reviews**: Update with real movie reviews in `movie_reviews.html`
- **Music**: Customize your music preferences in `music.html`
- **Diary**: Add real diary entries in `diary.html`
- **Daily Thoughts**: Update thought content in `thought_of_day.html`

### Styling

- **Colors**: Modify color schemes in `static/css/style.css`
- **Fonts**: Update font families in the CSS file
- **Layout**: Adjust Bootstrap classes in templates
- **Images**: Add your actual photos to `static/images/`

## 🌐 Deployment

### Local Development
The application runs on `http://localhost:5000` by default with debug mode enabled.

### Production Deployment
For production deployment:

1. Set `debug=False` in `app.py`
2. Use a production WSGI server like Gunicorn:
   ```bash
   gunicorn -w 4 -b 0.0.0.0:5000 app:app
   ```

### Platform Deployment Options
- **Heroku**: Add `Procfile` with `web: gunicorn app:app`
- **Vercel**: Configure for Flask deployment
- **DigitalOcean App Platform**: Use the requirements.txt
- **AWS/Azure**: Deploy using their Python web app services

## 📱 Features Overview

### 🏠 Home Page
- Hero section with call-to-action
- Feature highlights
- Recent updates preview

### 👤 About Page
- Personal biography
- Skills and interests
- Contact information

### 🔗 Links Page
- Social media profiles
- Gaming platform accounts
- Professional networks
- Contact methods

### 🎮 Steam Profile
- Gaming statistics
- Recently played games
- All-time favorites
- Achievement showcase

### ⭐ Review Pages
- **Game Reviews**: Detailed game analysis with ratings
- **Movie Reviews**: Film critiques with star ratings
- Filtering by genre and rating

### 🎵 Music Page
- Currently playing track
- Favorite songs and albums
- Custom playlists
- Music platform links

### 📖 Diary Page
- Personal journal entries
- Mood tracking
- Category filtering
- Interactive like system

### 💭 Thought of the Day
- Daily inspirational thoughts
- Reflection questions
- Mood tracking
- Previous thoughts archive

## 🎨 Design Features

- **Responsive Design**: Works on all device sizes
- **Dark Mode Support**: Automatic system preference detection
- **Smooth Animations**: CSS transitions and JavaScript effects
- **Interactive Elements**: Hover effects and click animations
- **Modern Typography**: Clean, readable fonts
- **Color-coded Sections**: Each section has its theme color

## 🔧 Technical Features

- **Flask Routes**: Clean URL structure
- **Template Inheritance**: Consistent layout across pages
- **Static File Management**: Organized CSS, JS, and images
- **Performance Optimized**: Efficient loading and animations
- **SEO Friendly**: Proper HTML structure and meta tags

## 📝 TODO / Customization Checklist

- [ ] Replace all placeholder text with your actual content
- [ ] Update social media links with your real profiles
- [ ] Add your actual Steam username and game statistics
- [ ] Write real game and movie reviews
- [ ] Add your favorite music and playlists
- [ ] Create authentic diary entries
- [ ] Update personal information in About page
- [ ] Add your profile photos/images
- [ ] Customize color scheme if desired
- [ ] Test all interactive features
- [ ] Deploy to your preferred hosting platform

## 🤝 Contributing

This is a personal portfolio template. Feel free to:
- Fork and customize for your own use
- Submit bug reports or feature requests
- Share improvements or suggestions

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 📞 Support

If you need help customizing your portfolio:
1. Check the code comments for guidance
2. Refer to Flask and Bootstrap documentation
3. Test locally before deploying

---

**Made with ❤️ using Flask, Bootstrap, and modern web technologies**