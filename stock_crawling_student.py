"""cli에서 다음과 같이 입력하면 자동으로 패키지 다운, 설치가 됩니다.
   시간이 소요되니 커서가 뜰 때까지 기다려 주세요.
   pip install beautifulsoup4
   pip install matplotlib
"""
#내장 모듈
from urllib.request import *
import sys
import time

#외부 모듈
from bs4 import *
import matplotlib.pyplot as p

def extractLastPrice ( webUrl, DN ) :  
    """인터넷에서 주어진 일 수만큼 최근의 일일 종가를 추출
       입력: webUrl (인터넷 주소), DN (추출할 일 수)
       출력: 일일 종가 리스트(가장 오래된 종가부터 최근까지 순서대로 저장)
    """
    
    pass    #### 학생이 작성
    
    print (pList,"size=",len(pList))   # 결과 확인 용(확인 후 주석처리)
    return pList

def makeMA (pList, numMA) :  
    """이동평균선 리스트를 만든다
       입력: pList(주식 종가 리스트), numMA (평균 낼 종가 수)
       출력: mList (이동평균값 리스트)
    """

    pass   #### 학생이 작성

    print (mList,"size=",len(mList))   # 결과 확인 용(확인 후 주석처리)
    return mList


def inputCompanyAndDays ():
    """회사, 회사의 web 주소, 추출할 종가의 기간을 선택
       입력: 없음
       출력: companyName (회사이름), webUrl (web 주소 시작 페이지), days (추출할 일 수)
    """

    #회사 선택
    print ('1:samsung, 2:lge, 3:hynix')  #관심있는 다른 회사로 시도해 보세요.
    inputName = input ('회사를 고르세요 : ')   
    if (inputName == '1'):
        webUrl = 'http://finance.naver.com/item/frgn.nhn?code=005930&page='
        companyName = 'samsung'
    elif (inputName == '2'):
        webUrl = 'http://finance.naver.com/item/frgn.nhn?code=066570&page='
        companyName = 'lge'
    elif (inputName == '3'):
        webUrl = 'http://finance.naver.com/item/frgn.nhn?code=000660&page='
        companyName = 'hynix'
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

    
def drawGraph (pList):  
    """주식 일일종가, 5일, 20일, 60일 이동평균선을 그린다.
       입력: pList (주식 종가 리스트)
       출력: 그래프
    """

    days = len(pList)
    print("일수=", days)
    #그래프의 x값 list 생성
    xAxis = list(range(-days + 1, 1)) # 100개면 -99~0개까지 x축을 만든다.

    #이동평균선 생성
    MA5List  = makeMA (pList,  5)
    MA20List = makeMA (pList, 20)
    MA60List = makeMA (pList, 60)

    #종가와 이동평균선 그리기
    p.plot (xAxis, pList,    'r', label = stockName) #종가를 그린다.
    p.plot (xAxis, MA5List,  'b', label = '5MA')     # 5일 이동평균선
    p.plot (xAxis, MA20List, 'g', label = '20MA')    # 20일 이동평균선
    p.plot (xAxis, MA60List, 'y', label = '60MA')    # 60일 이동평균선

    #그래프의 레이블 및 비주얼 효과 생성
    p.xlabel ('Day')
    p.ylabel ('Last Price')
    p.grid (True)
    p.legend(loc = 'upper left')
    p.show()

    return


"""***메인 프로그램: 주식 종가 추출 및 그리기***"""

stockName, stockAddr, days = inputCompanyAndDays() # 회사 선택

startTime = time.time()            # 현재 시각 기록

pList = extractLastPrice(stockAddr, days) # 종가 추출

exeTime = time.time() - startTime  # 경과 시간 체크
print("\n추출 완료(소요 시간 = %.2f 초)" %exeTime)

drawGraph(pList) # 그리기

""" ***The End of Main*** """

