import time, random

def human_delay(a=3, b=7):
    time.sleep(random.randint(a, b))

def safe_click(page, selector):
    if page.locator(selector).count() > 0:
        page.click(selector)
        return True
    return False
