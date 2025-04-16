"""cli에서 다음과 같이 입력하면 자동으로 패키지 다운, 설치가 됩니다.
   시간이 소요되니 커서가 뜰 때까지 기다려 주세요.
   pip install beautifulsoup4
   pip install matplotlib
"""
#내장 모듈
from urllib.request import *
import sys
import time
import re

#외부 모듈
from bs4 import *
import matplotlib.pyplot as p

def extractLastPrice ( webUrl, DN ) :  
    """인터넷에서 주어진 일 수만큼 최근의 일일 종가를 추출
       입력: webUrl (인터넷 주소), DN (추출할 일 수)
       출력: 일일 종가 리스트(가장 오래된 종가부터 최근까지 순서대로 저장)
    """
    
    pList = []  # 종가를 저장할 리스트
    page = 1    # 페이지 번호는 1부터 시작

    # DN개 이상의 종가를 모을 때까지 반복
    while len(pList) < DN:
        target_url = webUrl + str(page)
        req = Request(target_url, headers={'User-Agent': 'Mozilla/5.0'})
        html = urlopen(req)
        soup = BeautifulSoup(html, "html.parser")

        # summary 속성과 class를 이용하여 원하는 테이블 선택
        table = soup.find("table", attrs={
            "class": "type2",
            "summary": re.compile("외국인 기관 순매매")
        })

        if table is None:
            print("테이블을 찾을 수 없습니다. URL 또는 HTML 구조를 확인하세요.")
            break
        
        rows = table.find_all("tr")
        
        # 각 행에서 9개의 셀이 있는 경우(데이터 행)만 처리
        for row in rows:
            cells = row.find_all("td")
            if len(cells) == 9:
                # 두 번째 셀(td)에서 종가 데이터 추출 (예: <span class="tah p11">53,000</span>)
                price_text = cells[1].get_text(strip=True)
                if price_text and price_text != '-':  
                    # 천 단위 구분 쉼표 제거 후 숫자로 변환
                    try:
                        price = float(price_text.replace(',', ''))
                        pList.append(price)
                    except Exception as e:
                        print("가격 변환 에러:", e)
                # 원하는 개수만큼 모으면 종료
                if len(pList) >= DN:
                    break
        page += 1

    # 추출된 리스트는 최신순으로 모였으므로, 가장 오래된 값이 맨 앞에 오도록 뒤집는다.
    pList.reverse()  
    # print(pList, "size=", len(pList)) # 확인 완료 
    return pList

def computeRSI(pList, period=14):
    """종가 데이터를 바탕으로 RSI(Relative Strength Index)를 계산  
       입력: pList (종가 리스트), period (RSI 계산 기간, 기본 14)
       출력: RSI 리스트 (초기 period는 None 처리)
    """
    if len(pList) < period:
        print("RSI 계산을 위한 데이터가 부족합니다.")
        return [None] * len(pList)
    
    rsi = [None] * len(pList)
    # 가격 변화(델타) 계산: p[i] - p[i-1]
    deltas = [pList[i] - pList[i-1] for i in range(1, len(pList))]
    
    # 초기 기간의 평균 상승폭과 하락폭 계산
    avg_gain = sum(max(delta, 0) for delta in deltas[:period]) / period
    avg_loss = sum(-min(delta, 0) for delta in deltas[:period]) / period
    
    if avg_loss == 0:
        rsi[period] = 100
    else:
        rs = avg_gain / avg_loss
        rsi[period] = 100 - (100 / (1 + rs))
    
    # 그 이후 값들은 지수 이동평균 방식으로 업데이트
    for i in range(period + 1, len(pList)):
        delta = deltas[i - 1]
        gain = max(delta, 0)
        loss = -min(delta, 0)
        avg_gain = (avg_gain * (period - 1) + gain) / period
        avg_loss = (avg_loss * (period - 1) + loss) / period
        if avg_loss == 0:
            rsi[i] = 100
        else:
            rs = avg_gain / avg_loss
            rsi[i] = 100 - (100 / (1 + rs))
    return rsi

def makeMA(pList, numMA):
    """이동평균선 리스트를 만든다.
       입력: pList (주식 종가 리스트), numMA (평균 낼 기간)
       출력: mList (이동평균값 리스트, pList와 동일한 길이; 초반에는 None 값 포함)
    """
    mList = []
    # pList의 각 인덱스에 대해 numMA만큼의 구간 평균을 계산
    for i in range(len(pList)):
        if i < numMA - 1:
            # 데이터가 부족한 초기 구간은 None을 채워 넣어 pList와 길이를 맞춘다.
            mList.append(None)
        else:
            window = pList[i - numMA + 1: i + 1]
            avg = sum(window) / numMA
            mList.append(avg)
    # print(mList, "size=", len(mList))  # 확인 완료 
    return mList


def inputCompanyAndDays ():
    """회사, 회사의 web 주소, 추출할 종가의 기간을 선택
       입력: 없음
       출력: companyName (회사이름), webUrl (web 주소 시작 페이지), days (추출할 일 수)
    """

    #회사 선택
    print('1:Saltlux, 2:Hyundai Motors, 3:Hanwha Ocean')  #관심있는 다른 회사로 시도해 보세요.
    inputName = input('회사를 고르세요 : ')
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

    #추출할 종가의 날 수를 입력받는다.
    inputNumber = input ('종가 추출 기간을 입력하세요(20의 배수가 되도록 상향 조정합니다) : ')
    if (inputNumber.isdigit() and int(inputNumber) > 0) :
        days = int (inputNumber)
    else:
        print("잘못된 입력입니다. 프로그램을 종료합니다.")
        sys.exit()

    return companyName, webUrl, days

def drawGraph(pList, stockName, rsiList):
    """주식 일일 종가 및 이동평균선과 RSI를 하나의 Figure의 서브플롯으로 시각화  
       위쪽 서브플롯: 종가 및 5, 20, 60일 이동평균선  
       하단 서브플롯: RSI
    """

    days = len(pList)
    print("일수=", days)
    #그래프의 x값 list 생성
    xAxis = list(range(-days + 1, 1)) # 100개면 -99~0개까지 x축을 만든다.

    # 두 개의 서브플롯 생성 (위: 3배, 아래: 1배 높이)
    fig, (ax1, ax2) = p.subplots(2, 1, sharex=True, gridspec_kw={'height_ratios': [3, 1]})
    
    # 위쪽: 종가 및 이동평균선
    MA5List  = makeMA(pList, 5)
    MA20List = makeMA(pList, 20)
    MA60List = makeMA(pList, 60)
    ax1.plot(xAxis, pList, 'r', label=stockName)   # 종가
    ax1.plot(xAxis, MA5List,  'b', label='5MA')
    ax1.plot(xAxis, MA20List, 'g', label='20MA')
    ax1.plot(xAxis, MA60List, 'y', label='60MA')
    ax1.set_ylabel("Price")
    ax1.grid(True)
    ax1.legend(loc='upper left')
    
    # 아래쪽: RSI
    ax2.plot(xAxis, rsiList, 'm', label='RSI')
    # 보통 RSI에서 70 이상은 과매수, 30 이하은 과매도로 봄
    ax2.axhline(70, color='gray', linestyle='--', linewidth=1)
    ax2.axhline(30, color='gray', linestyle='--', linewidth=1)
    ax2.set_ylabel("RSI")
    ax2.set_xlabel("Day")
    ax2.grid(True)
    ax2.legend(loc='upper left')

     # 서브플롯 간 간격 조정 (예: 수평 간격 0.1)
    fig.subplots_adjust(hspace=0.01)
    
    p.show()

"""***메인 프로그램: 주식 종가 추출 및 그리기***"""

stockName, stockAddr, days = inputCompanyAndDays() # 회사 선택

startTime = time.time()            # 현재 시각 기록

pList = extractLastPrice(stockAddr, days) # 종가 추출

exeTime = time.time() - startTime  # 경과 시간 체크
print("\n추출 완료(소요 시간 = %.2f 초)" %exeTime)

# RSI 계산
rsiList = computeRSI(pList, period=14)

# 종가 및 이동평균선, RSI를 함께 시각화
drawGraph(pList, stockName, rsiList)

""" ***The End of Main*** """
