import mysql.connector as mys
from tabulate import tabulate
con=mys.connect(host="servername",user="your-username",password="your-password", database='store')
cur=con.cursor()

def displaybills():
    q="select * from bills order by InvoiceNo"
    cur.execute(q)
    data=cur.fetchall()
    h=['Invoice No','Date of Purchase','Total Price','Payment Method','Cashier Id']
    print(tabulate(data,headers=h,tablefmt='fancy_grid'))

def displayIndividual():
    st=int(input("Enter Invoice No: "))
    q="select * from bills where InvoiceNo={}".format(st)
    cur.execute(q)
    data=cur.fetchall()
    if data==None:
        print("Invoice No does not exist,\nPlease Try Again")
    else:
        q="select ProdId,ProdName,Price,Qty,TPrice from bill_archive where InvoiceNo={}".format(st)
        cur.execute(q)
        d=cur.fetchall()
        print("Archived Bill Found")
        print("\nBill Details")
        h=['Invoice No','Date of Purchase','Total Price','Payment Method','Cashier Id']
        print(tabulate(data,headers=h,tablefmt='fancy_grid'))
        print("\nArchived Bill")
        h=['Product Id','Name','Price','Quantity','Total Price']
        print(tabulate(d,headers=h,tablefmt='fancy_grid'))

def display_cashier(userId,status):
    if status=='admin':
        q="select Username from users where Status='Cashier' and userId={}".format(userId)
        cur.execute(q)
        found=cur.fetchone()
        if found==None:
            print("Cashier not found")
        else:
            q="select InvoiceNo,Date,TotalPrice,PayMethod,Username from bills NATURAL JOIN users where userId={}".format(userId)
            cur.execute(q)
            data=cur.fetchall()
            print('\nCashier Found\nBills Created By the cashier:-')
            if data==None:
                print("Cashier at Userid",userId,"haven't created any bills.")
            else:
                h=['Invoice No','Date of Purchase','Total Price','Payment Method','Cashier']
                print(tabulate(data,headers=h,tablefmt='fancy_grid'))
    else:
        print('Bills Created By You:-')
        q="select InvoiceNo,Date,TotalPrice,PayMethod,Username from bills NATURAL JOIN users where userId={}".format(userId)
        cur.execute(q)
        data=cur.fetchall()
        h=['Invoice No','Date of Purchase','Total Price','Payment Method','Cashier']
        print(tabulate(data,headers=h,tablefmt='fancy_grid'))
        

def delete():
    print("This deletes all bill data and resets your invoice no to 1")
    k=input("Do you want to delete all Bill Data? [Y/N]: ")
    if k in 'Yy':
        q=("delete from bills","delete from bill_archive")
        for i in q:
            cur.execute(i)
            con.commit()
        print("All Bill data cleared from your database")

def export():
    print("This exports your bill data and archived bills into two csv files")
    fc=input("Do you want to continue?[Y/N]: ")
    if fc in 'Yy':
        print("Exporting in Progress, This may take some time")
        import csv
        import os
        from datetime import datetime as dt
        date=dt.now().date()
        name="exportedbills{}".format(date)
        os.mkdir(name)                   #Creates a folder at the Current Working Directory
        bills=name+'/bills.csv'
        ba=name+'/bill_archive.csv'
        with open(bills,"w",newline='') as b: #Creates csv file in the newly created directory
            q="select * from bills order by InvoiceNo"
            cur.execute(q)
            v=cur.fetchall()
            w=csv.writer(b)
            w.writerow(['Invoice No','Date of Purchase','Total Price','Payment Method','Cashier Id'])
            for i in v:
                w.writerow([i[0],i[1],i[2],i[3],i[4]])
            print("\nExported List of Bills to bills.csv")
                           
        with open(ba,"w",newline='') as b:    #Creates csv file in the newly created directory
            q="select * from bill_archive"
            cur.execute(q)
            v=cur.fetchall()
            w=csv.writer(b)
            w.writerow(['Invoice No','Date of Purchase','Total Price','Payment Method'])
            for i in v:
                w.writerow([i[0],i[1],i[2],i[3]])
            print("\nExported All Archived Bills to bill_archive.csv")
        print("\nExporting Successfull, your exported files are stored in a folder",name)
    

def menu():
    while True:
        h=["Choice","Corresponding Function"]
        functions=[('1','Display List of Archived Bills.'),('2','Open an Archived Bill.'),('3','Sort bills by cashier'),('4','Delete All Bill Data'),('5','Export Archived Bills to csv'),('6','Back')]
        print('\n'+'*'*25,'Archived Bills Dashboard','*'*25,'\n')
        print(tabulate(functions,headers=h,tablefmt='simple'))
        try:
            ch=int(input("Enter your choice: "))
            if ch==1:
                displaybills()
            elif ch==2:
                displayIndividual()
            elif ch==3:
                staffId=int(input('Enter the UserId of cashier: '))
                display_cashier(staffId,'admin')
            elif ch==4:
                delete()
            elif ch==5:
                export()
            elif ch==6:
                break
            else:
                print("Invalid Input\nPlease Try Again.")
        except ValueError:
            print("\nInvalid Input\nPlease Try Again")
