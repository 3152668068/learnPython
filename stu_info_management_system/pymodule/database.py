import sqlite3, os, hashlib
import prettytable as pt

class database():
    def __init__(self):
        self.con = sqlite3.connect(os.path.join(os.getcwd(),'pymodule','info.db'))
        self.cursor = self.con.cursor()

    def create_table(self):
        # 创建学生信息表
        self.cursor.execute("""
            create table stu_info(
            sno TEXT PRIMARY KEY,  
            name TEXT NOT NULL,
            sex CHAR(1) NOT NULL,
            birth TEXT NOT NULL,
            enroll TEXT NOT NULL,
            class TEXT,
            tel TEXT,
            major TEXT,
            local TEXT,
            other TEXT
            );
        """)

        # 创建课程表
        self.cursor.execute("""
            create table course(
            cno TEXT PRIMARY KEY,
            cname TEXT NOT NULL,
            ctype TEXT NOT NULL,
            cpno TEXT,
            cother TEXT,
            FOREIGN KEY(cpno) REFERENCES course(cno)
            );
            """)

        # 创建学生成绩表
        self.cursor.execute("""
            create table stu_score(
            sno TEXT NOT NULL,
            cno TEXT NOT NULL,
            score REAL NOT NULL,
            FOREIGN KEY(cno) REFERENCES course(cno),
            FOREIGN KEY(sno) REFERENCES stu_info(sno)
            );
        """)

        # 创建系统用户表
        self.cursor.execute("""
                    create table system_user (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT,
                    passwd TEXT,
                    power INT
                    );
                """)


    def read(self,all,table_name,key=None,value=None):
        tb=pt.PrettyTable()
        if all:
            self.cursor.execute("select * from %s;" % table_name)
            values = self.cursor.fetchall()
            if len(values)==0:
                print("无数据！")
                return
            if table_name=='course':
                tb.field_names=['课程号','课程名','课程类型','先导课','备注信息']
                for v in values:
                    tb.add_row([v[0], v[1], v[2], v[3], v[4]])
                print(tb)

            if table_name=='stu_score':
                tb.field_names=['学号', '课程号', '成绩']
                for v in values:
                    tb.add_row([v[0], v[1], v[2]])
                print(tb)

            if table_name=='stu_info':
                tb.field_names=['学号', '姓名', '性别', '出生日期','入学时间','班级','联系电话','专业','户籍','其他']
                for v in values:
                    tb.add_row([v[0],v[1],v[2],v[3],v[4],v[5],v[6],v[7],v[8],v[9]])
                print(tb)

        else:
            self.cursor.execute("select * from {0:s} where {1:s}='{2:s}'".format(table_name, key, value))
            values=self.cursor.fetchall()

            if table_name=='stu_info':
                tb.field_names = ['学号', '姓名', '性别', '出生日期', '入学时间', '班级', '联系电话', '专业','户籍', '其他']
                for v in values:
                    tb.add_row([v[0], v[1], v[2], v[3], v[4], v[5], v[6], v[7], v[8], v[9]])
                print(tb)

            if table_name=='course':
                tb.field_names = ['课程号', '课程名','课程类型', '先导课','备注信息']
                for v in values:
                    tb.add_row([v[0], v[1], v[2], v[3], v[4]])
                print(tb)

            if table_name=='stu_score':
                tb.field_names = ['学号', '课程号', '成绩']
                for v in values:
                    tb.add_row([v[0], v[1], v[2]])
                print(tb)


    def insert(self,table_name,*value):
        if table_name=='course':
            sql = "INSERT INTO course VALUES('{0:s}','{1:s}','{2:s}','{3:s}','{4:s}')".format(value[0], value[1],value[2],value[3],value[4])
            self.cursor.execute(sql)

        if table_name=='stu_score':
            sql = "INSERT INTO stu_score VALUES('{0:s}','{1:s}',{2:s})".format(value[0], value[1],value[2])
            self.cursor.execute(sql)

        if table_name=='stu_info':
            sql = "INSERT INTO stu_info VALUES('{0:s}','{1:s}','{2:s}','{3:s}','{4:s}','{5:s}','{6:s}','{7:s}','{8:s}','{9:s}');".format(value[0], value[1], value[2], value[3], value[4], value[5], value[6], value[7], value[8],value[9])
            self.cursor.execute(sql)

    def update(self,table_name):
        if table_name == 'stu_info':
            pass
        if table_name == 'stu_score':
            pass
        if table_name == 'course':
            pass

    def delete(self,table_name):
        if table_name == 'stu_info':
            pass
        if table_name == 'stu_score':
            pass
        if table_name == 'course':
            pass

    def create_super_user(self):
        passwd=self.md5('root')
        self.cursor.execute("""
        insert into system_user
        values (1,'admin','%s',1)
        """ % passwd)

    def md5(self,content):
        md5 = hashlib.md5()
        md5.update(content.encode('utf-8'))
        return md5.hexdigest()

    def change_pwd(self,username,new_pwd):
        pwd_md5 = self.md5(new_pwd)
        sql="update system_user set passwd='%s' where name='%s';" % (pwd_md5,username)
        self.cursor.execute(sql)
        return "密码修改成功!\n"

    def login(self,username,passwd):
        self.cursor.execute("select passwd,power from system_user where name='%s'" % username)
        pwd=self.cursor.fetchall()
        if len(pwd)==0:
            return 0
        if pwd[0][0]==self.md5(passwd):
            return pwd[0][1]
        else:
            return 0

    def close(self):
        self.cursor.close()
        self.con.commit()
        self.con.close()



