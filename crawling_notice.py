import requests
from bs4 import BeautifulSoup

def getElem(line):
    rtn = {}
    
    a = line.find('href=')
    line = line[a+6:]
    a = line.find('>')
    
    y = line[:a-1]
    x = y.find('uid')
    rtn['href'] = y[x:]
    
    line = line[a+1:]
    a = line.find('<')
    rtn['title'] = line[:a]
    a = line.find(';">')
    line = line[a+3:]
    a = line.find('<')
    rtn['user'] = line[:a]
    a = line.find('hit b')
    line = line[a+7:]
    a = line.find('<')
    rtn['visit'] = int(line[:a])
    a = line.find('<td>')
    line = line[a+4:]
    a = line.find('<')
    rtn['date'] = line[:a]

    return rtn
    

def getNotice(limit):
    url = 'http://jym.or.kr/?r=home&c=5'
    source_code = requests.get(url, allow_redirects=False)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, 'html.parser')

    table = soup.findAll('div', {'id': 'bbslist'})[0]
    
    lst = table.findAll('tr')[1:]
    if len(lst)>limit:
        lst = lst[:limit]
    l = []
    for i in lst:
        l.append(getElem(str(i)))

    return l

if __name__ == "__main__":
    l = getNotice(5)
    for i in l:
        print(i)
    
