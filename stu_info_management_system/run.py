import getpass, sys, prettytable as pt, os, json
from pymodule import database

print("""
======================学生信息管理系统======================
1、登录
2、查询学生学籍信息
3、添加学生学籍信息
4、查询学生选课信息
5、添加学生选课信息
6、查询课程信息
7、添加课程信息
8、SQL高级查询
9、修改账号密码
10、退出程序
======================================================
""")

login_checked=0
login_name=""
db=database.database()

def init():
    global db
    all=os.listdir()
    if 'config.json' not in all:
        db.create_table()
        db.create_super_user()
        db.close()
        db=database.database()
        print("程序初始化成功，初始用户名:admin，密码:root")

        data={}
        data['学籍信息']={'sno':'学号','name':'名字','sex':'性别','birth':'出生日期','enroll':'入学时间','class':'班级','tel':'电话','major':'专业','other':'其他'}
        data['课程表']={'cno':'课程号','cname':'课程名','cpno':'先修课程号'}
        data['学生选课表']={'sno':'学号','cno':'课程号','score':'成绩'}

        with open('config.json','w') as f:
            json.dump(data,f)
    else:
        return


if __name__=='__main__':

    init()

    operation=0
    while operation!='10':
        if login_checked==0:
            operation=input("请输入操作序号: ")
        else:
            operation=input("请输入操作序号(用户: %s): " % login_name)
        if login_checked==0 and operation!='1':
            print("无权限，请先登录")
            continue
        if operation=='1':
            username=input("请输入用户名:")
            passwd=getpass.getpass("请输入密码:")
            login_time=3
            login_checked=db.login(username,passwd)
            if not login_checked:
                while login_time:
                    passwd = getpass.getpass("密码错误，请重试:")
                    login_checked = db.login(username, passwd)
                    if login_checked:
                        break
                    login_time-=1
                if login_checked:
                    print("登录成功")
                    login_name = username
                    continue
                print("错误次数过多，程序结束")
                sys.exit(0)
            else:
                print("登录成功")
                login_name=username
            continue

        if operation=='2':
            db.read(1,'stu_info')

        if operation=='3':
            sno = input("学号: ")
            name = input("姓名: ")
            sex = input("性别(M/F): ")
            birth = input("出生日期: ")
            enroll = input("入学时间: ")
            classment = input("班级: ")
            tel = input("联系电话: ")
            major = input("专业: ")
            local = input("户籍: ")
            other = input("备注: ")
            db.insert('stu_info',sno,name,sex,birth,enroll,classment,tel,major,local,other)

        if operation=='4':
            db.read(1,'stu_score')

        if operation=='5':
            sno=input("学号: ")
            cno=input("课程号: ")
            score=input("成绩: ")
            db.insert('stu_score',sno,cno,score)

        if operation=='6':
            db.read(1,'course')

        if operation=='7':
            cno = input("课程号: ")
            cname = input("课程名: ")
            ctype = input("课程类型: ")
            cpno = input("先导课程号: ")
            cother = input("备注信息: ")
            db.insert('course', cno, cname, ctype, cpno, cother)

        if operation=='8':
            print("输入exit退出")
            sql = input(">>")
            while sql!='exit':
                db.cursor.execute("%s" % sql)
                values = db.cursor.fetchall()
                result = []
                tb = pt.PrettyTable()
                for i in values:
                    tb.add_row(i)
                print(tb)
                sql = input(">>")

        if operation=='9':
            new_passwd=getpass.getpass("新密码: ")
            new_passwd_again = getpass.getpass("确认密码: ")
            if new_passwd!=new_passwd_again:
                print("两次密码不一致！")
                continue
            print(db.change_pwd(login_name,new_passwd))

    db.close()
    print("感谢使用本系统，程序结束！")