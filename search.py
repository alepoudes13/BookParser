from bs4 import BeautifulSoup
import urllib.request, requests

alf = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщъыьэюя"

url_alf = "%C0%C1%C2%C3%C4%C5%A8%C6%C7%C8%C9%CA%CB%CC%CD%CE%CF%D0%D1%D2%D3%D4%D5%D6%D7%D8%D9%DA%DB%DA%DD%DE%DF%E0%E1%E2%E3%E4%E5%B8%E6%E7%E8%E9%EA%EB%EC%ED%EE%EF%F0%F1%F2%F3%F4%F5%F6%F7%F8%F9%FA%FB%FC%FD%FE%FF"
url_alf = url_alf.split('%')[1:]

def encode(str):
    req = ""
    for i in str:
        if i == ' ':
            req += '+'
        elif not i in alf:
            req += i
        else:
            for j in range(len(alf)):
                if alf[j] == i:
                    req += '%' + url_alf[j]
                    break
    return req

def print_list(lst):
    print("====================================")
    print("Book list: ")
    if lst == []:
        return
    for book in lst:
        print(book[1] + " ||| " + book[2])
    print("====================================")

def authors_search(au):
    req = 'http://loveread.ec/' + au[0]
    html_doc = urllib.request.urlopen(req).read()
    soup = BeautifulSoup(html_doc, 'html.parser')
    uls = soup.findAll('ul', 'sr_book')

    lst = []

    for ul1 in uls:
        l = ul1.find('li')
        liss1 = [l]
        liss1 += l.find_next_siblings('li')
        for lis1 in liss1:
            sp = lis1.find('span')
            a = sp.find('a')

            serie = []
            if a == None:
                serie.append([-1, "Вне серий"])
            else:
                serie.append([a['href'].split('=')[-1], str(a.string)])
            books = []
            lis2 = lis1.find('ul').findAll('li')
            for li in lis2:
                ass = li.findAll('a')
                for aa in ass:
                    forb = ['\t', '\r', '\n', '\xa0']
                    a_name = ""
                    for ch in str(aa.string):
                        if not ch in forb:
                            a_name += ch
                    a_temp = a_name.split()
                    if a != None and '.' in a_temp[0] and len(a_temp[0]) < 4:                    
                        a_name = ' '.join(a_temp[1:])
                    books.append([aa['href'].split('=')[-1], a_name])

            serie.append(books)
            lst.append(serie)

    print("Книги автора: ")

    i = 1
    series_ind = []

    for serie in lst:
        if serie[0][0] == -1:
            print("/----Вне серий: ")
        else:
            print(str(i) + ') /----' + serie[0][1])
            i += 1
        for book in serie[1]:
            print(str(i) + ') ' + book[1])
            i += 1

    added = []

    while True:
        try:
            ans = int(input('Type the number you need("-1" to return): '))
        except:
            print("/----Invalid input")
            continue

        if ans == -1:
            break
        ans -= 1
        ind = 0
        try:
            for serie in lst:
                if serie[0][0] == -1:
                    pass
                else:
                    if ind == ans:
                        for book in serie[1]:
                            added.append([book[0], book[1], au[1]])
                        raise NameError
                    ind += 1

                for book in serie[1]:
                    if ind == ans:
                        added.append([book[0], book[1], au[1]])
                        raise NameError
                    ind += 1
        except:
            pass
        else:
            print("/---Incorrect number, type again")

    return added



def series_search(s):
    req = 'http://loveread.ec/' + s[0]
    html_doc = urllib.request.urlopen(req).read()
    soup = BeautifulSoup(html_doc, 'html.parser')

    added = []
    au = None

    books = []

    td = soup.find('td', 'letter_nav_bg')
    tbls = td.findAll('table')

    au_table = tbls[-1]
    try:
        au = str(au_table.find('h2').string)
    except:
        au = ''
    
    ass = tbls[0].findAll('a')
    for a in ass:
        st = a.find('strong')
        if not st == None:
            books.append([a['href'].split('=')[-1], str(st.string)])

    print("1) /----Серия " + s[1] + ": ")
    i = 2
    for book in books:
        print(str(i) + ') ' + book[1] + ' ||| ' + au)
        i += 1

    while True:
        try:
            ans = int(input('Type the number you need("-1" to return): '))
        except:
            print("/----Invalid input")
            continue

        if ans == -1:
            break
        if ans == 1:
            for book in books:
                added.append([book[0], book[1], au])
        else:
            ans -=2
            if ans < 0 or ans >= len(books):
                print("/---Incorrect number, type again")
            else:
                added.append([books[ans][0], books[ans][1], au])
                
    return added

def search():
    ids, nm = [], []
    lst = []

    while(True):
        inp = input('Type your request("-1" to end searching): ')
        if inp == "-1":
            return [ids, nm]
        req = encode(inp)
        url = 'http://loveread.ec/search.php?search=' + req

        html_doc = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(html_doc, 'html.parser')

        uls = soup.findAll('ul', 'let_ul')
        if uls == []:
            print("/----Nothing found, please try again")
            continue


        books = []
        authors = []
        series = []

        for ul in uls:
            name_div = ul.find('div', 'contents')
            name_div = name_div.string

            if "книг" in name_div:
                ass = ul.findAll('a')
                i = 0
                while i < (len(ass) - 1):
                    bk = ass[i]
                    name = ' '.join(bk['title'].split(' ')[1:-4])

                    au = ass[i + 1]

                    id = bk['href'].split('=')[-1]

                    books.append([id, name, au.string])

                    i += 2
            elif "автор" in name_div:
                ass = ul.findAll('a')
                for au in ass:
                    href = au['href']
                    name = ' '.join(au['title'].split(' ')[:-3])
                    authors.append([href, name])
            elif "серии" in name_div:
                ass = ul.findAll('a')
                for s in ass:
                    href = s['href']
                    name = s['title']
                    series.append([href, name])

        i = 0
        if len(books) > 0:
            print("/----Найденные книги: ")
            for bk in books:
                print(str(i + 1) + ') ' + bk[1] + ' ||| ' + bk[2])
                i += 1
        if len(authors) > 0:
            print("/----Найденные авторы: ")
            for au in authors:
                print(str(i + 1) + ') ' + au[1])
                i += 1
        if len(series) > 0:
            print("/----Найденные серии: ")
            for s in series:
                print(str(i + 1) + ') ' + s[1])
                i += 1

        while True:
            try:
                ans = int(input('Type the number you need("-1" to change search request, "-2" to end searching): '))
            except:
                print("/----Invalid input")
                continue

            if ans == -1:
                break
            elif ans == -2:
                return [ids, nm]
            if ans <= len(books) and len(books) > 0:
                lst.append(books[ans - 1])
                ids.append(books[ans - 1][0])
                nm.append(books[ans - 1][1])
            elif ans <= len(books) + len(authors) and len(authors) > 0:
                added = authors_search(authors[ans - len(books) - 1])
                lst += added
                for bkk in added:
                    ids.append(bkk[0])
                    nm.append(bkk[1])
                break
            elif ans <= len(books) + len(authors) + len(series) and len(series) > 0:
                added = series_search(series[ans - len(books) - len(authors) - 1])
                lst += added
                for bkk in added:
                    ids.append(bkk[0])
                    nm.append(bkk[1])
                break
            else:
                print("/---Incorrect number, type again")

        print_list(lst)

if __name__ == "__main__":
    search()
