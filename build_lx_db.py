import sqlite3
from db_util import util

class build:
    
    def __init__(self):
        self.db_name = 'lxb_bible.db'
        self.con = sqlite3.connect(self.db_name)
        self.cur = self.con.cursor()
        self.table_names = []
    def query_table_names(self):
        self.cur.execute("select name from sqlite_master where type='table' order by name;")
        res = self.cur.fetchall()
        for r in res:
            self.table_names.append(r[0])
        print(self.table_names)
    
    def show_table_info(self,name):
        self.cur.execute("PRAGMA table_info("+name+")")
        res = self.cur.fetchall()
        print("table "+name)
        for r in res:
            print(r)
        print()

    def create_tables(self):
        #create_lx_sql .....Id,Title,Content,BookId,ChapterId,NoteId
        create_lx_sql = "create table bible_lx(Id integer primary_key auto_increment,Title text not null,Content text not null,BookId integer,ChapterId integer,NoteId integer)"
        create_book_sql = "create table bible_book(Id integer primary_key auto_increment,Content text not null,BookId integer,ChapterId integer,SectionId integer)"
        create_info_sql = "create table bible_info(BookId integer primary_key,BookName text not null,BookShortName text not null,BookEnglishName text not null,ChapterNum integer)"
        self.cur.execute("drop table if exists bible_lx")
        self.cur.execute("drop table if exists bible_book")
        self.cur.execute("drop table if exists bible_info")
        self.con.commit()
        self.cur.execute(create_lx_sql)
        self.cur.execute(create_book_sql)
        self.cur.execute(create_info_sql)
        self.con.commit()
        
    def insert_info(self,book_id,book_name,book_short_name,book_english_name,chapter_num):
        sql = "insert into bible_info values(%d,'%s','%s','%s',%d)"%(book_id,book_name,book_short_name,book_english_name,chapter_num)
        self.cur.execute(sql)
    def insert_infos(self):
        u = util()
        infos = u.query_infos_for_db()
        for info in infos:
            self.insert_info(info[0],info[1],info[2],info[3],u.chapter_nums[info[0]-1])
        self.con.commit()
    def query_infos(self):
        sql = "select * from bible_info"
        self.cur.execute(sql)
        res = self.cur.fetchall()
        for r in res:
            print(r)
    def insert_lx(self,title,content,book_id,chapter_id,note_id):
        sql = "insert into bible_lx(Title,Content,BookId,ChapterId,NoteId) values('%s','%s',%d,%d,%d)"%(title,content,book_id,chapter_id,note_id)
        self.cur.execute(sql)
    def insert_lxs(self):
        u = util()
        for i in range(1,67):
            book_key = u.book_keys[i-1]
            chapter_num = u.chapter_nums[i-1]
            for chapter_id in range(1,chapter_num+1):
                notes = u.query_lx_for_db(book_key,chapter_id)
                for note in notes:
                    
                    self.insert_lx(note[0],note[1],i,chapter_id,note[2])
        self.con.commit()
    def query_lx(self,book_id,chapter_id,note_id):
        sql = "select Title,Content from bible_lx where BookId=%d and ChapterId=%d and NoteId=%d"%(book_id,chapter_id,note_id)
        self.cur.execute(sql)
        res = self.cur.fetchall()
        for r in res:
            print(r)
    def insert_book(self,content,book_id,chapter_id,section_id):
        sql = "insert into bible_book(Content,BookId,ChapterId,SectionId) values(\"%s\",%d,%d,%d)"%(content,book_id,chapter_id,section_id)
        self.cur.execute(sql)
    def insert_books(self):
        u = util()
        for i in range(1,67):
            book_key = u.book_keys[i-1]
            chapter_num = u.chapter_nums[i-1]
            for chapter_id in range(1,chapter_num+1):
                contents = u.query_book_for_db(book_key,chapter_id)
                for j in range(len(contents)):
                    self.insert_book(contents[j],i,chapter_id,j)
        self.con.commit()
    def query_book(self,book_id,chapter_id,section_id):
        sql = "select *from bible_book where BookId=%d and ChapterId=%d and SectionId=%d"%(book_id,chapter_id,section_id)
        self.cur.execute(sql)
        return self.cur.fetchone()
def test():
    b = build()
    #b.insert_infos()
    #b.insert_lxs()
    #b.insert_lxs()
    #b.query_lx(1,1,1)
    b.insert_books()
    print(b.query_book(1,1,1))
    print(b.query_book(1,1,2))
    print(b.query_book(1,1,3))
def main():
    pass
    
if __name__ == "__main__":
    test()
