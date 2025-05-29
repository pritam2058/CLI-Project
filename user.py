import csv
import sqlite3

def create_connection():
    try:
        con=sqlite3.connect('users.sqlite3')
        return con
    
    except Exception as e:
        print(e)

INPUT_STRING="""
Enter the option:
    1. CREATE TABLE
    2. DUMP users from csv INTO users TABLE
    3. ADD new user INTO users TABLE
    4. QUERY all users from TABLE
    5. QUERY users by id from TABLE
    6. QUERY specified no. of records from TABLE
    7. DELETE all users
    8. DELETE users by id
    9. UPDATE user
    10. Press any key to EXIT
"""
#  1. CREATE TABLE
def create_table(con):
    CREATE_USER_TABLE_QUERY="""
        CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name CHAR(255) NOT NULL,
        last_name CHAR(255) NOT NULL,
        company_name CHAR(255) NOT NULL,
        address CHAR(255) NOT NULL,
        city CHAR(255) NOT NULL,
        county CHAR(255) NOT NULL,
        state CHAR(255) NOT NULL,
        zip REAL NOT NULL,
        phone1 CHAR(255) NOT NULL,
        phone CHAR(255),
        email CHAR(255) NOT NULL,
        web text
      )
    """
    cur=con.cursor()
    cur.execute(CREATE_USER_TABLE_QUERY)
    print("User table was created successfully.")

#  2. DUMP users from csv INTO users TABLE
def read_csv():
    users=[]
    with open("sample_users.csv","r") as f:
        data=csv.reader(f)
        for user in data:
            users.append(tuple(user))
        
        return users[1:]
    
def insert_users(con,users):
    user_add_query ="""
        INSERT INTO users
        (
            first_name,
            last_name,
            company_name,
            address,
            city,
            county,
            state,
            zip,
            phone1,
            phone,
            email,
            web
        )
        VALUES (?,?,?,?,?,?,?,?,?,?,?,?);
    """
    cur=con.cursor()
    cur.executemany(user_add_query,users)
    con.commit()
    print(f"{len(users)} users were imported successfully.")

#  3. ADD new user INTO users TABLE
COLUMNS = (
    "first_name",
    "last_name",
    "company_name",
    "address",
    "city",
    "county",
    "state",
    "zip",
    "phone1",
    "phone",
    "email",
    "web",
)

# 4. QUERY all users from TABLE
def QUERY_all_users(con):
    cur = con.cursor()
    query_all=cur.execute("SELECT * FROM users")
    for u in query_all:
        print(u)
        
#  5. QUERY users by id from TABLE
def Query_users_by_id(con, user_id):
    cur = con.cursor()
    cur.execute("SELECT * FROM users WHERE id=?;", (user_id,))
    rows = cur.fetchall()
    
    if rows:
        for row in rows:
            print("User found:", row)

    # Applicable if you want to Query users by providing multiple ids

    # ids_list = []
    # ids = input("Enter the id's in comma separated form : ")
    # split_ids = ids.split(',') # Given input lai list ko form ma rakhxa, by separating with comma
    # for i in split_ids:
    #     remove_space = i.strip() # unnecessary spaces haru remove garxa
    #     id = int(remove_space) # id chai string format ma hunxa eg: "1" so yelai integer ma convert garna parxa eg: 1
    #     ids_list.append(id)
    
    # print(f"The given id's are: {ids_list}")

    # placeholder=','.join(['?'] * len(ids_list))
    # query = f" SELECT * from users where id IN ({placeholder})"
    # cur.execute(query,ids_list)
    # rows = cur.fetchall()

    # for row in rows:
    #     print(row)


#  6. QUERY specified no. of records from TABLE
def select_specified_no_of_users(con,no_of_users):
        cur = con.cursor()
        users = cur.execute("SELECT * FROM users LIMIT ?; ",(no_of_users,))
        for user in users:
            print(user)
            

def delete_user(con):
    cur = con.cursor()
    cur.execute("DELETE FROM users;")
    con.commit()
    print("ALL users were deleted successfully")

def delete_user_by_id(con,user_id):
    cur = con.cursor()
    cur.execute("DELETE FROM users where id=?",(user_id,))
    con.commit()
    print(f"User with id [{user_id}] was successfully deleted")

def update_user_by_id(con,user_id,column_name,column_value):
    cur = con.execute()
    cur.execute(
        f"UPDATE users set {column_name}=? where id = ?;",(column_name,user_id)
    )
    con.commit()
    print(
        f"[{column_name}] was updated with value [{column_value}] of user with id [{user_id}]"
    )


def main():
    con = create_connection()
    user_input = input(INPUT_STRING)
    if user_input == "1":
        create_table(con)

    elif user_input == "2":
        users = read_csv()
        insert_users(con,users)

    elif user_input == "3":
        user_data = []
        for column in COLUMNS:
            column_value = input(f"Enter the value for {column}: ")
            user_data.append(column_value)
        
        insert_users(con, [tuple(user_data)])  
        print("New user added successfully.")


    elif user_input == "4":
        QUERY_all_users(con)

    elif user_input == "5":
        id_input = input("Enter the ID number: ")
        if id_input.isnumeric():
             Query_users_by_id(con, int(id_input))

    elif user_input == "6":
        no_of_users = input("Enter the id no. : ")
        if no_of_users.isnumeric():
            select_specified_no_of_users(con,no_of_users)
    
    elif user_input == "7":
        confirmation = input("Are you sure you want to delete all users? (y/n): ")
        if confirmation == "y":
          delete_user(con)
        
        else:
            print("You don't want to delete")
    
    elif user_input == "8":
        del_id = input("Enter the id : ")
        if del_id.isnumeric():
            delete_user_by_id(con,del_id)

    elif user_input == "9":
         user_id = input("Enter the id : ")
         if user_id.isnumeric():
             column_name= input(
                 f"Enter the column you want to edit. Please make sure column is with us {COLUMNS}: "
             )
             if column_name is COLUMNS:
                 column_value = input (f"Enter the value of {column_name}: ")
                 update_user_by_id(con,user_id,column_name,column_value)

    else:
        exit()



main()
