import threading,urllib.request,re,datetime

crawler_threads = []
base_url = "http://bible.kyhs.me/hhb/"
index = base_url+"index.htm"
con = urllib.request.urlopen(index) #bytes
content = con.read().decode('gbk')
pattern = '<P>(.*)</?P>'
book_names = re.findall(pattern,content)

book_names = list(map(lambda s:s.strip(),book_names))
print(book_names)

url_arrays = []

def grap_urls():
    pattern = "<A HREF='(.*)'>"
    res = re.findall(pattern,content)
    print(len(res))
    flag = "B01"
    temp = []
    for i in res:
        if i.startswith(flag):
            temp.append(i)
        else:
            url_arrays.append(temp)
            print(len(temp))
            flag = i[:3]
            temp = [i]
    url_arrays.append(temp)

def run(urls):#a book
    filename = urls[0][1:3]
    f = open(".\\bib\\"+filename,'w')
    bookname = book_names[int(filename)-1]
    f.write(bookname+",共"+str(len(urls))+"章\n")
    for url in urls:
        f.write(url[4:7]+"\n")
        chapter = grap_chapter(base_url+url)
        for s in chapter:
            f.write(s)
    f.flush()
    f.close()
def grap_chapter(url):
    con = urllib.request.urlopen(url)
    content = con.read().decode("gbk").strip()
    p = '</td><td>(.*)'
    res = re.findall(p,content)
    return res
        
def main():
    grap_urls()

    for urls in url_arrays:
        t = threading.Thread(target=run,args=(urls,))
        crawler_threads.append(t)
    for thread in crawler_threads:  #一次只运行于一个
        thread.start()
        thread.join()
    
if __name__ == '__main__':
    print(datetime.datetime.now())
    main()
    print(datetime.datetime.now())
