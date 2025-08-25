
# from flask import Flask, request, jsonify
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


# # API Endpoint: Get company research
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

#     ### Last 1 Year Revenue
#     - Revenue (2024): ...

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


# # Optional: Health check
# @app.route("/health", methods=["GET"])
# def health():
#     return jsonify({"status": "OK", "timestamp": datetime.now().isoformat()})


# if __name__ == "__main__":
#     app.run(debug=True, host="0.0.0.0", port=5000)

from flask import Flask, request, jsonify
from flask_cors import CORS  # Import CORS
import os
import requests
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

app = Flask(__name__)




ALLOWED_ORIGINS = ["*"]

CORS(
    app,
    resources={r"/api/*": {"origins": ALLOWED_ORIGINS}},
    supports_credentials=True,                           # allow cookies/Authorization
    allow_headers=["Authorization", "Content-Type"],     # match your client
    expose_headers=["Content-Disposition"],              # if you need to read these
    methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    max_age=86400,                                       # cache preflight 24h
)

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


# Health check
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "OK", "timestamp": datetime.now().isoformat()})


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)