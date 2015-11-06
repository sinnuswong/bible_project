import threading,datetime,re,urllib.request
from bs4 import BeautifulSoup
crawler_threads = []
base_url = "http://bible.kyhs.me/lingxiu/"
list_url = base_url+"list.htm"


contents = urllib.request.urlopen(list_url).read().decode("gb2312")
pattern = '<a href="(.*)".*?>(.*)</a>'
res = re.findall(pattern,contents)
#print(res)
infos = []  #(name,eng_name,simple_eng_name,chapter_num)
crawler_threads = []
def grap_infos(res):
    for i in res:
        content_url = i[0]
        name = i[1]
        title_url = content_url.replace("content","title")
        url = base_url+title_url
        if name != "诗篇":
            contents = urllib.request.urlopen(url).read().decode('gb2312')
        else:
            contents = urllib.request.urlopen(url).read().decode('utf8')
        pattern = '<a href="O|NT.*"'
        res = re.findall(pattern,contents)
        chapter_num = len(res)

        temp = content_url.replace("_content.htm","").split('/')
        eng_name = temp[0] #OT06jos
        simple_eng_name = temp[1] #OT06joshua
        
        infos.append((name,eng_name,simple_eng_name,chapter_num))
        
def grap_chapter_notes(url):
    con = urllib.request.urlopen(url)
    contents = con.read().decode('utf8')
    soup = BeautifulSoup(contents,"html.parser")
    #s = soup.findAll('font',color="blue")
    #print(s[0])

    sp = '</font><font face="新细明体" size="2" color="blue">'

    res = contents.split(sp)

    sp1='</font><font face="新细明体" size="2">'

    notes = []
    for s in res[1:]:
        c = s.split(sp1)
        title = c[0].strip().replace("<br>","").replace("\u3000","").replace("\r\n","")
        content = c[1].strip().replace("<br>","").replace("\u3000","").replace("\r\n","").replace("</font></body></html>","")
        notes.append((title,content))
    return notes

def run(info): # run in a thread write in a file,is notes in a book
    eng_name = info[1]
    simple_eng_name = info[2]
    chapter_num = info[3]
    base_url = "http://www.godoor.com/book/library/html/bible/bible-lingxiu/LAB/"
    urls = []  # url for grap notes
    file_name = eng_name[2:4] #NT01,OT01,,,
    f = open(".\\note\\"+file_name,'w')
    if eng_name.startswith("NT"):
        file_name = str(int(file_name)+39)
    for i in range(chapter_num):
        url = base_url + "/"+ eng_name+"/Note/"+str(i+1)+"_"+simple_eng_name+".htm"
        urls.append(url)

    for url in urls:
        notes = grap_chapter_notes(url)  # indicate a chapter notes  [(title,content),(,),(,)]
        for note in notes:
            f.write(note[0]+"\n")
            f.write(note[1]+"\n")
            f.write("***\n")
        f.write("*****\n")
        f.flush
    f.close()
    
def main():
    grap_infos(res)
    for info in infos:
        t = threading.Thread(target=run,args=(info,))
        crawler_threads.append(t)
    for t in crawler_threads:
        t.start()
        t.join()
   
           
        
if __name__ == "__main__":
    main()
