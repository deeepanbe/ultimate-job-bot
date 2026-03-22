import os
from flask import Flask, jsonify
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright
from bot.linkedin import run_linkedin
from bot.naukri import run_naukri

load_dotenv()

app = Flask(__name__)

@app.route("/run", methods=["POST"])
def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()

        results = {}

        results["linkedin"] = run_linkedin(
            page,
            os.getenv("LINKEDIN_EMAIL"),
            os.getenv("LINKEDIN_PASSWORD"),
            int(os.getenv("MAX_APPLIES", 5))
        )

        results["naukri"] = run_naukri(
            page,
            os.getenv("NAUKRI_EMAIL"),
            os.getenv("NAUKRI_PASSWORD")
        )

        browser.close()

        return jsonify(results)

@app.route("/")
def home():
    return "Ultimate Job Bot Running"
