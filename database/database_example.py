import database_lib as db



connection=db.create_connection("mydatabase.sqlite", verbose=True)

create_users_table = """
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL, 
    age INTEGER,
    gender TEXT,
    nationality TEXT
);
"""
db.execute_query(connection, create_users_table, verbose=True)

insert_users="""
INSERT INTO users (name, age, gender, nationality) VALUES
    ('James', 25, 'Male', 'USA'),
    ('Leila', 32, 'Female', 'France'),
    ('Brigitte', 35, 'Female', 'England');
"""

db.execute_query(connection, insert_users, verbose=True)

select_users = "SELECT * FROM users;"
columns,users = db.execute_read_query(connection, select_users, verbose=True)
print(columns)
for user in users:
    print(user) 

thename="James"
select_users_with_name = """
SELECT * FROM users WHERE name = '{}';""".format(thename)
# select_users_with_name = f"SELECT * fROM users WHERE name = '{thename}';"

column,users = db.execute_read_query(connection, select_users_with_name, verbose=True)
age=users[0][2]
print(age)
newage=age+1
update_user_age = """
UPDATE users SET age = {} WHERE name = '{}' and id=1
""".format(newage, thename)
db.execute_query(connection, update_user_age, verbose=True)

name_to_delete = 'Leila'    
delete_user = """
DELETE FROM users WHERE name = '{}';
""".format(name_to_delete)
db.execute_query(connection, delete_user, verbose=True)

