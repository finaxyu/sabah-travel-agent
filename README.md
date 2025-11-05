# 🏝️ Sabah Tourism AI Platform

> **Connecting travelers with authentic kampung experiences in Sabah, Malaysia**

An intelligent travel assistant that helps tourists discover hidden gems in Sabah's remote kampungs (villages) while empowering local operators with digital tools. Built with **100% free and open-source technology**.

![Platform](https://img.shields.io/badge/Cost-RM_0.00-green)
![AI](https://img.shields.io/badge/AI-Groq_Llama_3.3-blue)
![Maps](https://img.shields.io/badge/Maps-OpenStreetMap-orange)
![Python](https://img.shields.io/badge/Python-3.9+-yellow)

---

## 🎯 Problem We're Solving

**Challenge**: 500+ homestays and tour operators in Sabah's remote kampungs (like Kinabatangan, Penampang, Ranau) have **zero online visibility**.

**Impact**:
- Local operators miss 80% of potential customers
- Travelers can't discover authentic kampung experiences
- Cultural heritage tourism remains hidden

**Our Solution**: AI-powered platform that bridges the gap between remote operators and travelers.

---

## ✨ Key Features

### 1. 🤖 AI Travel Itinerary Planner
- Natural language queries: *"Plan a nature trip to Kinabatangan"*
- Discovers homestays, restaurants, and cultural sites
- Real-time data from OpenStreetMap
- Direct Google Maps integration

### 2. 🌍 Multilingual AI Chatbot
- Real-time translation: English ↔ Malay ↔ Chinese ↔ Japanese
- Helps international tourists communicate with local operators
- Breaks language barriers in rural tourism

### 3. 📝 AI Listing Generator (For Operators)
- Transforms simple descriptions into professional tourism listings
- No technical skills required
- Generates in 30 seconds
- Downloadable markdown format

---

## 🚀 Quick Start 

### Prerequisites

- **Python 3.9+** - [Download here](https://www.python.org/downloads/)
- **Git** - [Download here](https://git-scm.com/downloads)
- **VS Code** (recommended) - [Download here](https://code.visualstudio.com/)
- **Groq API Key** (FREE) - [Get it here](https://console.groq.com/)

### Step 1: Clone the Repository

```bash
# Clone the project
git clone https://github.com/YOUR-USERNAME/sabah-tourism-ai.git

# Navigate to project folder
cd sabah-tourism-ai
```

### Step 2: Set Up Virtual Environment

**Windows:**
```bash
# Create virtual environment
python -m venv venv

# Activate it
venv\Scripts\activate
```

**Mac/Linux:**
```bash
# Create virtual environment
python3 -m venv venv

# Activate it
source venv/bin/activate
```

You should see `(venv)` at the start of your terminal prompt.

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Get Your FREE Groq API Key

1. Go to [https://console.groq.com/](https://console.groq.com/)
2. Sign up with your Google account (takes 30 seconds)
3. Click **"Create API Key"**
4. Copy the key (starts with `gsk_...`)

### Step 5: Configure API Keys

Create a folder and file:

```bash
mkdir .streamlit
```

Create `.streamlit/secrets.toml` and add:

```toml
GROQ_API_KEY = "gsk_your_actual_key_here"
```

⚠️ **IMPORTANT**: Never commit this file to GitHub! It's already in `.gitignore`.

### Step 6: Run the App

```bash
streamlit run app.py
```

Your browser will automatically open to `http://localhost:8501` 🎉

---

## 📁 Project Structure

```
sabah-tourism-ai/
├── app.py                    # Main application
├── requirements.txt          # Python dependencies
├── README.md                # This file
├── .gitignore               # Git ignore rules
├── .streamlit/
│   └── secrets.toml         # API keys (NOT in git!)
└── venv/                    # Virtual environment (NOT in git!)
```

---

## 🧪 Testing the App

### Test Queries for Travelers:

```
✅ "Show me attractions in Kota Kinabalu"
✅ "Find restaurants in Sandakan"
✅ "Where to stay in Kinabatangan"
✅ "Food places in Tawau"
✅ "Cultural experiences in Penampang"
```

### Test Operator Listing Generator:

1. Click **"Create Professional Listing"** in sidebar
2. Fill in:
   - Business Name: `Kampung Penampang Homestay`
   - Location: `Penampang, Sabah`
   - Type: `Homestay`
   - Description: `Traditional Kadazan homestay with cultural activities`
3. Click **"Generate"**
4. Download the listing!

### Test Multilingual Feature:

1. Select language from sidebar (Bahasa Malaysia / 中文 / 日本語)
2. Ask any question
3. Watch it auto-translate! 🌍

---

## 🤝 Team Workflow (Git Basics)

### Before You Start Working:

```bash
# Get latest code from team
git pull origin main
```

### After You Make Changes:

```bash
# Check what you changed
git status

# Add your changes
git add .

# Commit with a clear message
git commit -m "Added feature: multilingual support for Japanese"

# Push to GitHub
git push origin main
```

### If You Get Merge Conflicts:

1. Don't panic! 😊
2. Open the conflicting file in VS Code
3. VS Code shows options: "Accept Current" or "Accept Incoming"
4. Choose one, save the file
5. Then:
```bash
git add .
git commit -m "Resolved merge conflict"
git push
```

---

## 🛠️ Common Issues & Solutions

### Issue 1: "Module not found"
```bash
# Solution: Reinstall dependencies
pip install -r requirements.txt
```

### Issue 2: "API key invalid"
```bash
# Solution: Check your .streamlit/secrets.toml
# Make sure:
# - Quotes are straight (" not ")
# - No extra spaces
# - Key starts with "gsk_"
```

### Issue 3: "Port 8501 already in use"
```bash
# Windows: Kill the process
netstat -ano | findstr :8501
taskkill /PID <number> /F

# Mac/Linux: Kill the process
lsof -ti:8501 | xargs kill -9
```

### Issue 4: "Location not found"
```
# OpenStreetMap works best with larger towns
# Try: Kota Kinabalu, Sandakan, Tawau, Kudat
# Instead of very small kampungs
```

### Issue 5: Model error (like you had)
```python
# Update model in app.py line ~35
model="llama-3.3-70b-versatile"  # Use latest model
```

---

## 💰 Cost Breakdown (For Hackathon Budget)

| Service | Cost | Usage |
|---------|------|-------|
| Groq AI (Llama 3.3) | **FREE** | Unlimited (fair use) |
| OpenStreetMap | **FREE** | Unlimited |
| Streamlit Hosting | **FREE** | 1 app |
| **TOTAL** | **RM 0.00** | ✨ |

---

## 🚢 Deploying to Production (FREE Hosting)

### Option 1: Streamlit Cloud (Recommended)

1. Push all code to GitHub
2. Go to [https://share.streamlit.io/](https://share.streamlit.io/)
3. Sign in with GitHub
4. Click **"New app"**
5. Select your repo: `sabah-tourism-ai`
6. Set main file: `app.py`
7. Click **"Advanced settings"** → Add secrets:
   ```toml
   GROQ_API_KEY = "gsk_your_key"
   ```
8. Click **"Deploy"**
9. Wait 3-5 minutes
10. Get your URL: `https://sabah-tourism-ai-yourname.streamlit.app`

Share this URL with judges and users! 🎉
---

### Key Stats to Mention:
- ✅ Zero cost platform (RM 0.00/month)
- ✅ 4 languages supported
- ✅ 30-second listing generation
- ✅ Community-driven data (OpenStreetMap)
- ✅ Works in remote areas

---

## 📊 Technical Architecture

```
User Query
    ↓
Streamlit UI
    ↓
Groq AI (Llama 3.3) ← Extracts location & intent
    ↓
Nominatim API ← Gets GPS coordinates (FREE)
    ↓
Overpass API ← Searches places (FREE)
    ↓
Groq AI ← Generates friendly response
    ↓
Display Results + Google Maps links
```

**Why This Stack?**
- **Groq**: Fastest free LLM (faster than GPT-3.5)
- **OpenStreetMap**: Community data = better rural coverage
- **Streamlit**: Fast prototyping, free hosting
- **No database needed**: Real-time data from APIs

---

## 📚 Learning Resources

**Streamlit Documentation**: https://docs.streamlit.io/
**Groq API Docs**: https://console.groq.com/docs
**OpenStreetMap**: https://wiki.openstreetmap.org/
**Python Tutorial**: https://www.python.org/about/gettingstarted/
**Git Basics**: https://www.atlassian.com/git/tutorials

---

## 📝 License

MIT License - Free to use, modify, and distribute.

This project is built for social good and empowering rural communities. 💚

---

## 🙏 Acknowledgments

- **OpenStreetMap Contributors** - For community-driven map data
- **Groq** - For providing free, fast AI infrastructure
- **Sabah Tourism Operators** - The inspiration for this project
- **Our Hackathon Mentors** - For guidance and support

---

## 📞 Contact & Support

**GitHub Issues**: [Report bugs here](https://github.com/YOUR-USERNAME/sabah-tourism-ai/issues)

**Demo URL**: `https://sabah-tourism-ai.streamlit.app` *(after deployment)*

**Team Email**: your-team-email@example.com

---

## 🚀 Ready to Make an Impact!

This project can genuinely help Sabah's kampung operators gain visibility and compete in the digital tourism economy. Let's make it happen! 🏝️

**For team members**: Follow the Quick Start guide above and you'll be running the app in 10 minutes!

**For judges**: Check our live demo and see how we're solving real problems with innovative technology!

---

Made with ❤️ for Sabah's Tourism Community | Hackathon 2025
