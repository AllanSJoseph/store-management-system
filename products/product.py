from tabulate import tabulate
import mysql.connector as mys
con=mys.connect(host="servername",user="your-username",password="your-password", database='store')
cur=con.cursor()

def add_item(userId):  #Adds Item to Products Table
    cur.execute("select ProdId from products")
    codes=cur.fetchall()
    while True:
        item_code = int(input("Enter Product Id: "))
        for i in codes:
            if item_code==i[0]:
                print("Item Code Already Exists.")
                break
        else:
            item_name = input("Enter new Product Name: ")
            item_price = int(input("Enter Price: "))
            item_stock = int(input("Enter Stock: "))
            cur.execute("insert into products values({},'{}',{},{},{})".format(item_code,item_name,item_price,item_stock,userId))
            con.commit()
            print("\nProduct added.")
        ch=input("Do you want to continue? [Y/N]: ")
        if ch in "Nn":
            break

def delete_item(): #Deletes Item from Products table
    s=int(input("Enter the Product Id of the item to be deleted: "))
    cur.execute("Delete from products where ProdId={}".format(s))
    con.commit()
    print("Item code",s,"deleted.")
    
def modifystock_item(userId): #Modifies Stock of the specific item
    s=int(input("Enter the item code to be updated: "))
    query="select * from products where ProdId={}".format(s)
    cur.execute(query)
    data=cur.fetchone()
    if data==None:
        print("Record not found")
    else:
        n=int(input("Enter new stock:"))
        query="update products set Stock={}, UserId={} where ProdId={}".format(n,userId,s)
        cur.execute(query)
        con.commit()
        print(cur.rowcount, " record updated.")
        
def modifyitem_price(userId):  #Modifies Price of the specific item
    s=int(input("Enter the item code to be updated: "))
    query="select * from products where ProdId={}".format(s)
    cur.execute(query)
    data=cur.fetchone()
    if data==None:
        print("Record not found")
    else:
        n=int(input("Enter new price:"))
        query="update products set Price={}, UserId={} where ProdId={}".format(n,userId,s)
        cur.execute(query)
        con.commit()
        print(cur.rowcount, " record updated.")
        
def display_Products(): #Displays Product table
    cur.execute("select ProdId,ProdName,Price,Stock from products")
    data=cur.fetchall()
    print("\n"+'*'*20+"Products Saved to Database"+'*'*20+"\n")
    h=['Product Id','Name','Price','Stock']
    print(tabulate(data,headers=h,tablefmt='fancy_grid'))

def display_stocker(userId,status):
    if status=='admin':
        q="select Username from users where Status='Stocker' and userId={}".format(userId)
        cur.execute(q)
        found=cur.fetchone()
        if found==None:
            print("\nStocker not found")
        else:
            q="select ProdId,ProdName,Price,Stock,Username from products NATURAL JOIN users where userId={}".format(userId)
            cur.execute(q)
            data=cur.fetchall()
            if data==None:
                print("Stocker at Userid",userId,"haven't updated any data recently.")
            else:
                print("\nProduct Entries Updated by Stocker\n")
                h=['Product Id','Name','Price','Stock','Last Updated By (Stocker)']
                print(tabulate(data,headers=h,tablefmt='fancy_grid'))
    else:
        q="select ProdId,ProdName,Price,Stock,Username from products NATURAL JOIN users where userId={}".format(userId)
        cur.execute(q)
        data=cur.fetchall()
        print("\nProduct Entries Updated Recently by You :-\n")
        h=['Product Id','Name','Price','Stock','Last Updated By (Stocker)']
        print(tabulate(data,headers=h,tablefmt='fancy_grid'))
        
def main(status,userId):
    while True:
        print("\n"+'*'*20+"Product Dashboard"+'*'*20+"\n")
        if status.lower()=='admin':
            h=["Choice","Corresponding Function"]
            functions=[('1','Add Products to Database'),('2','Delete products from database'),('3','Modify products'),('4','Display products'),('5','Sort Products by Stocker who updated'),('6','Back')]
            print(tabulate(functions,headers=h,tablefmt='simple'))
            #try:
            ch=int(input("Enter your choice:"))
            if ch==1:
                add_item(userId)
            elif ch==2:
                delete_item()
            elif ch==3:
                print("Your account is only allowed to change the price of the product.")
                modifyitem_price(userId)
            elif ch==4:
                display_Products()
            elif ch==5:
                user=int(input("Enter userId of Stocker: "))
                display_stocker(user,status)
            elif ch==6:
                break
            else:
                print("\nEnter a Valid Choice")
        else:
            h=["Choice","Corresponding Function"]
            functions=[('1','Add Products to Database'),('2','Delete products from system'),('3','Modify products'),('4','Display products'),('5','Display products recently updated by you'),('6','Back')]
            print("\nMain Menu\n")
            print(tabulate(functions,headers=h,tablefmt='simple'))
            try:
                ch=int(input("Enter your choice: "))
                if ch==1:
                    add_item(userId)
                elif ch==2:
                    delete_item()
                elif ch==3:
                    print("Your account is only allowed to change the stock count.")
                    modifystock_item(userId)
                elif ch==4:
                    display_Products()
                elif ch==5:
                    display_stocker(userId,status)
                elif ch==6:
                    break
                else:
                    print("\nEnter a Valid Choice")
            except NameError:
                print("\nEnter a Valid Choice")
