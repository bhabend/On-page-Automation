from playwright.sync_api import sync_playwright

def fetch_rendered_html(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            page.goto(url, wait_until="networkidle", timeout=20000)
            html = page.content()
        except Exception as e:
            print(f"Error fetching {url}: {e}")
            html = ""
        browser.close()
        return html
