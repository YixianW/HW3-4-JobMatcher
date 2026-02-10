# JobMatcher - Intelligent Job Opportunity Analyzer

## Overview

**JobMatcher** is a smart job search application designed to help professionals find role opportunities that best align with their background, skills, and visa sponsorship requirements. Instead of manually browsing through hundreds of job postings, JobMatcher automatically filters, scores, and ranks job opportunities based on multi-step matching logic.

### Why JobMatcher?

Job hunting can be overwhelming, especially for professionals seeking:
- **High-match roles** tailored to their specific skill set
- **Visa sponsorship opportunities** (H1-B, etc.)
- **Recently posted positions** to stay competitive
- **Strategic career alignment** with their professional background

JobMatcher solves this by combining AI-powered job matching with real-time job market data from the Adzuna API.

---

## Features

### 1. **Intelligent Job Matching Algorithm**
The application uses a multi-step matching engine that evaluates:
- **Title Relevance**: Does the job title match your search criteria?
- **Skill Alignment**: Do your core skills (Python, Tableau, Product Management, etc.) appear in the job description?
- **Strategic Fit**: Does the role align with your MBA specialization and professional experience?
- **Visa Sponsorship Audit**: Does the employer explicitly mention visa sponsorship or legal authorization support?

### 2. **Smart Scoring System**
- Each job receives a score from 0-10 based on the matching criteria
- Only positions scoring 4 or higher are displayed (filtering out poor matches)
- Results are automatically sorted by match score (highest to lowest)

### 3. **Real-time Job Data**
- Integrates with the Adzuna API to fetch the latest US job postings
- Returns 10 most relevant opportunities per search
- Reduces manual browsing time significantly

### 4. **Customizable Profile**
- Define your education background (e.g., MBA, CMU Tepper with specific focuses)
- List your technical and domain skills
- Highlight relevant work experience
- The algorithm automatically matches your profile against job requirements

---

## How It Works

1. **User enters a job search keyword** (e.g., "Product Manager", "Data Analyst")
2. **Application queries the Adzuna API** for the latest US job postings matching the keyword
3. **Multi-step matching algorithm analyzes each posting** against the user's profile
4. **Results are scored and ranked** by relevance
5. **Top 10 matches are displayed** with:
   - Job title and company name
   - Location and job URL
   - Match score (0-10)
   - Visa sponsorship likelihood
   - Key matching reasons

---

## Installation & Setup

### Prerequisites
- Python 3.8+
- Adzuna API credentials (free account at [https://www.adzuna.com/api](https://www.adzuna.com/api))

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd HW3-JobMatcher
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Configure API Credentials
The application securely reads API credentials from environment variables:

**Locally (for development):**
```bash
export ADZUNA_ID="your_adzuna_app_id"
export ADZUNA_KEY="your_adzuna_app_key"
```

**On deployment platform (e.g., Render):**
- Add `ADZUNA_ID` and `ADZUNA_KEY` to your environment variables in the platform's dashboard

### Step 4: Run the Application
```bash
python app.py
```
The application will be available at `http://localhost:5000`

---

## Usage

1. **Open the web interface** at `http://localhost:5000`
2. **Enter a job search keyword** (e.g., "Product Manager", "Data Science", "Strategy")
3. **Click "Search"** to analyze matching opportunities
4. **Review results** sorted by match score
5. **Click job links** to apply directly on the employer's website

---

## Architecture

### Core Components

| Component | Purpose |
|-----------|---------|
| `app.py` | Flask backend with job matching logic |
| `templates/index.html` | Web interface for search and results display |
| `requirements.txt` | Python dependencies |

### Key Functions

- **`analyze_aria_fit(search_query, job_title, description)`**: Core matching engine that evaluates job relevance across 4 dimensions
- **`@app.route('/', methods=['GET', 'POST'])`**: Main Flask route handling search requests and API calls

---

## Customization

### Edit Your Profile
Modify the `MY_PROFILE` dictionary in `app.py` to match your own background:

```python
MY_PROFILE = {
    "education": "Your degree and specialization",
    "skills": ["Your", "Key", "Skills"],
    "experience": ["Your", "Work", "Experience"]
}
```

### Adjust Matching Weights
The matching algorithm assigns different weights to each criterion. You can fine-tune scores by editing the `analyze_aria_fit()` function:
- Title match: +3 points
- Skill match: +2 points
- Strategic fit: +2 points
- Base score: 5 points
- Minimum display threshold: 4 points

---

## Security Considerations

✅ **Best Practices Implemented:**
- API credentials stored in environment variables (not hardcoded)
- Safe deployment on platforms like Render or Heroku
- No sensitive data stored in the repository

---

## Technologies Used

- **Backend**: Flask (Python web framework)
- **API**: Adzuna Job Search API
- **Frontend**: HTML/CSS/JavaScript
- **Deployment**: Prepared for Render, Heroku, or similar PaaS platforms

---

## Future Enhancements

- [ ] Support for multiple job markets (UK, Canada, Australia, etc.)
- [ ] Email alerts for new high-match opportunities
- [ ] User authentication and saved searches
- [ ] Salary range filtering and negotiation insights
- [ ] LinkedIn integration for profile auto-fill
- [ ] AI-powered cover letter suggestions
- [ ] Company culture and benefits matching

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| API Error: 403 Unauthorized | Verify your ADZUNA_ID and ADZUNA_KEY in environment variables |
| No results returned | Try a broader search keyword (e.g., "Manager" instead of "Senior Manager") |
| Slow response time | Adzuna API may be rate-limited; wait a few moments and retry |
| Flask not starting | Ensure port 5000 is not in use, or run `app.run(port=5001)` |

---

## Contributing

Contributions are welcome! To contribute:
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/improvement`)
3. Commit changes (`git commit -m "Add improvement"`)
4. Push to branch (`git push origin feature/improvement`)
5. Open a pull request

---

## License

This project is open source and available under the MIT License.

---

## Contact & Support

For questions, feedback, or support, please open an issue on GitHub or contact the project maintainer.

---

**Happy job hunting! 🚀**