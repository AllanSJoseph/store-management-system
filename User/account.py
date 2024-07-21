from tabulate import tabulate
import mysql.connector as mys
con=mys.connect(host="servername",user="your-username",password="your-password", database='store')
cur=con.cursor()

def display():
    try:
        n=input('Enter category to be displayed (All,Cashier,Stocker,Unassigned): ')
        if n.lower()=='all':
            cur.execute("select UserId,Username,status from users where status in ('cashier','stocker') or status is NULL")
            l=cur.fetchall()
            h=['User Id','Name','Status']
            print(tabulate(l,headers=h,tablefmt='fancy_grid'))
        elif n.lower()=='cashier' or n.lower()=='stocker':
            cur.execute("select UserId,Username,status from users where status='"+n+"'")
            l=cur.fetchall()
            h=['User Id','Name','Status']
            print(tabulate(l,headers=h,tablefmt='fancy_grid'))
        elif n.lower()=='unassigned':
            cur.execute("select UserId,Username,status from users where status is null")
            l=cur.fetchall()
            h=['User Id','Name','Status']
            print(tabulate(l,headers=h,tablefmt='fancy_grid'))
        else:
            print("\nPlease Enter a valid Input")
    except ValueError:
        print("\nPlease Enter a valid Input")

def search(userId):
    cur.execute("select UserId,Username,status from users where UserId={}".format(userId))
    l=cur.fetchall()
    if len(l)==0:
        print("\nUser Not Found\nPlease Try Again")
    else:
        h=['IdNo','Name','Status','Last Updated By']
        print(tabulate(l,headers=h,tablefmt='fancy_grid'))
    
def update():
    userId=input('Enter the UserId of the staff :')
    cur.execute("select UserId from users where status = 'admin' or UserId=0")
    l=cur.fetchall()
    adminList = []
    for i in l:
        adminList.append(i[0])
    if int(userId) in adminList:
        print('Status of Given UserId cannot be assigned/modified')
        n=input('Do you want to assign/modify another user?(y/n): ')
        if n.lower()=='y':
            AssignModify(adminId)    
    else:
        while True:
            h=['Choice', 'Status']
            l=[('1','Cashier'),('2','Stocker'),('3','Admin')]
            print(tabulate(l,headers=h,tablefmt='grid'))
            n=int(input('Enter Status option :'))
            if n==1:
                status='cashier'
            elif n==2:
                status='stocker'
            elif n==3:
                status='admin'
            else:
                print('\nPlease Enter a Valid Choice')
                continue
            break
        cur.execute("update users set status ='"+status+"' where UserId='"+userId+"'")
        con.commit()
        print('UserId',userId,'Status updated to',status)

def remove():
    userId=input('Enter the UserId of the staff: ')
    cur.execute("select UserId from users where status = 'Admin'")
    l=cur.fetchall()
    adminList = []
    for i in l:
        adminList.append(i[0])
    if int(userId) in adminList:
        print('Given UserId cannot be removed')
        n=input('Do you want to remove another user?(y/n): ')
        if n.lower()=='y':
            remove()
    else:
        cur.execute("delete from users where UserId={}".format(userId))
        con.commit()
##        cur.execute("update bills set UserId=0 where UserId={}".format(userId))
##        con.commit()     #To prevent Unexpected Outputs when accessing bills table
        print('UserId at',userId,'deleted')

def change_pass(userId):
    oldPass=input("Enter your current password: ")
    cur.execute("select * from users where UserId={}".format(userId))
    l=cur.fetchone()
    if oldPass==l[2]:
        newPass=input("\nEnter your new password: ")
        confirmPass=input("\nConfirm your new password: ")
        if confirmPass==newPass:
            cur.execute("update users set password='{}' where UserId={}".format(newPass,userId))
            con.commit()
            print('\nPassword Successfully Updated')
        else:
            print("\nCannot Change your Password\nConfirmation password not matching new password\nPlease Try Again")
    else:
        print("\nCannot Authorize your account\nPlease Try Again")


def main(status,userId):
    while True:
        print("\n"+'*'*20+"Account Dashboard"+'*'*20+"\n")
        if status.lower()=='admin':
            h=['Choice', 'Corresponding Function']
            l=[('1','Display Your Staff Records'),('2','Search Staff'),('3','Update Status'),('4','Remove Staff'),('5','Change Account Password'),('6','Back')]
            print(tabulate(l,headers=h,tablefmt='simple'))
            n=int(input('Enter choice :'))
            if n==1:
                display()
            elif n==2:
                staffId=input('Enter the UserId of the staff: ')
                search(staffId)
            elif n==3:
                update()
            elif n==4:
                remove()
            elif n==5:
                change_pass(userId)
            elif n==6:
                break
            else:
                print('Invalid Input')
        elif status.lower()=='cashier':
            h=['Choice', 'Corresponding Function']
            l=[('1','Change Account Password'),('2','Back')]
            print(tabulate(l,headers=h,tablefmt='simple'))
            n=int(input('Enter choice :'))
            if n==1:
                change_pass(userId)
            elif n==2:
                break
            else:
                print('\nInvalid Input\nPlease Try Again')
        elif status.lower()=='stocker':
            h=['Choice', 'Corresponding Function']
            l=[('1','Change Account Password'),('2','Back')]
            print(tabulate(l,headers=h,tablefmt='simple'))
            n=int(input('Enter choice :'))
            if n==1:
                change_pass(userId)
            elif n==2:
                break
            else:
                print('\nInvalid Input\nPlease Try Again')
