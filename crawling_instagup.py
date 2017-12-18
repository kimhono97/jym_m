import requests
from bs4 import BeautifulSoup
import sys

def get_img(soup):
    lst = []
    div = soup.findAll('div', {'class': 'post-masonry-media loading'})

    for x in div:
        x = str(x)
        a = x.find('src="https')
        x = x[a+5:]
        a = x.find('"')
        img = x[:a]
        a = x.find('-time">')
        x = x[a+7:]
        a = x.find('</span>')
        day = x[:a]
        lst.append([img, day])

    return lst

def get_stat(soup):
    lst = []
    div = soup.findAll('div', {'class': 'post-masonry-stats'})
    
    for x in div:
        x = str(x)
        a = x.find('count">')
        x = x[a+7:]
        a = x.find('</span>')
        likes = x[:a]
        a = x.find('count">')
        x = x[a+7:]
        a = x.find('</span>')
        comments = x[:a]
        lst.append([likes, comments])

    return lst

def get_context(soup):
    lst = []
    p = soup.findAll('p', {'class': 'post-masonry-caption'})
#    print(len(p))
#    non_bmp_map = dict.fromkeys(range(0x10000, sys.maxunicode + 1), 0xfffd)
    
    for x in p:
        x = str(x)
        a = x.find('>')
        x = x[a+1:]

        a = x.find('<a href="/tag/')
        while a != -1 :
            b = x[a:].find('#') + a
#            print(a, b, x[a:b].translate(non_bmp_map))
            x = x[:a] + x[b:]
            c = x.find('</a>')
#            print(c, c+4, x[c:c+4].translate(non_bmp_map))
            x = x[:c] + x[c+4:]
            a = x.find('<a href="/tag/')

        a = x.find('&amp;')
        while a != -1:
            x = x[:a+1] + x[a+5:]
            a = x.find('&amp;')

        a = x.find('<')
        while a != -1:
            b = x[a+1:].find('>')
            x = x[:a] + x[a+b+2:]
            a = x.find('<')
        
        lst.append(x)

    return lst

def get_url(soup):
    lst = []
    a = soup.findAll('a', {'class': 'post-masonry-link'})

    for x in a:
        x = str(x)
        b = x.find('href=')
        x = x[b+6:]
        b = x.find('title=')
        x = x[:b-2]
#        print("http://www.instagup.com" + x)
        lst.append("http://www.instagup.com" + x)

    return lst

def get_instagup():
    lst = []
    url = 'http://www.instagup.com/profile/jym_joyfulyouthmission'
    source_code = requests.get(url, allow_redirects=False)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, 'html.parser')

    imgs = get_img(soup)

    stats = get_stat(soup)

    txt = get_context(soup)

    url = get_url(soup)

#    print(len(txt))

    for i in range(len(imgs)):
        dic = {}
        dic['img'] = imgs[i][0]
        dic['day'] = imgs[i][1]
        dic['likes'] = stats[i][0]
        dic['comments'] = stats[i][1]
        dic['txt'] = txt[i]
        dic['url'] = url[i]
        lst.append(dic)
    
    return lst

if __name__ == "__main__":
    get_instagup()
