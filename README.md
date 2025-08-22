# Rocketpunch Job Crawler 🧲

Rocketpunch에서 초급 개발자/데이터 관련 채용공고를 키워드 기반으로 자동 크롤링하는 Python 프로젝트입니다.

## 주요 기능
- Selenium 기반 동적 웹 크롤링
- 키워드/경력 레벨 필터링
- 공고 텍스트 및 링크 저장
- 중복 제거 후 CSV 저장

## 사용 방법
```bash
pip install -r requirements.txt
python crawl.py

---

### ✅ 5단계: GitHub에 새 저장소 만들기
1. [github.com](https://github.com) 접속
2. 오른쪽 상단 **+** → `New repository` 클릭
3. 저장소 이름 예: `rocketpunch-crawler`
4. `Create repository` 클릭

---

### ✅ 6단계: GitHub 연결 및 푸시

```bash
git add .
git commit -m "Initial commit 🚀"
git remote add origin https://github.com/your-username/rocketpunch-crawler.git
git branch -M main
git push -u origin main
