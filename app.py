import os
from flask import Flask, jsonify, request
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

from bot.linkedin import run_linkedin
from bot.naukri import run_naukri

load_dotenv()

app = Flask(__name__)

# -------------------------------
# HEALTH CHECK
# -------------------------------
@app.route("/")
def home():
    return "Ultimate Job Bot Running ✅"


# -------------------------------
# PROFILE UPDATE (LinkedIn + Naukri)
# -------------------------------
@app.route("/run", methods=["POST"])
def run():
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True,
                args=["--no-sandbox", "--disable-dev-shm-usage"]
            )

            page = browser.new_page()

            results = {}

            # LinkedIn
            try:
                results["linkedin"] = run_linkedin(
                    page,
                    os.getenv("LINKEDIN_EMAIL"),
                    os.getenv("LINKEDIN_PASSWORD"),
                    int(os.getenv("MAX_APPLIES", 5))
                )
            except Exception as e:
                results["linkedin"] = f"Error: {str(e)}"

            # Naukri
            try:
                results["naukri"] = run_naukri(
                    page,
                    os.getenv("NAUKRI_EMAIL"),
                    os.getenv("NAUKRI_PASSWORD")
                )
            except Exception as e:
                results["naukri"] = f"Error: {str(e)}"

            browser.close()

            return jsonify({
                "status": "success",
                "results": results
            })

    except Exception as e:
        return jsonify({
            "status": "failed",
            "error": str(e)
        })


# -------------------------------
# AUTO APPLY API (for n8n)
# -------------------------------
@app.route("/apply", methods=["POST"])
def apply_jobs():
    try:
        data = request.json
        job_links = data.get("job_links", [])

        applied = 0
        failed = 0

        # (Basic simulation — extend later)
        for link in job_links:
            try:
                print(f"Applying to: {link}")
                applied += 1
            except:
                failed += 1

        return jsonify({
            "status": "success",
            "applied": applied,
            "failed": failed
        })

    except Exception as e:
        return jsonify({
            "status": "failed",
            "error": str(e)
        })
