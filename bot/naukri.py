import random
from bot.helpers import human_delay

HEADLINES = [
    "Data Analyst | SQL | Power BI | Excel",
    "Data Analyst | Python | Dashboard | SQL",
    "Data Analyst | Power BI | Excel | Insights"
]

def run_naukri(page, email, password):
    page.goto("https://www.naukri.com/")
    human_delay()

    try:
        page.fill("#usernameField", email)
        page.fill("#passwordField", password)
        page.click("button[type='submit']")
        human_delay()
    except:
        pass

    page.goto("https://www.naukri.com/mnjuser/profile")
    human_delay()

    try:
        page.fill("input[name='resumeHeadline']", random.choice(HEADLINES))
        page.click("button:has-text('Save')")
        human_delay()
        return True
    except:
        return False
