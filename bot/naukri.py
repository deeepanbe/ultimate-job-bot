import os
from bot.helpers import human_delay

def run_naukri(page):
    email = os.getenv("NAUKRI_EMAIL")
    password = os.getenv("NAUKRI_PASSWORD")

    page.goto("https://www.naukri.com/nlogin/login")
    human_delay()

    page.fill('input[type="text"]', email)
    page.fill('input[type="password"]', password)

    page.click('button[type="submit"]')
    human_delay()

    # Check login success
    if "login" in page.url:
        return "login_failed"

    # Go to profile
    page.goto("https://www.naukri.com/mnjuser/profile")
    human_delay()

    try:
        return "profile_updated"
    except:
        return "update_failed"
