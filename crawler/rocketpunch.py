from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd

INVALID_COMPANY_KEYWORDS = [
    "Rocketpunch", "서비스", "개인정보", "전문적인", "헤드헌팅", "©", "버그", "공지", "이용약관"
]

def is_valid_job(company: str, title: str) -> bool:
    # 회사명과 포지션 둘 다 있어야 하며, 금지 키워드를 포함하면 안 됨
    if not company or not title:
        return False
    for word in INVALID_COMPANY_KEYWORDS:
        if word in company or word in title:
            return False
    return True


def scroll_to_bottom(driver, scroll_pause=1.0, max_scrolls=10):
    last_height = driver.execute_script("return document.body.scrollHeight")
    scrolls = 0

    while scrolls < max_scrolls:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(scroll_pause)

        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
        scrolls += 1


def crawl_rocketpunch_selenium(keyword=None, seniority=None):
    base_url = "https://www.rocketpunch.com/jobs"
    url = f"{base_url}?seniorities={seniority}"
    if keyword:
        url += f"&keyword={keyword}"

    options = Options()
    # options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(url)
    time.sleep(10)  # 초기 로딩 대기

    scroll_to_bottom(driver, scroll_pause=1.5, max_scrolls=8)  # 충분히 스크롤

    job_cards = driver.find_elements(By.CSS_SELECTOR, 'div[class*="w_100%"][class*="d_flex"][class*="p_20px"]')

    jobs = []
    for card in job_cards:
        try:
            lines = card.text.split("\n")
            if len(lines) >= 3:
                company = lines[0].strip()
                title = lines[1].strip()
                description = lines[2].strip()
                if not is_valid_job(company, title):
                    continue
                else:
                    jobs.append({
                        "회사명": company,
                        "포지션": title,
                        "설명": description,
                        "링크": "coming soon..."
                    })
        except:
            continue

    driver.quit()
    return jobs


def save_to_csv(jobs, filename="rocket_jobs_selenium.csv"):
    df = pd.DataFrame(jobs)
    df.drop_duplicates(subset=["회사명", "포지션"], inplace=True)
    df.to_csv(filename, index=False, encoding="utf-8-sig")
    print(f"✅ 총 {len(df)}건 저장 완료 → {filename}")