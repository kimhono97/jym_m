import requests
from bs4 import BeautifulSoup
from bible_index import getIndexName

def getIndex(s_idx):    # From. joyful-c.or.kr
    idx = []
    
    a = s_idx.find('(')
    s_idx = s_idx[a+1:]

    a = s_idx.find(' ')
    idx.append(s_idx[:a])
    s_idx = s_idx[a+1:]

    a = s_idx.find('장')
    idx.append(int(s_idx[:a]))
    s_idx = s_idx[a+1:]

    a = s_idx.find('절')
    idx.append(int(s_idx[:a]))
    s_idx = s_idx[a+1:]

    a = s_idx.find('~')
    s_idx = s_idx[a+1:]

    a = s_idx.find('장')
    idx.append(int(s_idx[:a]))
    s_idx = s_idx[a+1:]

    a = s_idx.find('절')
    idx.append(int(s_idx[:a]))
    s_idx = s_idx[a+1:]

    return idx

def getContext_1(ori):
    l = []
    b = 0

    ori = ori[1:]
    for i in ori:
        i = str(i)
        a = i.find('>')
        i = i[a+1:]
        a = i.find('<')
        if b%2 == 0:
            i = i[:a]
            tmp = i
        else:
            i = i[:a-2]
            l.append([tmp, i])
        b += 1
    
    return l

def getContext_2(ori):  # From. biblegateway.com
    l = []

    for i in ori:
        i = str(i)
        versenum = '<sup class="versenum">'
        a = i.find(versenum)
        if a == -1:
            versenum = '<span class="chapternum">'
            a = i.find(versenum)
            if a == -1:
                a = i.find(">")
                i = i[a+1:]
                a = i.find("<")
                i = i[:a]
                l[len(l)-1][1] += ("\n"+i)
                continue
        i = i[a+len(versenum):]
        a = i.find('<')
        if (len(l) == 0) and not ('-' in i[:a]):
            tmp = '1'
        else:
            tmp = i[:a].strip()
        a = i.find('>')
        i = i[a+1:]
        dul = '<span class="place double-underline">'
        b = i.find(dul)
        while b != -1:
            a = i[b+1:].find('<') + (b+1)
            i = i[:a] + i[a+7:]
            i = i[:b] + i[b+len(dul):]
            b = i.find(dul)
        pul = '<u class="person underline">'
        b = i.find(pul)
        while b != -1:
            a = i[b+1:].find('<') + (b+1)
            i = i[:a] + i[a+4:]
            i = i[:b] + i[b+len(pul):]
            b = i.find(pul)
        fnt = '<sup class="footnote"'
        b = i.find(fnt)
        while b != -1:
            a = i[b+1:].find('</sup>') + (b+1)
            i = i[:b] + i[a+6:]
            b = i.find(fnt)
        a = i.find('<')
        i = i[:a]
        l.append([tmp+'.  ', i])
    
    return l
        
def makeFullTxt(idx, txt):
    full = ""
    full = full+idx[0]+"\t"
    full = full+str(idx[1])+":"+str(idx[2])
    full = full+" ~ "+str(idx[3])+':'+str(idx[4])+'\n\n'
    for i in txt:
        full = full+i[0]+i[1]+"\n"

    return full

def cutTxt(idx, txt):
    for a in range(len(txt)):
        i = txt[a]
        if '-' in i[0]:
            flag = False
            x = []
            y = i[0].find('-')
            x.append(int(i[0][:y]))
            z = i[0].find('.')
            x.append(int(i[0][y+1:z]))
            for j in x:
                if j == idx[2]:
                    flag =True
                    break
            if flag:
                break
        elif int(i[0][:len(i[0])-3]) == idx[2]:
            break
    for b in range(len(txt)):
        i = txt[b]
        if '-' in i[0]:
            flag = False
            x = []
            y = i[0].find('-')
            x.append(int(i[0][:y]))
            z = i[0].find('.')
            x.append(int(i[0][y+1:z]))
            for j in x:
                if j == idx[4]:
                    flag =True
                    break
            if flag:
                break
        elif int(i[0][:len(i[0])-3]) == idx[4]:
            break
    
    return txt[a:b+1]

def getQT(lang, date):
    idx = []
    txt = []
    
    url = 'http://www.joyful-c.or.kr/index.php?r=home&mod=qt_index&date=' + date
    source_code = requests.get(url, allow_redirects=False)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, 'html.parser')
    s_kr = soup.findAll('div', {'id': 'view_bible'})[0]
    kr = s_kr.findAll('td')
    idx = getIndex(str(kr[0]))
    idx[0] = getIndexName(idx[0], lang)
        
    if lang == 'kr':
        txt = getContext_1(kr)
        
    elif lang == 'en':
        s_en = soup.findAll('div', {'id': 'view_bible1'})[0]
        en = s_en.findAll('td')
        txt = getContext_1(en)
    elif lang == 'jp':
        pre = 'https://www.biblegateway.com/passage/?search='
        post = '&version=JLB'
        url = pre + idx[0] + str(idx[1]) + post
        source_code = requests.get(url, allow_redirects=False)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text, 'html.parser')
        s_jp = soup.findAll('div', {'class' : 'version-JLB result-text-style-normal text-html '})[0]
        s_jp = s_jp.findAll('p')
        jp = []
        for i in s_jp:
            jp = jp + i.findAll('span', {'class': 'text'})
        txt = getContext_2(jp)
        txt = cutTxt(idx, txt)
    elif lang == 'cn':
        pre = 'https://www.biblegateway.com/passage/?search='
        post = '&version=CUVMPT'
        url = pre + idx[0] + str(idx[1]) + post
        source_code = requests.get(url, allow_redirects=False)
        plain_text = source_code.text
        soup = BeautifulSoup(plain_text, 'html.parser')
        s_cn = soup.findAll('div', {'class' : 'version-CUVMPT result-text-style-normal text-html '})[0]
        s_cn = s_cn.findAll('p')
        cn = []
        for i in s_cn:
            cn = cn + i.findAll('span', {'class': 'text'})
        txt = getContext_2(cn)
        txt = cutTxt(idx, txt)
    full = makeFullTxt(idx, txt)
    
    return {'idx':idx, 'txt':txt, 'full':full, 'lang':lang}

if __name__ == "__main__":
    qt = getQT('kr', "2018-02-02")
    print(qt['idx'])
    for i in qt['txt']:
        print(">--", i[0], i[1], "<--")
    print()
    print(qt['full'])
