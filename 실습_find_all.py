from urllib.request import *
from bs4 import *  # import Beautiful Soup

html = """
<!doctype html>
<head><title>An Example</title></head>
<body>
   <h3>The second heading(small font).</h3>
   <p>A paragraph(number list):
     <b style="color:red;">123</b>, <b style="color:red;">356</b>,
     <b>641</b>, <b>387</b> </p>
   <p>Hyperlink: <a href="http://www.google.com">google</a></p>
   <p>Link with italic: <a href="http://www.naver.com"><i>naver</i></a></p>
</body>
"""

soup = BeautifulSoup(html, 'html.parser') # parsing

### 태그가 b인 object 리스트 추출
print("## 태그가 b인 object 리스트 추출 ##")
bList = soup.find_all('b')  
print(bList)

print("\n # bList에서 정수 값 추출")
for b in bList :
  print(b.get_text()) # 123 356 641 387 차례로 출력

### 태그가 b이고 속성이 style="color:red;"인 object 추출
print("\n## 태그가 b이고 속성이 style='color:red;'인 object 리스트 추출 ##")
bList = soup.find_all('b', {'style':'color:red;'})
print(bList)        # 추출한 리스트 출력(아래 참조)

print("\n # bList에서 두 번째 원소 값")
print(bList[1].get_text()) # 356 (bList의 두번째)
print ('----------')
print (type(soup))
print (bList)
print (type(bList))
print (bList[1])
print (type(bList[1]))
print ('----------')
###두 단계에 걸친 추출
print("\n## 두 단계에 걸친 추출 ##")

print("\n # 태그가 p인 object 리스트 추출(pList)")
pList = soup.find_all('p') # 태그가 p인 object 리스트
print(pList)

 # pList[0]에 태그가 b인 object들이 있다.
print("\n # pList에서[0]에서 태그가 b인 object 리스트 추출(bList)")
bList = pList[0].find_all('b') # 태그가 b인 리스트
print(bList)

print("\n # bList에서 추출한 정수 값들")
for b in bList :
  print(b.get_text()) # 123 356 641 387 차례로 출력
