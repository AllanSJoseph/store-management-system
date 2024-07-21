import mysql.connector as mys
con=mys.connect(host="servername",user="your-username",password="your-password", database='store')
cur=con.cursor()


def login():
    cur.execute("select * from users")
    l=cur.fetchall()
    uName=input("Enter Username: ")
    Pass=input("Enter Password: ")
    for i in l:
        if i[1]==uName and i[2]==Pass:
            print("Welcome",uName)
            return (i[0],i[3])
            break
    else:
        print("Invalid Username or Password\n")                                #if any of the info given is not matching
        return main()
    
        #Sign up Function
def signup():
    newUser = input('\nChoose new username: ')
    cur.execute("select * from users")
    l=cur.fetchall()
    for i in l:                   #checks if the username given is taken by anyone else before
        if i[1]==newUser:
            print('Username not available')
            return signup()
            break
    
    else:
        newPass = input('\nChoose new password: ')
        NewUserId=(l[-1][0]+1)
        q="insert into users(UserId,Username,Password) values({},'{}','{}')".format(NewUserId,newUser,newPass)
        cur.execute(q)
        con.commit()
        print('\nLogin to your new account\n')
        return login()



def main():
    x=input('\nDo you want to sign up or try login?(s/l) :')
    if x.lower()=='s':
        return signup()
    elif x.lower()=='l':
        return login()
    else:
        print('Invalid input')
        return main()
