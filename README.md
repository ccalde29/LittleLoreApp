# 📚 Little Lores
**Discover the world through reading!**

A web-based reading comprehension app for children featuring traditional folk stories from around the globe. Little Lores combines engaging storytelling with modern technology to help young readers explore different cultures while improving their reading skills.

## 🌟 Features

### 📖 **Reading Experience**
- **3,000+ Traditional Folk Stories** from around the world
- **Grade-Appropriate Content** (K-1 through 6-8)
- **Interactive Text-to-Speech** with multiple voice options
- **Word Helper System** with definitions for difficult words
- **Adjustable Reading Settings** (font size, speech speed, pitch)
- **Reading Progress Tracking** with completion certificates

### 🗺️ **Global Exploration**
- **Regional Story Collections** from Africa, Asia, Europe, Americas, and Oceania
- **Cultural Learning** through traditional tales and folklore
- **Nation-Specific Stories** to learn about different countries
- **Mixed Mode** for surprise story discovery

### 🎭 **Voice & Audio**
- **6 Voice Categories**: Narrator (Male/Female), Teacher (Male/Female), Storyteller (Male/Female)
- **Customizable Speech Settings**: Speed, pitch, and tone controls
- **Voice Preview System** to test different narrators
- **Pause/Resume Functionality** with audio controls

### 👤 **User Management**
- **Google OAuth Authentication** for secure login
- **Personal Reading Dashboard** with statistics
- **Progress Tracking** across all stories
- **Grade and Region Preferences** saved per user

## 🚀 Live Demo

Visit the live application: [Little Lores App](https://ccalde29.github.io/LittleLoreApp/)

## 🛠️ Tech Stack

- **Frontend**: Vanilla HTML5, CSS3, JavaScript (ES6+)
- **Database**: Supabase (PostgreSQL)
- **Authentication**: Supabase Auth with Google OAuth
- **Text-to-Speech**: Web Speech API
- **Hosting**: GitHub Pages
- **Design**: Responsive CSS Grid/Flexbox

## 📦 Installation & Setup

### Prerequisites
- Modern web browser with JavaScript enabled
- Internet connection for authentication and story loading
- Python 3.8+ (for audio generation scripts)

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/ccalde29/LittleLoreApp.git
   cd LittleLoreApp
   ```

2. **Set up Supabase Locally**
   ```bash
   # Install Supabase CLI
   npm install -g supabase
   
   # Start local Supabase
   supabase start
   
   # Database will be available at http://127.0.0.1:54321
   # Studio UI at http://127.0.0.1:54323
   ```

3. **Configure Google OAuth**
   - Set up Google OAuth in your Supabase project
   - Add your domain to allowed redirect URLs

4. **Generate Story Audio (Optional but Recommended)**
   ```bash
   cd scripts
   # See AUDIO_GENERATION_GUIDE.md for detailed instructions
   python analyze_stories.py  # Analyze K-5 stories
   python clean_stories.py --apply  # Clean story text
   python generate_audio.py --all --apply  # Generate audio
   ```
   
   📘 **Read-Aloud Feature**: Uses Google Cloud Text-to-Speech with natural Chirp voices optimized for children. Audio files stored in Google Cloud Storage (`little-lore-audio` bucket). See [`AUDIO_GENERATION_GUIDE.md`](AUDIO_GENERATION_GUIDE.md) for complete setup.

5. **Serve the application**
   ```bash
   # Using Python
   python -m http.server 8000
   
   # Using Node.js
   npx serve .
   
   # Using PHP
   php -S localhost:8000
   ```

6. **Access the app**
   Open your browser and navigate to `http://localhost:8000`

## 🗄️ Database Schema

### Required Tables

#### `stories_raw`
```sql
CREATE TABLE stories_raw (
    story_id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    text TEXT NOT NULL,
    nation VARCHAR(100),
    region VARCHAR(50),
    grade_level VARCHAR(10),
    created_at TIMESTAMP DEFAULT NOW()
);
```

#### `user_profiles`
```sql
CREATE TABLE user_profiles (
    user_id UUID PRIMARY KEY REFERENCES auth.users(id),
    grade VARCHAR(10),
    preferred_nation VARCHAR(100),
    onboarding_complete BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);
```

#### `user_progress`
```sql
CREATE TABLE user_progress (
    id SERIAL PRIMARY KEY,
    user_id UUID REFERENCES auth.users(id),
    story_id INTEGER REFERENCES stories_raw(story_id),
    completed TIMESTAMP,
    completed_at TIMESTAMP,
    last_read TIMESTAMP DEFAULT NOW(),
    UNIQUE(user_id, story_id)
);
```

## 🎯 Usage

1. **Login**: Use Google OAuth to authenticate
2. **Setup Profile**: Select grade level and preferred region
3. **Discover Stories**: Browse available stories from your chosen region
4. **Read & Listen**: Enjoy stories with customizable text-to-speech
5. **Track Progress**: Complete stories and view your reading journey

## 🎨 Customization

### Voice Settings
The app automatically categorizes available system voices into:
- **Narrator Voices**: Professional, clear reading voices
- **Teacher Voices**: Educational, instructional tone
- **Storyteller Voices**: Expressive, engaging narration

### Reading Levels
Stories are categorized by grade levels:
- **K-1**: Kindergarten to 1st Grade
- **2-3**: 2nd to 3rd Grade  
- **4-5**: 4th to 5th Grade
- **6-8**: 6th to 8th Grade

### Regional Content
Stories are organized by world regions:
- 🌍 **Africa**: Traditional African folktales
- 🏯 **Asia**: Asian legends and stories
- 🏰 **Europe**: European fairy tales and folklore
- 🗽 **Americas**: North and South American tales
- 🏝️ **Oceania**: Pacific Island stories
- 🌈 **Mixed**: Random selection from all regions

## 🧪 Testing

The application includes several test scenarios:
- Authentication flow testing
- Story loading and display
- Voice system functionality
- Progress tracking verification
- Mobile responsiveness testing

## 📱 Mobile Support

Little Lores is fully responsive and optimized for:
- **Mobile Phones**: Touch-friendly controls, optimized layouts
- **Tablets**: Enhanced reading experience with larger text areas
- **Desktop**: Full-featured experience with all controls visible

### Mobile-Specific Features
- Horizontal scrolling for reading controls
- Touch-optimized sliders and buttons
- Responsive grid layouts
- Mobile-friendly navigation

## 🔒 Privacy & Security

- **Minimal Data Collection**: Only necessary user information is stored
- **Secure Authentication**: Google OAuth integration
- **Child-Safe Environment**: No external links or inappropriate content
- **COPPA Considerations**: Designed with child privacy in mind

## 🤝 Contributing

We welcome contributions to Little Lores! Here are ways you can help:

### Story Content
- Submit traditional folk stories from your culture
- Review stories for cultural accuracy
- Translate existing stories to other languages

### Technical Improvements
- Bug fixes and performance optimizations
- New features and enhancements
- Accessibility improvements
- Mobile app development

### Process
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Story Sources**: Traditional folk tales from public domain collections
- **Voice Technology**: Web Speech API contributors
- **Design Inspiration**: Educational apps and children's reading platforms
- **Cultural Consultants**: Community members who helped verify story authenticity

## 📞 Support

- **Issues**: Report bugs or request features via [GitHub Issues](https://github.com/ccalde29/LittleLoreApp/issues)
- **Discussions**: Join conversations in [GitHub Discussions](https://github.com/ccalde29/LittleLoreApp/discussions)
- **Documentation**: Full documentation available in the `/docs` folder

## 🎯 Roadmap

### Upcoming Features
- [ ] **Native Mobile Apps** (iOS/Android)
- [ ] **Offline Reading** capability
- [ ] **Parent Dashboard** with analytics
- [ ] **Achievement System** and badges
- [ ] **Multi-language Support**
- [ ] **Classroom Integration** tools
- [ ] **Story Bookmarking** within texts
- [ ] **Reading Streak Tracking**

### Long-term Goals
- [ ] **AI-Powered Recommendations**
- [ ] **Interactive Story Elements**
- [ ] **Community Story Submissions**
- [ ] **Educational Standards Alignment**
- [ ] **Accessibility Enhancements**

## 📊 Current Status

- **Version**: 2.9 (Beta)
- **Stories**: 3,000+ traditional folk tales
- **Regions**: 5 major world regions covered
- **Grade Levels**: K-8 supported
- **Voice Options**: 6 categorized voice types
- **Platform**: Web-based (GitHub Pages)

---

**Made with ❤️ for young readers around the world**

*Little Lores aims to foster global understanding and reading skills through the timeless art of storytelling.*