from crawler.rocketpunch import crawl_rocketpunch_selenium

def crawl_jobs(keyword: str = None, seniority: str = "BEGINNER"):
    # Selenium 기반 크롤링 함수 호출
    return crawl_rocketpunch_selenium(keyword, seniority)