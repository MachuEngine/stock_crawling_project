from urllib.request import *
from bs4 import *  # import Beautiful Soup

wp = urlopen('http://mail.sogang.ac.kr')

soup = BeautifulSoup(wp, 'html.parser') # parsing
print(type(soup))  # <class 'bs4.BeautifulSoup'>
print(soup.prettify()) # HTML 코드 출력