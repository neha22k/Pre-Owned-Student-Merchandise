from django.views import View
from django.shortcuts import render
from django.template import RequestContext
from django.contrib import messages
import pymysql
from django.http import HttpResponse
from django.core.files.storage import FileSystemStorage
import os
from datetime import date

global uname

def getDetails(owner):
    contact_no = "none"
    con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'preowned',charset='utf8')
    with con:
        cur = con.cursor()
        cur.execute("select contact_no from signup where username = '"+owner+"'")
        rows = cur.fetchall()
        for row in rows:
            contact_no = row[0]
            break
    return contact_no

def PurchaseProduct(request):
    if request.method == 'GET':
        global uname
        pname = request.GET.get('t1', False)
        price = request.GET.get('t2', False)
        dd = str(date.today())
        db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'preowned',charset='utf8')
        db_cursor = db_connection.cursor()
        student_sql_query = "INSERT INTO purchase VALUES('"+uname+"','"+pname+"','"+price+"','"+dd+"')"
        db_cursor.execute(student_sql_query)
        db_connection.commit()
        context= {'data':'Product Purchase successfully recorded in database'}
        return render(request, 'UserScreen.html', context)           

def ViewHistory(request):
    if request.method == 'GET':
        global uname
        output ='<table border=1 align=center width=100%><tr><th><font size="" color="black">Purchase Name</th><th><font size="" color="black">Product Name</th>'
        output += '<th><font size="" color="black">Product Price</th><th><font size="" color="black">Purchase Date</th>'
        output+='</tr>'    
        query = "select * from purchase where purchaser_name='"+uname+"'"
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'preowned',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute(query)
            rows = cur.fetchall()
            for row in rows:
                user = row[0]
                product = row[1]
                price = str(row[2])
                dd = row[3]
                output += '<tr><td><font size="" color="black">'+user+'</td><td><font size="" color="black">'+product+'</td>'
                output += '<td><font size="" color="black">'+price+'</td><td><font size="" color="black">'+dd+'</td></tr>'
        output += "</table><br/><br/><br/><br/>"        
        context= {'data':output}
        return render(request, 'UserScreen.html', context)         

def SearchProductsAction(request):
    if request.method == 'POST':
        global uname
        category = request.POST.get('t1', False)
        price = request.POST.get('t2', False)
        location = request.POST.get('t3', False)
        from_price = 0
        to_price = 0
        if 'Above' in price:
            from_price = 1000
            to_price = 100000
        else:
            arr = price.split("-")
            from_price = float(arr[0].strip())
            to_price = float(arr[1].strip())
        output ='<table border=1 align=center width=100%><tr><th><font size="" color="black">Owner Name</th><th><font size="" color="black">Contact No</th>'
        output += '<th><font size="" color="black">Product ID</th><th><font size="" color="black">Product Name</th>'
        output += '<th><font size="" color="black">Description</th><th><font size="" color="black">Price</th>'
        output += '<th><font size="" color="black">Product Condition</th><th><font size="" color="black">Product Category</th>'
        output += '<th><font size="" color="black">Location</th><th><font size="" color="black">Image</th>'
        output += '<th><font size="" color="black">Purchase Product</th>'
        output+='</tr>'    
        query = "select * from product where category='"+category+"' and price >= '"+str(from_price)+"' and price <= '"+str(to_price)+"' and location like '%"+location+"%'"
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'preowned',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute(query)
            rows = cur.fetchall()
            for row in rows:
                owner = row[0]
                contact = getDetails(owner)
                pid = row[1]
                pname = row[2]
                desc = row[3]
                price = row[4]
                prod_condition = row[5]
                categories = row[6]
                locations = row[7]
                image = row[8]
                output += '<tr><td><font size="" color="black">'+owner+'</td><td><font size="" color="black">'+contact+'</td>'
                output += '<td><font size="" color="black">'+str(pid)+'</td><td><font size="" color="black">'+pname+'</td>'
                output += '<td><font size="" color="black">'+desc+'</td><td><font size="" color="black">'+str(price)+'</td>'
                output += '<td><font size="" color="black">'+prod_condition+'</td><td><font size="" color="black">'+categories+'</td>'
                output += '<td><font size="" color="black">'+locations+'</td>'
                output += '<td><img src="static/photo/'+image+'" height="200" width="200"/></td>'
                output+='<td><a href=\'PurchaseProduct?t1='+str(pname)+'&t2='+str(price)+'\'><font size=3 color=red>Click Here to Purchase</font></a></td></tr>'                
        output += "</table><br/><br/><br/><br/>"        
        context= {'data':output}
        return render(request, 'UserScreen.html', context)        

def SearchProducts(request):
    if request.method == 'GET':
        return render(request, 'SearchProducts.html', {})

def SaleProduct(request):
    if request.method == 'GET':
        return render(request, 'SaleProduct.html', {})

def SaleProductAction(request):
    if request.method == 'POST':
        global uname
        pname = request.POST.get('t1', False)
        desc = request.POST.get('t2', False)
        price = request.POST.get('t3', False)
        condition = request.POST.get('t4', False)
        category = request.POST.get('t5', False)
        location = request.POST.get('t6', False)
        filename = request.FILES['t7'].name
        myfile = request.FILES['t7'].read() #reading uploaded file from user
        pid = 1
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'preowned',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select max(product_id) from product")
            rows = cur.fetchall()
            for row in rows:
                pid = row[0]
        if pid is None:
            pid = 1
        else:
            pid += 1
        db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'preowned',charset='utf8')
        db_cursor = db_connection.cursor()
        student_sql_query = "INSERT INTO product VALUES('"+uname+"','"+str(pid)+"','"+pname+"','"+desc+"','"+price+"','"+condition+"','"+category+"','"+location+"','"+filename+"')"
        db_cursor.execute(student_sql_query)
        db_connection.commit()
        if os.path.exists('ProductApp/static/photo/'+filename):
            os.remove('ProductApp/static/photo/'+filename)
        with open('ProductApp/static/photo/'+filename, "wb") as file:
            file.write(myfile)
        file.close()    
        context= {'data':'Product details added with Product ID = '+str(pid)}
        return render(request, 'SaleProduct.html', context)           

def Feedback(request):
    if request.method == 'GET':
        output = '<tr><td><font size="3" color="black">Product&nbsp;ID</b></td><td><select name="t1">'
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'preowned',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select product_id from product")
            rows = cur.fetchall()
            for row in rows:
                output += '<option value="'+str(row[0])+'">'+str(row[0])+'</option>'
        output += "</select></td></tr>"
        context= {'data1': output}
        return render(request, 'Feedback.html', context)  

def UserLogin(request):
    if request.method == 'GET':
       return render(request, 'UserLogin.html', {})

def index(request):
    if request.method == 'GET':
       return render(request, 'index.html', {})

def Register(request):
    if request.method == 'GET':
       return render(request, 'Register.html', {})

def FeedbackAction(request):
    if request.method == 'POST':
        global uname
        product_id = request.POST.get('t1', False)
        feedback = request.POST.get('t2', False)
        ratings = request.POST.get('t3', False)
        db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'preowned',charset='utf8')
        db_cursor = db_connection.cursor()
        student_sql_query = "INSERT INTO feedback(username,product_id,feedback,ratings) VALUES('"+uname+"','"+product_id+"','"+feedback+"','"+ratings+"')"
        db_cursor.execute(student_sql_query)
        db_connection.commit()
        context= {'data':'Your feedback accepted'}
        return render(request, 'UserScreen.html', context)    

def RegisterAction(request):
    if request.method == 'POST':
        username = request.POST.get('t1', False)
        password = request.POST.get('t2', False)
        contact = request.POST.get('t3', False)
        email = request.POST.get('t4', False)
        address = request.POST.get('t5', False)        
        status = 'none'
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'preowned',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select username from signup where username = '"+username+"'")
            rows = cur.fetchall()
            for row in rows:
                if row[0] == email:
                    status = 'Given Username already exists'
                    break
        if status == 'none':
            db_connection = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'preowned',charset='utf8')
            db_cursor = db_connection.cursor()
            student_sql_query = "INSERT INTO signup(username,password,contact_no,email_id,address) VALUES('"+username+"','"+password+"','"+contact+"','"+email+"','"+address+"')"
            db_cursor.execute(student_sql_query)
            db_connection.commit()
            print(db_cursor.rowcount, "Record Inserted")
            if db_cursor.rowcount == 1:
                status = 'Signup Process Completed'
        context= {'data':status}
        return render(request, 'Register.html', context)

def AdminLogin(request):
    if request.method == 'GET':
       return render(request, 'AdminLogin.html', {})

def AdminLoginAction(request):
    if request.method == 'POST':
        global uname
        option = 0
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        if username == "admin" and password == "admin":
            context= {'data':'welcome '+username}
            return render(request, 'AdminScreen.html', context)
        else:
            context= {'data':'Invalid login details'}
            return render(request, 'AdminLogin.html', context)    

def UserLoginAction(request):
    if request.method == 'POST':
        global uname
        option = 0
        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'preowned',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute("select * FROM signup")
            rows = cur.fetchall()
            for row in rows:
                if row[0] == username and row[1] == password:
                    uname = username
                    option = 1
                    break
        if option == 1:
            context= {'data':'welcome '+username}
            return render(request, 'UserScreen.html', context)
        else:
            context= {'data':'Invalid login details'}
            return render(request, 'UserLogin.html', context)

def ViewUsers(request):
    if request.method == 'GET':
        global uname
        output ='<table border=1 align=center width=100%><tr><th><font size="" color="black">Username</th><th><font size="" color="black">Password</th>'
        output += '<th><font size="" color="black">Contact No</th><th><font size="" color="black">Email ID</th>'
        output += '<th><font size="" color="black">Address</th>'
        output+='</tr>'    
        query = "select * from signup"
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'preowned',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute(query)
            rows = cur.fetchall()
            for row in rows:
                user = row[0]
                password = row[1]
                contact = row[2]
                email = row[3]
                address = row[4]
                output += '<tr><td><font size="" color="black">'+user+'</td><td><font size="" color="black">'+password+'</td>'
                output += '<td><font size="" color="black">'+contact+'</td><td><font size="" color="black">'+email+'</td>'
                output += '<td><font size="" color="black">'+address+'</td></tr>'
        output += "</table><br/><br/><br/><br/>"        
        context= {'data':output}
        return render(request, 'AdminScreen.html', context)         

def ViewProducts(request):
    if request.method == 'GET':
        output ='<table border=1 align=center width=100%><tr><th><font size="" color="black">Owner Name</th><th><font size="" color="black">Contact No</th>'
        output += '<th><font size="" color="black">Product ID</th><th><font size="" color="black">Product Name</th>'
        output += '<th><font size="" color="black">Description</th><th><font size="" color="black">Price</th>'
        output += '<th><font size="" color="black">Product Condition</th><th><font size="" color="black">Product Category</th>'
        output += '<th><font size="" color="black">Location</th><th><font size="" color="black">Image</th>'
        output+='</tr>'    
        query = "select * from product"
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'preowned',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute(query)
            rows = cur.fetchall()
            for row in rows:
                owner = row[0]
                contact = getDetails(owner)
                pid = row[1]
                pname = row[2]
                desc = row[3]
                price = row[4]
                prod_condition = row[5]
                categories = row[6]
                locations = row[7]
                image = row[8]
                output += '<tr><td><font size="" color="black">'+owner+'</td><td><font size="" color="black">'+contact+'</td>'
                output += '<td><font size="" color="black">'+str(pid)+'</td><td><font size="" color="black">'+pname+'</td>'
                output += '<td><font size="" color="black">'+desc+'</td><td><font size="" color="black">'+str(price)+'</td>'
                output += '<td><font size="" color="black">'+prod_condition+'</td><td><font size="" color="black">'+categories+'</td>'
                output += '<td><font size="" color="black">'+locations+'</td>'
                output += '<td><img src="static/photo/'+image+'" height="200" width="200"/></td></tr>'
        output += "</table><br/><br/><br/><br/>"        
        context= {'data':output}
        return render(request, 'AdminScreen.html', context)

def ViewFeedback(request):
    if request.method == 'GET':
        global uname
        output ='<table border=1 align=center width=100%><tr><th><font size="" color="black">Username</th><th><font size="" color="black">Product ID</th>'
        output += '<th><font size="" color="black">Feedback</th><th><font size="" color="black">Ratings</th>'
        output+='</tr>'    
        query = "select * from feedback"
        con = pymysql.connect(host='127.0.0.1',port = 3306,user = 'root', password = 'root', database = 'preowned',charset='utf8')
        with con:
            cur = con.cursor()
            cur.execute(query)
            rows = cur.fetchall()
            for row in rows:
                user = row[0]
                product = row[1]
                feedback = row[2]
                ratings = row[3]
                output += '<tr><td><font size="" color="black">'+user+'</td><td><font size="" color="black">'+product+'</td>'
                output += '<td><font size="" color="black">'+feedback+'</td><td><font size="" color="black">'+ratings+'</td></tr>'
        output += "</table><br/><br/><br/><br/>"        
        context= {'data':output}
        return render(request, 'AdminScreen.html', context)  
      
from django.views import View
from django.shortcuts import render

class PaymentView(View):
    def get(self, request):
        return render(request, 'payment.html')  # Ensure this matches your template name
    from django.shortcuts import render

from django.views import View
from django.shortcuts import render

class UPIPaymentView(View):
    def get(self, request):
        return render(request, 'upi_payment.html')