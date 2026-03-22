from bot.helpers import human_delay, safe_click

def run_linkedin(page, email, password, max_apply=5):
    results = {"posted": False, "applied": 0}

    page.goto("https://www.linkedin.com/login")
    page.fill("#username", email)
    page.fill("#password", password)
    page.click("button[type=submit]")
    human_delay()

    page.goto("https://www.linkedin.com/feed/")
    human_delay()

    if safe_click(page, "button:has-text('Start a post')"):
        human_delay()
        page.fill("div[role='textbox']",
                  "Actively seeking Data Analyst roles | SQL | Power BI | Excel | Python")
        safe_click(page, "button:has-text('Post')")
        results["posted"] = True
        human_delay()

    page.goto("https://www.linkedin.com/jobs/search/?keywords=Data%20Analyst")
    human_delay()

    jobs = page.locator("a.job-card-container").all()[:max_apply]

    for job in jobs:
        try:
            job.click()
            human_delay()

            if safe_click(page, "button:has-text('Easy Apply')"):
                human_delay()

                if safe_click(page, "button:has-text('Submit')"):
                    results["applied"] += 1
                    human_delay()
        except:
            continue

    return results
