import os
from bot.helpers import human_delay

def run_linkedin(page):
    email = os.getenv("LINKEDIN_EMAIL")
    password = os.getenv("LINKEDIN_PASSWORD")

    page.goto("https://www.linkedin.com/login")
    human_delay()

    page.fill('input[name="session_key"]', email)
    page.fill('input[name="session_password"]', password)

    page.click('button[type="submit"]')
    human_delay()

    # CAPTCHA check
    if "captcha" in page.content().lower():
        return "captcha_detected"

    # Go to feed
    page.goto("https://www.linkedin.com/feed/")
    human_delay()

    # Create post
    post_text = "Actively exploring Data Analyst roles | SQL | Power BI | Excel | Python"

    try:
        page.click("button[aria-label='Start a post']")
        human_delay()

        page.fill("div[role='textbox']", post_text)
        human_delay()

        page.click("button[aria-label='Post']")
        human_delay()

        return "posted"

    except:
        return "post_failed"
