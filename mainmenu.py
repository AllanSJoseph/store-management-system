import sys
from tabulate import tabulate
from User import login,account
from products import product
from billing import billFunctions,billaccess

print("""
-----------------------------------------------------------

             WELCOME TO SAR STORE MANAGEMENT SYSTEM
Authors: Sankaran Sanjai, Allan S Joseph and Mohamed Rayhan Mansoor

-----------------------------------------------------------
""")

def main():
    print('*'*25,'Login','*'*25)
    userId,Status=login.main()
    h=["Choice","Corresponding Function"]
    while True:
        if Status==None:
            print("For Security Reasons your access is denied.")
            print("Please Contact your administrator for gaining access.")
            ch=input("Enter any letter to exit program: ")
            sys.exit()

        elif Status.lower()=='admin':
            while True:
                functions=[('1','Open Account Dashboard'),('2','Open Products Dashboard'),('3','Open Archived Bills Dashboard'),('4','Exit/Logout')]
                print('\n'+'*'*25,'Main Menu','*'*25,'\n')
                print(tabulate(functions,headers=h,tablefmt='simple'))
                try:
                    ch=int(input("Enter your choice: "))
                    if ch==1:
                        account.main(Status,userId)
                    elif ch==2:
                        product.main(Status,userId)
                    elif ch==3:
                        billaccess.menu()
                    elif ch==4:
                        sys.exit()
                    else:
                        print("\nInvalid Input\nPlease Try Again")
                except ValueError:
                    print("\nInvalid Input\nPlease Try Again")
        
        elif Status.lower()=='stocker':
            while True:
                functions=[('1','Open Account Dashboard'),('2','Open Products Dashboard'),('3','Exit/Logout')]
                print('\n'+'*'*25,'Main Menu','*'*25,'\n')
                print(tabulate(functions,headers=h,tablefmt='simple'))
                try:
                    ch=int(input("Enter your choice: "))
                    if ch==1:
                        account.main(Status,userId)
                    elif ch==2:    
                        product.main(Status,userId)
                    elif ch==3:
                        sys.exit()
                    else:
                        print("\nInvalid Input\nPlease Try Again")
                except ValueError:
                    print("\nInvalid Input\nPlease Try Again")
        
        elif Status.lower()=='cashier':
            while True:
                functions=[('1','Account Dashboard'),('2','Show List of Products'),('3','Create New Bill'),('4','Display bills you created'),('5','Exit/Logout')]
                print('\n'+'*'*25,'Main Menu','*'*25,'\n')
                print(tabulate(functions,headers=h,tablefmt='simple'))
                try:
                    ch=int(input("Enter your choice: "))
                    if ch==1:
                        account.main(Status,userId)
                    elif ch==2:
                        print("Note: Your account cannot make any changes to the products table.")
                        product.display_Products()
                    elif ch==3:
                        billFunctions.menu(userId)
                    elif ch==4:
                        billaccess.display_cashier(userId,Status)
                    elif ch==5:
                        sys.exit()
                    else:
                        print("\nInvalid Input\nPlease Try Again")
                except ValueError:
                    print("\nInvalid Input\nPlease Try Again")
            


if __name__=="__main__":
    main()
