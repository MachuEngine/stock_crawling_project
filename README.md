# stock_crawling_project
웹크롤링 개인 프로젝트

### 개요
네이버 금융 정보 주식 페이지를 웹크롤링하여 국내 상장 주식의 일일 종가 그래프를 시각화합니다.

---

### 코드
회사를 입력 받아 url을 설정하고, 기간을 설정 받습니다. 
```py
...
def inputCompanyAndDays ():
    """회사, 회사의 web 주소, 추출할 종가의 기간을 선택
       입력: 없음
       출력: companyName (회사이름), webUrl (web 주소 시작 페이지), days (추출할 일 수)
    """
    if (inputName == '1'):
            webUrl = 'https://finance.naver.com/item/frgn.naver?code=304100&page='
            companyName = 'Saltlux'
        elif (inputName == '2'):
            webUrl = 'https://finance.naver.com/item/frgn.naver?code=005380&page='
            companyName = 'Hyundai Motors'
        elif (inputName == '3'):
            webUrl = 'https://finance.naver.com/item/frgn.naver?code=042660&page='
            companyName = 'Hanwha Ocean'
        else:
            print("잘못된 입력입니다. 프로그램을 종료합니다.")
            sys.exit()
...
```

```py
...
#추출할 종가의 날 수를 입력받는다.
    inputNumber = input ('종가 추출 기간을 입력하세요(20의 배수가 되도록 상향 조정합니다) : ')
    if (inputNumber.isdigit() and int(inputNumber) > 0) :
        days = int (inputNumber)
    else:
        print("잘못된 입력입니다. 프로그램을 종료합니다.")
        sys.exit()
...
```

실제로 web에서 데이터를 가져오는 부분입니다. 
```py
def extractLastPrice ( webUrl, DN ) :  
    """인터넷에서 주어진 일 수만큼 최근의 일일 종가를 추출
       입력: webUrl (인터넷 주소), DN (추출할 일 수)
       출력: 일일 종가 리스트(가장 오래된 종가부터 최근까지 순서대로 저장)
    """
```

그래프를 그리는 함수입니다. 
```py
def drawGraph(pList, stockName, rsiList):
    """주식 일일 종가 및 이동평균선과 RSI를 하나의 Figure의 서브플롯으로 시각화  
       위쪽 서브플롯: 종가 및 5, 20, 60일 이동평균선  
       하단 서브플롯: RSI
    """
```

부가적으로 일일 종가 데이터를 활용하여 RSI 지표와 이동평균선을 추가하여 보조지표를 표시하도록 하였습니다.

---

### 결과 시각화
<img width="622" height="565" alt="image" src="https://github.com/user-attachments/assets/8eca5485-7d97-45a6-975b-f9bea2391c72" />
