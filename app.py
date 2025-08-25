# from flask import Flask, render_template, request, jsonify
# import os
# import requests
# from dotenv import load_dotenv
# from datetime import datetime

# # Load environment variables
# load_dotenv()

# app = Flask(__name__)

# # OpenRouter API Key
# OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
# if not OPENROUTER_API_KEY:
#     raise RuntimeError("OPENROUTER_API_KEY not found in .env file!")

# # Fixed: Removed extra spaces in URL
# OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"


# # API Endpoint for testing in Postman
# @app.route("/api/company", methods=["POST"])
# def api_company():
#     # Parse JSON input
#     data = request.get_json()
#     if not data:
#         return jsonify({"error": "No JSON provided"}), 400

#     company = data.get("company", "").strip()
#     if not company:
#         return jsonify({"error": "Missing 'company' field"}), 400

#     # Build prompt for full business report
#     prompt = f"""
#     You are a business research assistant. Provide a detailed, accurate, and up-to-date analysis of {company} focused on: All.

#     Use the following structure exactly:

#     ## Detailed Analysis: {company}

#     ### Company Snapshot
#     - **Full Name:** 
#     - **Industry:** 
#     - **Headquarters:** 
#     - **Size (Employees):** 
#     - **Description:** One-sentence overview.

#     ### Latest News (Past 1 year)
#     - Recent update (Month 2025): ...
#     - Recent update (Month 2025): ...

#     ### Key People
#     - Name – Role

#     ### Business Health
#     | Metric | Value |
#     |--------|-------|
#     | Revenue (Last Year) | ... |
#     | Stock Trend (1Y) | ... |
#     | Profitability | ... |

#     ### Litigations
#     - Summary of legal/regulatory issues.

#     ### Business Expansion Plan
#     - Strategic plans (2025–2030).

#     ### Competitor Comparison
#     | Competitor | Strength | Weakness vs {company} |
#     |----------|----------|------------------------|
#     | ... | ... | ... |

#     ### Hiring or Layoffs Plan
#     - Current workforce strategy.

#     Use real, verified data as of 2025. Avoid markdown code blocks. Keep tables clean.
#     """

#     try:
#         response = requests.post(
#             OPENROUTER_API_URL,
#             headers={
#                 "Authorization": f"Bearer {OPENROUTER_API_KEY}",
#                 "HTTP-Referer": "http://localhost:5000",
#                 "X-Title": "Company Research Assistant",
#                 "Content-Type": "application/json"
#             },
#             json={
#                 "model": "qwen/qwen3-30b-a3b",
#                 "messages": [{"role": "user", "content": prompt}],
#                 "temperature": 0.5,
#                 "max_tokens": 2000,
#                 "top_p": 0.9
#             }
#         )

#         if response.status_code == 200:
#             ai_response = response.json()["choices"][0]["message"]["content"].strip()
#             return jsonify({
#                 "company": company,
#                 "timestamp": datetime.now().isoformat(),
#                 "data": ai_response
#             })
#         else:
#             return jsonify({
#                 "error": "AI API error",
#                 "details": response.text
#             }), response.status_code

#     except Exception as e:
#         return jsonify({"error": "Request failed", "details": str(e)}), 500


# # Web Route
# @app.route("/", methods=["GET", "POST"])
# def index():
#     result = None
#     company = ""
#     now = None

#     if request.method == "POST":
#         company = request.form.get("company", "").strip()

#         if not company:
#             result = "Please enter a company name."
#         else:
#             now = datetime.now()

#             prompt = f"""
#             You are a business research assistant. Provide a detailed, accurate, and up-to-date analysis of {company} focused on: All.

#             Use the following structure exactly:

#             ## Detailed Analysis: {company}

#             ### Company Snapshot
#             - **Full Name:** 
#             - **Industry:** 
#             - **Headquarters:** 
#             - **Size (Employees):** 
#             - **Description:** One-sentence overview.

#             ### Latest News (Past 1 year)
#             - Recent update (Month 2025): ...
#             - Recent update (Month 2025): ...

#             ### Last 1 Year Revenue
#             - last 1 year revenue (Month 2025): ...

#             ### Key People
#             - Name – Role

#             ### Business Health
#             | Metric | Value |
#             |--------|-------|
#             | Revenue (Last Year) | ... |
#             | Stock Trend (1Y) | ... |
#             | Profitability | ... |

#             ### Litigations
#             - Summary of legal/regulatory issues.

#             ### Business Expansion Plan
#             - Strategic plans (2025–2030).

#             ### Competitor Comparison
#             | Competitor | Strength | Weakness vs {company} |
#             |----------|----------|------------------------|
#             | ... | ... | ... |

#             ### Hiring or Layoffs Plan
#             - Current workforce strategy.

#             Use real, verified data as of 2025. Avoid markdown code blocks. Keep tables clean.
#             """

#             try:
#                 response = requests.post(
#                     OPENROUTER_API_URL,
#                     headers={
#                         "Authorization": f"Bearer {OPENROUTER_API_KEY}",
#                         "HTTP-Referer": "http://localhost:5000",
#                         "X-Title": "Company Research Assistant",
#                         "Content-Type": "application/json"
#                     },
#                     json={
#                         "model": "qwen/qwen3-30b-a3b",
#                         "messages": [{"role": "user", "content": prompt}],
#                         "temperature": 0.5,
#                         "max_tokens": 2000,
#                         "top_p": 0.9
#                     }
#                 )

#                 if response.status_code == 200:
#                     data = response.json()
#                     result = data["choices"][0]["message"]["content"].strip()
#                 else:
#                     result = f"API Error: {response.status_code} - {response.text}"

#             except Exception as e:
#                 result = f"Request failed: {str(e)}"

#     return render_template("index.html", result=result, company=company, now=now)


# if __name__ == "__main__":
#     app.run(debug=True)


from flask import Flask, request, jsonify
import os
import requests
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

app = Flask(__name__)

# OpenRouter API Key
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
if not OPENROUTER_API_KEY:
    raise RuntimeError("OPENROUTER_API_KEY not found in .env file!")

# Fixed: Removed extra spaces in URL
OPENROUTER_API_URL = "https://openrouter.ai/api/v1/chat/completions"


# API Endpoint: Get company research
@app.route("/api/company", methods=["POST"])
def api_company():
    # Parse JSON input
    data = request.get_json()
    if not data:
        return jsonify({"error": "No JSON provided"}), 400

    company = data.get("company", "").strip()
    if not company:
        return jsonify({"error": "Missing 'company' field"}), 400

    # Build prompt for full business report
    prompt = f"""
    You are a business research assistant. Provide a detailed, accurate, and up-to-date analysis of {company} focused on: All.

    Use the following structure exactly:

    ## Detailed Analysis: {company}

    ### Company Snapshot
    - **Full Name:** 
    - **Industry:** 
    - **Headquarters:** 
    - **Size (Employees):** 
    - **Description:** One-sentence overview.

    ### Latest News (Past 1 year)
    - Recent update (Month 2025): ...
    - Recent update (Month 2025): ...

    ### Last 1 Year Revenue
    - Revenue (2024): ...

    ### Key People
    - Name – Role

    ### Business Health
    | Metric | Value |
    |--------|-------|
    | Revenue (Last Year) | ... |
    | Stock Trend (1Y) | ... |
    | Profitability | ... |

    ### Litigations
    - Summary of legal/regulatory issues.

    ### Business Expansion Plan
    - Strategic plans (2025–2030).

    ### Competitor Comparison
    | Competitor | Strength | Weakness vs {company} |
    |----------|----------|------------------------|
    | ... | ... | ... |

    ### Hiring or Layoffs Plan
    - Current workforce strategy.

    Use real, verified data as of 2025. Avoid markdown code blocks. Keep tables clean.
    """

    try:
        response = requests.post(
            OPENROUTER_API_URL,
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "HTTP-Referer": "http://localhost:5000",
                "X-Title": "Company Research Assistant",
                "Content-Type": "application/json"
            },
            json={
                "model": "qwen/qwen3-30b-a3b",
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.5,
                "max_tokens": 2000,
                "top_p": 0.9
            }
        )

        if response.status_code == 200:
            ai_response = response.json()["choices"][0]["message"]["content"].strip()
            return jsonify({
                "company": company,
                "timestamp": datetime.now().isoformat(),
                "data": ai_response
            })
        else:
            return jsonify({
                "error": "AI API error",
                "details": response.text
            }), response.status_code

    except Exception as e:
        return jsonify({"error": "Request failed", "details": str(e)}), 500


# Optional: Health check
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "OK", "timestamp": datetime.now().isoformat()})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)