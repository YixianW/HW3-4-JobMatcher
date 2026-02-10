import os
import requests
from flask import Flask, render_template, request

app = Flask(__name__)

# --- 1. 安全配置：从系统环境变量读取 Key，防止 GitHub 泄露 ---
# 在 Render 的 Environment Variables 面板中设置这两个变量
ADZUNA_ID = os.environ.get('ADZUNA_ID')
ADZUNA_KEY = os.environ.get('ADZUNA_KEY')

# --- 2. 你的简历核心背景 (已根据 Aria Wang 的最新简历锁定) ---
MY_PROFILE = {
    "education": "MBA, CMU Tepper (AI in Business; Technology Strategy & Product Management)",
    "skills": ["Python", "Tableau", "Product Management", "Marketing", "Go-to-Market Strategy", "Digital Advertising", "Data Analysis"],
    "experience": ["Baidu ML-based ad analysis", "Growth Strategy at Hai De Han", "AR App Launch"]
}

def analyze_aria_fit(search_query, job_title, description):
    """
    HW3 Core Logic: Multi-step Reasoning
    Step 1: Title Relevance
    Step 2: Skill Alignment
    Step 3: MBA Strategic Match
    Step 4: Visa Sponsorship Audit
    """
    description = description.lower()
    job_title_lower = job_title.lower()
    search_query = search_query.lower()
    
    reasons = []
    score = 5 # Base score

    # Step 1: Title Relevance Check
    if search_query in job_title_lower:
        score += 3
        reasons.append(f"Title Match: This is a targeted '{search_query.capitalize()}' position.")
    else:
        score -= 2 

    # Step 2: Skill Alignment (Python, Tableau, GTM, etc.)
    matches = [s for s in MY_PROFILE["skills"] if s.lower() in description]
    if matches:
        score += 2
        reasons.append(f"Technical Match: Your expertise in {', '.join(matches[:3])} is highly relevant.")

    # Step 3: Strategic Fit (Baidu & Tepper MBA)
    strategy_terms = ["strategy", "product management", "roadmap", "ai", "machine learning"]
    if any(term in description for term in strategy_terms) or "mba" in description:
        score += 2
        reasons.append("Strategic Fit: Your Tepper MBA track and Baidu ML experience match the role's seniority.")

    # Step 4: Visa Sponsorship Audit (Addressing International Student Needs)
    sponsor_terms = ["h1-b", "sponsorship", "visa", "legal authorization"]
    can_sponsor = "Potential Match"
    if any(term in description for term in sponsor_terms):
        can_sponsor = "Direct Mention (High Probability)"

    return {
        "score": max(min(score, 10), 0),
        "sponsor": can_sponsor,
        "reasons": reasons[:3]
    }

@app.route('/', methods=['GET', 'POST'])
def index():
    results = []
    if request.method == 'POST':
        query = request.form.get('keyword', '').strip()
        
        # API Call for US jobs only
        url = f"https://api.adzuna.com/v1/api/jobs/us/search/1?app_id={ADZUNA_ID}&app_key={ADZUNA_KEY}&results_per_page=15&what={query}&sort_by=date"
        
        try:
            response = requests.get(url)
            data = response.json()
            if data.get('results'):
                for job in data['results']:
                    analysis = analyze_aria_fit(query, job['title'], job['description'])
                    
                    # Filter for relevance
                    if analysis['score'] >= 4:
                        analysis.update({
                            "title": job['title'], 
                            "company": job['company']['display_name'],
                            "location": job['location']['display_name'], 
                            "url": job['redirect_url']
                        })
                        results.append(analysis)
                
                # Sort results by match score
                results = sorted(results, key=lambda x: x['score'], reverse=True)[:10]
        except Exception as e:
            print(f"API Error: {e}")

    return render_template('index.html', results=results)

if __name__ == '__main__':
    # Flask default port is 5000
    app.run(debug=True)