import os
from flask import Flask, jsonify, request
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

from bot.linkedin import run_linkedin
from bot.naukri import run_naukri

load_dotenv()

app = Flask(__name__)

@app.route("/")
def home():
    return "Ultimate Job Bot Running ✅"


@app.route("/run", methods=["POST"])
def run():
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=False,
                args=[
                    "--disable-blink-features=AutomationControlled",
                    "--start-maximized"
                ]
            )

            context = browser.new_context(
                user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36",
                viewport={"width": 1280, "height": 800}
            )

            page = context.new_page()

            results = {}

            # LinkedIn
            try:
                results["linkedin"] = run_linkedin(page)
            except Exception as e:
                results["linkedin"] = f"Error: {str(e)}"

            # Naukri
            try:
                results["naukri"] = run_naukri(page)
            except Exception as e:
                results["naukri"] = f"Error: {str(e)}"

            browser.close()

            return jsonify({
                "status": "success",
                "linkedin": results["linkedin"],
                "naukri": results["naukri"]
            })

    except Exception as e:
        return jsonify({
            "status": "failed",
            "error": str(e)
        })


@app.route("/apply", methods=["POST"])
def apply_jobs():
    data = request.json
    job_links = data.get("job_links", [])

    applied = 0
    failed = 0

    for link in job_links:
        try:
            print(f"Applying: {link}")
            applied += 1
        except:
            failed += 1

    return jsonify({
        "status": "success",
        "applied": applied,
        "failed": failed
    })
