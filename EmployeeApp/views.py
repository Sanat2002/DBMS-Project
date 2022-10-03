from typing import Tuple
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.db import connection
from django.contrib import messages

isadminlogin = False
isaemplogin = False
user = ()

def login(request):
    global isadminlogin,isaemplogin,user
    notfound = True
    cursor = connection.cursor()
    if request.method == "POST":
        email = request.POST.get("email")
        password = request.POST.get("password")
        type = request.POST.get("emptype")
        print(type)

        if type == "admin":
            cursor.execute(''' select * from alogin ''')
            rows = cursor.fetchall()
            for row in rows:
                if row[1] == email and row[2] == password:
                    cursor.execute(f''' insert into user(id,isadmin) values({row[0]},TRUE) ''')
                    isadminlogin = True
                    user = row
                    return HttpResponseRedirect("/home")
                elif row[1] == email and row[2] != password:
                    notfound = False
                    messages.error(request,"Incorrect Password!!!")
                    break
        else:
            cursor.execute(''' select * from employee ''')
            rows = cursor.fetchall()
            for row in rows:
                if row[1] == email and row[2] == password:
                    cursor.execute(f''' insert into user(id,isadmin) values({row[0]},FALSE) ''')
                    isaemplogin = True
                    user = row
                    return HttpResponseRedirect("/home")
                elif row[1] == email and row[2] != password:
                    notfound = False
                    messages.error(request,"Incorrect Password!!!")
                    break

        if notfound:
            messages.error(request,"Employee or Admin not found!!!")
    return render(request,"login.html")


def home(request):
    cursor = connection.cursor()
    cursor.execute(''' select * from user ''')
    user = cursor.fetchall()

    if user[0][1]:
        toextendfile = "base1.html"
    else:
        toextendfile = "base2.html"
    
    cursor.execute(''' select id,firstName,points from employee, rankk where employee.id = rankk.eid order by rankk.points desc''')
    # cursor.execute(''' select firstName,points from employee natural join rankk''') # returning dual result
    leaderboard = cursor.fetchall()

    cursor.execute(f''' select pname,duedate from project where project.eid = {user[0][0]} ''')
    durprojects = cursor.fetchall()

    cursor.execute(f''' select base,bonus,total from salary where salary.eid = {user[0][0]} ''')
    salary = cursor.fetchall()
    
    cursor.execute(f''' select start,end,reason,status from employee_leave where employee_leave.id = {user[0][0]} ''')
    leaves = cursor.fetchall()
    print(leaderboard)

    return render(request,"home.html",{"base":toextendfile,"admin":user[0][1],"leaderboard":leaderboard,"dueprojects":durprojects,"salary":salary,"leaves":leaves})


def addemployee(request):
    cursor = connection.cursor()
    empexist = False
    if request.method == "POST":
        fname = request.POST.get("firstName")
        lname = request.POST.get("lastName")
        email = request.POST.get("email")
        birthday = request.POST.get("birthday")
        gender = request.POST.get("gender")
        contact = request.POST.get("contact")
        nid = request.POST.get("nid")
        address = request.POST.get("address")
        dept = request.POST.get("dept")
        degree = request.POST.get("degree")
        salary = request.POST.get("salary")
        picurl = request.POST.get("picurl")

        cursor.execute(''' select email from employee ''')
        emails = cursor.fetchall()

        for e in emails:
            if e[0] == email:
                empexist = True
                messages.error(request,"Employee already exist!!!")
        
        if not empexist:
            command = '''insert into employee(firstName,lastName,email,password,birthday,gender,contact,nid,address,dept,degree,pic) values(%s,%s,%s,"1234",%s,%s,%s,%s,%s,%s,%s,%s)'''
            params = (fname,lname,email,birthday,gender,contact,nid,address,dept,degree,picurl)
            cursor.execute(command,params)
            cursor.execute(f''' select id from employee where employee.email = {email} ''')
            emp = cursor.fetchall()
            cursor.execute(f''' insert into rankk(eid,points) values({emp[0][0]},0) ''')
            cursor.execute(f''' insert into salary(eid,base,bonus,total) values({emp[0][0]},{salary},0,{salary}) ''')
            messages.success(request,"Employee Added!!!")
    return render(request,"addemployee.html")

def viewemployee(request):
    cursor = connection.cursor()
    cursor.execute(''' select * from employee,rankk where employee.id = rankk.eid ''')
    employees = cursor.fetchall()
    print(employees)
    return render(request,"viewemployee.html",{"employees":employees})

def deleteemployee(request,id):
    cursor = connection.cursor()
    cursor.execute(f''' delete from employee where employee.id = {id} ''')
    cursor.execute(f''' delete from rankk where rankk.eid = {id} ''')
    return HttpResponseRedirect("/viewemp")

def assignproject(request):
    cursor = connection.cursor()
    if request.method == "POST":
        eid = request.POST.get("eid")
        pname = request.POST.get("pname")
        duedate = request.POST.get("duedate")

        command = ''' insert into project(eid,pname,duedate,mark,status) values(%s,%s,%s,1,"Due") '''
        params = (eid,pname,duedate)
        cursor.execute(command,params)
        messages.success(request,"Assigned!!!")
    return render(request,"assignproject.html")

def projectstatus(request):
    cursor = connection.cursor()
    cursor.execute(''' select * from project ''')
    projects = cursor.fetchall()
    return render(request,"projectstatus.html",{"projects":projects})

def salarystatus(request):
    cursor = connection.cursor()
    cursor.execute(''' select eid,firstName,base,bonus,total from employee,salary where employee.id = salary.eid ''')
    salaries = cursor.fetchall()
    print(salaries)
    return render(request,"salarystatus.html",{"salaries":salaries})


def logout(request):
    cursor = connection.cursor()
    cursor.execute(''' truncate table user ''') # delete all rows without destroying structure of table
    return HttpResponseRedirect("/")