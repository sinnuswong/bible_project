import sqlite3

class util:
    def __init__(self):
        self.d_name = "biblelxb.db"
        self.conn = sqlite3.connect(self.d_name)
        self.cu = self.conn.cursor()
        self.table_names = []
        self.chapter_nums = [50, 40, 27, 36, 34, 24, 21, 4, 31, 24, 22, 25, 29, 36, 10, 13, 10, 42, 150, 31, 12, 8, 66, 52, 5, 48, 12, 14, 3, 9, 1, 4, 7, 3, 3, 3, 2, 14, 4, 28, 16, 24, 21, 28, 16, 16, 13, 6, 6, 4, 4, 5, 3, 6, 4, 3, 1, 13, 5, 5, 3, 5, 1, 1, 1, 22]
        self.book_keys = []
        self.book_names = []
        self.query_table_names()

        for name in self.table_names:
            self.show_table_info(name)
            
        self.query_book_names_and_keys()
        
    def query_table_names(self):
        self.cu.execute("select name from sqlite_master where type='table' order by name;")
        res = self.cu.fetchall()
        for r in res:
            self.table_names.append(r[0])
        print(self.table_names)
    def show_table_info(self,name):
        self.cu.execute("PRAGMA table_info("+name+")")
        res = self.cu.fetchall()
        print(name)
        for r in res:
            print(r)
        print()
    def query_book_names_and_keys(self):
        for i in range(1,67):
            self.cu.execute("select BookName,BookKey from Content where Id=%d"%i)
            res = self.cu.fetchone()
            print(res)
            self.book_names.append(res[0])
            self.book_keys.append(res[1])
    def query_infos_for_db(self):  #select select Id,BookName,BookShortName,BookNameEn from Content
        self.cu.execute("select Id,BookName,BookShortName,BookNameEn from Content")
        res = self.cu.fetchall()
        for r in res:
            print(r)
        return res    
    def query_lx_for_file(self,book_key,chapter_id): #select Title,Content from ZH_CN_LinXiu
        sql = "select Title,Content from ZH_CN_LinXiu where BookKey='%s' and Chapter=%d"%(book_key,chapter_id)
        self.cu.execute(sql)
        res = self.cu.fetchall()
        return res

    def query_lx_for_db(self,book_key,chapter_id):
        sql = "select Title,Content,NoteOrder from ZH_CN_LinXiu where BookKey='%s' and Chapter=%d"%(book_key,chapter_id)
        self.cu.execute(sql)
        res = self.cu.fetchall()
        return res
    
    def query_book_for_file(self,book_key,chapter_id): #query a chapter,return a list of sections
        sql = "select Content from ZH_CN_Book where BookKey='%s' and Chapter=%d"%(book_key,chapter_id)
        self.cu.execute(sql)
        res = self.cu.fetchall()
        ress = []
        for r in res:
            ress.append(r[0])
        return ress
    def query_book_for_db(self,book_key,chapter_id):
        return self.query_book_for_file(book_key,chapter_id)
            
    def save_book_to_file(self,id): #id 1-66
        book_key = self.book_keys[id-1]
        book_name = self.book_names[id-1]
        file_name = str(id)
        if id < 10:
            file_name = '0'+file_name
        chapter_num = self.chapter_nums[id-1]
        f = open(".\\bible\\"+file_name,'w',encoding='utf8')
        f.write(book_name+",共"+str(chapter_num)+"章\n")
        for chapter_id in range(1,chapter_num+1):
            sp = str(chapter_id)
            if chapter_id<10:
                sp = "00"+sp
            elif chapter_id <100:
                sp = "0"+sp
            f.write(sp+"\n")
            chapter = self.query_book_for_file(book_key,chapter_id) #a list of sections
            
            for s in chapter:
                f.write(s.strip().replace("\r\n","").replace("\r","").replace("\n","")+"\n")
        f.flush()
        f.close()

    def save_books_to_file(self):
        for i in range(1,67):
            self.save_book_to_file(i)

    def save_lx_to_file(self,id): # id 1-66
        book_key = self.book_keys[id-1]
        file_name = str(id)
        if id < 10:
            file_name = '0'+file_name
        chapter_num = self.chapter_nums[id-1]
        f = open(".\\note\\lx"+file_name,'w',encoding='utf8')

        for chapter_id in range(1,chapter_num+1):
            notes = self.query_lx_for_file(book_key,chapter_id)
            for note in notes:
                f.write(note[0].strip().replace("\r\n","").replace("\r","").replace("\n",""))
                f.write("###")
                f.write(note[1].strip().replace("\r\n","").replace("\r","").replace("\n","")+"\n")
            f.write("#####\n")
        f.flush()
        f.close()
        
def main():
    u = util()
    #u.query_infos()
    for i in range(1,67):
        u.save_lx_to_file(i)
if __name__ == "__main__":
    main()
    
