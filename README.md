# Aria's Job Matcher - HW4 Backend + Frontend Separation

## Architecture Overview

This is a **decoupled architecture** where:
- **Backend**: Flask API running on Render (handles job search logic and API calls)
- **Frontend**: HTML/CSS/JavaScript on GitHub Pages (user interface and frontend logic)
- **Communication**: Fetch API via CORS-enabled HTTP requests

```
GitHub Pages Frontend (index.html)
        ↓ (fetch requests via CORS)
Render Backend API (app.py)
        ↓ (HTTP requests)
Adzuna Job API
```

## Backend Setup (Render Deployment)

### 1. Environment Variables
Set these in your Render environment variables panel:

```
ADZUNA_ID=your_adzuna_app_id
ADZUNA_KEY=your_adzuna_api_key
PORT=8000  # Optional, defaults to 5000
```

⚠️ **IMPORTANT**: Never commit these credentials to GitHub. Always use Render's environment variable settings.

### 2. API Endpoints

#### GET `/`
Health check endpoint
```bash
curl https://aria-job-matcher.onrender.com/
# Response: {"message": "Job Matcher API - Backend is running..."}
```

#### POST `/search`
Main job search endpoint
```bash
curl -X POST https://aria-job-matcher.onrender.com/search \
  -H "Content-Type: application/json" \
  -d '{"keyword": "Product Manager"}'
```

**Request Format:**
```json
{
  "keyword": "Product Manager"
}
```

**Response Format:**
```json
{
  "success": true,
  "results": [
    {
      "score": 8,
      "sponsor": "Direct Mention (High Probability)",
      "title": "Senior Product Manager",
      "company": "Tech Corp",
      "location": "San Francisco, CA",
      "url": "https://...",
      "reasons": [
        "Title Match: This is a targeted 'product manager' position.",
        "Technical Match: Your expertise in Product Management, Strategy...",
        "Strategic Fit: Your Tepper MBA track and Baidu ML experience..."
      ]
    }
  ]
}
```

### 3. CORS Configuration
The backend has CORS enabled for all origins using `flask_cors`. This allows the frontend on GitHub Pages to make requests without browser security restrictions.

```python
from flask_cors import CORS
app = Flask(__name__)
CORS(app)  # Allow all origins
```

## Frontend Setup (GitHub Pages)

### 1. Static Files
Only three files are needed for GitHub Pages:
- `index.html` - Contains UI and JavaScript
- Images/CSS can be included inline or via external CDN
- No Flask templates or Python required

### 2. Backend URL Configuration
The frontend automatically detects the environment:

```javascript
const BACKEND_URL = window.location.hostname === 'localhost' 
    ? 'http://localhost:5000'      // Local development
    : 'https://aria-job-matcher.onrender.com';  // Production
```

**To use your actual Render URL**, update this line in `index.html`:
```javascript
const BACKEND_URL = 'https://your-render-app.onrender.com';
```

### 3. Frontend Features
- **Form Handling**: Prevents page reload, uses Fetch API instead
- **Error Handling**: Shows user-friendly error messages if backend is down
- **Dynamic Rendering**: Builds job cards purely from JavaScript
- **Security**: Escapes all HTML to prevent XSS attacks

## Local Development

### Prerequisites
```bash
python3 --version  # Ensure Python 3.8+
```

### 1. Clone Repository
```bash
git clone <repository-url>
cd HW3-JobMatcher
```

### 2. Install Backend Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Environment Variables (Local)
```bash
export ADZUNA_ID=your_app_id
export ADZUNA_KEY=your_api_key
```

Or create a `.env` file (never commit this):
```
ADZUNA_ID=your_app_id
ADZUNA_KEY=your_api_key
```

### 4. Run Backend Locally
```bash
python app.py
# Server runs at http://localhost:5000
```

### 5. View Frontend Locally
Simply open the HTML file in your browser:
```bash
open templates/index.html
# Or right-click → Open with Browser
```

The frontend will connect to `http://localhost:5000` automatically when running locally.

## Deployment Guide

### Backend Deployment (Render)

1. **Connect Repository**
   - Go to render.com
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Select `main` branch

2. **Configure Service**
   - Name: `aria-job-matcher`
   - Environment: `Python 3`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`

3. **Set Environment Variables**
   - In Render Dashboard → Your Service
   - Click "Environment" tab
   - Add `ADZUNA_ID` and `ADZUNA_KEY`

4. **Deploy**
   - Click "Deploy" to build and run
   - Check logs for any errors
   - Your API will be available at `https://aria-job-matcher.onrender.com`

### Frontend Deployment (GitHub Pages)

1. **Create GitHub Pages Branch**
   - Create a new branch: `gh-pages`
   - OR use your `main` branch if your repo is `username.github.io`

2. **Copy Frontend Files**
   - Copy `templates/index.html` to the root or `docs/index.html`
   - Update the `BACKEND_URL` to your Render URL

3. **Enable GitHub Pages**
   - Go to Repository Settings
   - Scroll to "GitHub Pages" section
   - Select source: `main` branch (root folder) or `gh-pages` branch
   - Wait for the green checkmark

4. **Access Your Site**
   - URL: `https://yixianw.github.io/HW3-JobMatcher/`
   - The frontend will now communicate with the Render backend

## Project Structure

```
HW3-JobMatcher/
├── app.py                    # Flask backend (API only)
├── requirements.txt          # Python dependencies
├── runtime.txt              # Python version for Render
├── README.md                # This file
└── templates/
    └── index.html           # Frontend (HTML + JavaScript)
```

## Key Changes from HW3 to HW4

### Backend Changes
| Aspect | HW3 | HW4 |
|--------|-----|-----|
| Route | `/` returns HTML (POST) | `/search` returns JSON (POST) |
| Templates | Uses Jinja2 templates | API-only, no templates |
| Response | HTML rendered server-side | JSON data, rendered client-side |
| Hosting | Single Flask app | Separate backend API |

### Frontend Changes
| Aspect | HW3 | HW4 |
|--------|-----|-----|
| Form Submit | Page reload (POST to `/`) | JavaScript fetch (POST to `/search`) |
| Data Rendering | Server-side (Jinja2) | Client-side (JavaScript) |
| Hosting | Same Flask server | GitHub Pages |
| Connectivity | Direct (same origin) | CORS-enabled (different origin) |

## Troubleshooting

### "Failed to fetch jobs: Failed to fetch"
- **Cause**: Backend URL is incorrect or backend is down
- **Solution**: 
  1. Check backend is running: Visit `https://your-backend-url/` in your browser
  2. Verify `BACKEND_URL` in `index.html` is correct
  3. Check that ADZUNA credentials are set

### "API request failed with status 500"
- **Cause**: Backend error (likely missing environment variables)
- **Solution**: 
  1. Check Render logs for error details
  2. Verify `ADZUNA_ID` and `ADZUNA_KEY` are set in Render environment
  3. Restart the Render service

### "CORS error" in browser console
- **Cause**: Backend doesn't have CORS enabled
- **Solution**: Ensure `from flask_cors import CORS` and `CORS(app)` are in `app.py`

### Frontend shows "No matching jobs found"
- **Cause**: Search keyword doesn't match any job listings
- **Solution**: Try broader search terms like "Product", "Engineer", "Manager"

## Security Features

✅ **Environment Variables**: API credentials stored in Render, not in code
✅ **CORS Enabled**: Frontend can safely communicate with backend
✅ **HTML Escaping**: All user input is escaped to prevent XSS attacks
✅ **Error Handling**: User-friendly errors that don't expose sensitive info
✅ **HTTPS**: GitHub Pages and Render both enforce HTTPS

## Technologies Used

- **Backend**: Flask, Flask-CORS, Requests, Gunicorn
- **Frontend**: HTML5, CSS3, Vanilla JavaScript (Fetch API)
- **Hosting**: Render (backend), GitHub Pages (frontend)
- **External API**: Adzuna Job Search API

## Features Preserved from HW3

### Intelligent Job Matching Algorithm
The application continues to use a multi-step matching engine that evaluates:
- **Title Relevance**: Does the job title match your search criteria?
- **Skill Alignment**: Do your core skills (Python, Tableau, Product Management, etc.) appear in the job description?
- **Strategic Fit**: Does the role align with your MBA specialization and professional experience?
- **Visa Sponsorship Audit**: Does the employer explicitly mention visa sponsorship or legal authorization support?

### Smart Scoring System
- Each job receives a score from 0-10 based on the matching criteria
- Only positions scoring 4 or higher are displayed (filtering out poor matches)
- Results are automatically sorted by match score (highest to lowest)

### Real-time Job Data
- Integrates with the Adzuna API to fetch the latest US job postings
- Returns 10 most relevant opportunities per search
- Reduces manual browsing time significantly

## Future Enhancements

- [ ] User authentication and saved preferences
- [ ] Search history and analytics
- [ ] Email notifications for new matching jobs
- [ ] Advanced filtering (salary, industry, location)
- [ ] Dark mode UI toggle
- [ ] Mobile app version

## Support

For issues or questions:
1. Check the Troubleshooting section above
2. Review error logs in Render Dashboard
3. Check browser console for JavaScript errors (Press F12)
4. Verify all environment variables are correctly set

---

**Last Updated**: February 2026
**Architecture**: Backend API + Frontend Static Site (HW4 Style)
**Status**: Production Ready ✅