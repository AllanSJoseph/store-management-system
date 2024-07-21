import mysql.connector as mys
from datetime import datetime as dt
from tabulate import tabulate
con=mys.connect(host="servername",user="your-username",password="your-password", database='store')
cur=con.cursor()

def invoiceNoGenerator():    #Automatically Generates a valid Invoice No for the bill
    cur.execute('select max(InvoiceNo) from bills')
    val=cur.fetchone()
    if val[0]==None:
        invoice=1
    else:
        invoice=int(val[0])+1
    return invoice
 
def addbill(IdNo):          #Inserts an Entry into bills table with required details
    invoiceNo=invoiceNoGenerator()
    date=dt.now().date()
    q="insert into bills(InvoiceNo,Date,UserId) values({},'{}',{})".format(invoiceNo,date,IdNo)
    cur.execute(q)
    con.commit()
    print("Bill Created Successfully, Your Invoice No is:",invoiceNo)
    return invoiceNo

def addEntry(invoiceNo):    #User can insert items which are purchased by the customer
    k='Y'
    while k in 'Yy':
        try:
            Prod_id=int(input("Enter Product ID: "))
            q="select * from products where ProdId={}".format(Prod_id)
            cur.execute(q)
            d=cur.fetchone()
            if d==None:
                print('\nItem Not Found\nPlease Try Again')
            else:
                ProdName=d[1]
                Price=d[2]
                Qty=int(input("Enter Quantity: "))
                TPrice=Price*Qty
                q="insert into bill_archive values({},{},'{}',{},{},{})".format(invoiceNo,Prod_id,ProdName,Price,Qty,TPrice)
                cur.execute(q)
                con.commit()
                print("\nItem Succesfully Added")
            k=input("Do you want to add more?[Y/N]: ")
        except ValueError:
            print("\nEnter a Valid Product Id")

def modifyEntry(invoiceNo):  #User can modify the quantity of a specific purchased item
    try:
        Prod_id=int(input("Enter Product ID: "))
        q="select * from bill_archive where InvoiceNo={} and ProdId={}".format(invoiceNo,Prod_id)
        cur.execute(q)
        d=cur.fetchone()
        if d==None:
            print('\nItem Not Found\nPlease Try Again')
        else:
            Price=d[3]
            Qty=int(input("Enter New Quantity: "))
            TPrice=Price*Qty
            q="update bill_archive set Qty={}, TPrice={} where InvoiceNo={} and ProdId={}".format(Qty,TPrice,invoiceNo,Prod_id)
            cur.execute(q)
            con.commit()
            print("\nItem Succesfully Updated")
    except ValueError:
        print("\nEnter a Valid Product Id")

def deleteEntry(invoiceNo): #User can remove purchased item from the draft bill
    try:
        Prod_id=int(input("Enter Product ID: "))
        q="select * from bill_archive where InvoiceNo={} and ProdId={}".format(invoiceNo,Prod_id)
        cur.execute(q)
        d=cur.fetchone()
        if d==None:
            print('\nItem Not Found\nPlease Try Again')
        else:
            q="delete from bill_archive where InvoiceNo={} and ProdId={}".format(invoiceNo,Prod_id)
            cur.execute(q)
            con.commit()
            print("\nItem Succesfully Deleted")
    except:
        print("\nEnter a Valid Product Id")

def displaybill(invoiceNo):  #Displays the draft bill
    q="select ProdId,ProdName,Price,Qty,TPrice from bill_archive where InvoiceNo={}".format(invoiceNo)
    cur.execute(q)
    data=cur.fetchall()
    print("\nInvoice No:",invoiceNo,'\n')
    h=['Product Id','Name','Price','Quantity','Total Price']
    print(tabulate(data,headers=h,tablefmt='fancy_grid'))
    q="select sum(TPrice) from bill_archive where InvoiceNo={}".format(invoiceNo)
    cur.execute(q)
    gt=cur.fetchone()
    print("\nGrand Total Price:",gt[0],"/-")

def updateStock(invoiceNo):   #Automatically Updates the Current stock of the product
    q="select ProdId,Qty from bill_archive where InvoiceNo={}".format(invoiceNo)
    cur.execute(q)
    p=cur.fetchall()
    for i in p:
        q="update products set Stock=Stock-{} where ProdId={}".format(i[1],i[0])
        cur.execute(q)
        con.commit()

def confirmation(invoiceNo):  #User confirms the draft bill after customer approves
    ch=input("\nConfirm Bill? [Y/N]: ")
    if ch in 'Yy':
        updateStock(invoiceNo) #After confirmation, the stock of the specific product will be reduced
        while True:
            pay=input("Enter your payment method (Cash/Card): ")
            if pay.upper() in ['CASH','CARD']:
                pay=pay.upper()
                q="select sum(TPrice) from bill_archive where InvoiceNo={}".format(invoiceNo)
                cur.execute(q)
                tp=cur.fetchone()
                print("\nYour Grand Total Price is Rs",tp[0],"/-")
                q="update bills set TotalPrice={}, PayMethod='{}' where InvoiceNo={}".format(tp[0],pay,invoiceNo)
                cur.execute(q)
                con.commit()
                print("\nBill Successfully Created and Archived!")
                return True
            else:
                print("\nPlease Enter a Valid Payment Method")
    else:
        return False

def discard(invoiceNo):   #Bill and its related details will be removed from the database
    print("\nDiscarding bill removes your bill from the database...")
    ch=input("Do you want to continue? This cannot be undone [Y/N]: ")
    if ch in "Yy":
        qlist=["delete from bills where invoiceNo=","delete from bill_archive where invoiceNo="]
        for i in qlist:
            q=i + str(invoiceNo)
            cur.execute(q)
            con.commit()
        print("\nBill Successfully Discarded from database.")
        return True
    else:
        return False

#The main menu of this module
def menu(IdNo):
    invoiceNo=addbill(IdNo)
    while True:
        h=["Choice","Corresponding Function"]
        functions=[('1','Add New Entry.'),('2','Modify existing Entry.'),('3','Delete Existing Entry'),('4','Display your Draft Bill'),('5','Finish Bill'),('6','Discard Draft Bill')]
        print("\nDraft Bill Functions\n")
        print(tabulate(functions,headers=h,tablefmt='simple'))
        try:                                     #To Prevent the program from failing
            ch=int(input("Enter your choice: "))
            if ch==1:
                addEntry(invoiceNo)
            elif ch==2:
                modifyEntry(invoiceNo)
            elif ch==3:
                deleteEntry(invoiceNo)
            elif ch==4:
                displaybill(invoiceNo)
            elif ch==5:
                confirmed=confirmation(invoiceNo)
                if confirmed:
                    break
            elif ch==6:
                discarded=discard(invoiceNo)
                if discarded:
                    break
            else:
                print("\nPlease enter a valid choice.")
        except ValueError:
            print("\nPlease enter a valid choice")
