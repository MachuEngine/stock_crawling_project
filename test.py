from urllib.request import Request, urlopen
from bs4 import BeautifulSoup

# 네이버는 기본 Python user-agent를 차단할 가능성이 있으므로, 헤더를 추가합니다.
url = "https://finance.naver.com/item/frgn.nhn?code=005930&page=1"
req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
html = urlopen(req)
soup = BeautifulSoup(html, "html.parser")

# 페이지 내 모든 테이블 출력
tables = soup.find_all("table", class_="type2")
for idx, table in enumerate(tables, start=1):
    tbl_summary = table.get("summary")
    print(f"Table {idx} summary: {tbl_summary}")
