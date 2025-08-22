import csv
import os
from datetime import datetime

def append_email_log(email, result, keyword, seniority):
    log_dir = "log"
    log_file = os.path.join(log_dir, "email_log.csv")

    # 로그 헤더
    fieldnames = ["이메일", "결과", "시각", "키워드", "숙련도"]

    # 현재 시각
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # 로그 내용
    log_data = {
        "이메일": email,
        "결과": result,
        "시각": now,
        "키워드": keyword,
        "숙련도": seniority
    }

    # 파일 없으면 헤더도 추가
    write_header = not os.path.exists(log_file)

    with open(log_file, "a", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        if write_header:
            writer.writeheader()
        writer.writerow(log_data)