
import os
import pymysql
import pymysql.cursors

conn = pymysql.connect(
    host=os.getenv("DB_HOST", "localhost"),
    user=os.getenv("DB_USER", "root"),
    password=os.getenv("DB_PASSWORD", ""),
    database=os.getenv("DB_NAME", "secure_issue_tracker"),              # IMPORTANT: no DictCursor -> fetchone() returns a tuple (matches your code)
    autocommit=False,
)
cursor = conn.cursor()  

def create_user(username, password_hash, email, first_name, last_name):
    cursor.execute(
        "INSERT INTO users (username, password_hash, email, first_name, last_name) VALUES (%s, %s, %s, %s, %s)",
        (username, password_hash, email, first_name, last_name)
    )
    conn.commit()
    pass

def check_login(username, password_hash):
    cursor.execute(
        "SELECT username, password_hash FROM users WHERE username=%s AND password_hash=%s LIMIT 1",
        (username, password_hash)
    )
    row = cursor.fetchone()          
    if not row:
        return False
    user = row[0]
    pas  = row[1]
    return (user == username and pas == password_hash)


def create_issue(user_id, title, content, tags):
    cursor.execute(
        "INSERT INTO issues (user_id, title, content) VALUES (%s, %s, %s)",
        (user_id, title, content)
    )
    conn.commit()  
    cursor.execute("SELECT issue_id FROM issues WHERE user_id = %s AND title = %s", (user_id, title))
    issue_id = cursor.fetchone()[0]  
    for i in tags:
        cursor.execute("INSERT INTO tags (issue_id, tag_name) VALUES (%s, %s)", (issue_id, i))
    conn.commit()
    pass

def get_issues(user_id):
    cursor.execute("SELECT title,content,created_at FROM issues WHERE user_id in (select user_id from users where username = %s)", (user_id,))
    return cursor.fetchall()
    pass

def get_issues_by_tag(tag_name):
    cursor.execute("SELECT * FROM issues WHERE issue_id IN (SELECT issue_id FROM tags WHERE tag_name = %s)", (tag_name,))
    return cursor.fetchall()
    pass

def add_comment(issue_id, user_id, content):
    cursor.execute(
        "INSERT INTO comments (issue_id, user_id, content) VALUES (%s, %s, %s)",
        (issue_id, user_id, content)
    )
    conn.commit()
    pass

def get_comments(issue_id):
    cursor.execute("SELECT * FROM comments WHERE issue_id = %s", (issue_id,))
    return cursor.fetchall()
    pass

def get_user_issues(user_id):
    cursor.execute("SELECT user FROM issues WHERE user_id = %s", (user_id,))
    return cursor.fetchall()
    pass

def insert_message(user1,user2,content):
    cursor.execute("INSERT INTO messages (user1, user2, content) VALUES (%s, %s, %s)", (user1, user2, content))
    conn.commit()
    pass

def get_messages(user1, user2):
    cursor.execute("SELECT user1,user2,content FROM messages WHERE (user1 = %s AND user2 = %s) OR (user1 = %s AND user2 = %s) ORDER BY timestamp desc limit 10", (user1, user2, user2, user1))
    return cursor.fetchall()
    pass

def get_profile(user_id):
    cursor.execute("SELECT username, email, first_name, last_name FROM users WHERE user_id = %s", (user_id,))
    return cursor.fetchone()
    pass

def friendsr(user1,user2):
    cursor.execute("Insert into requests (user1,user2,status) values (%s,%s,%s)", (user1, user2,"pending"))
    conn.commit()
    pass

def frindsra(user1,user2):
    cursor.execute("update requests set status ='accepted' where (user1= %s and user2= %s)", (user1,user2))
    conn.commit()

def friendsch(user1,user2):
        cursor.execute("select * from requests where (user1= %s and user2 = %s) or (user1= %s and user2=%s)",(user1,user2,user2,user1))
        if (cursor.fetchone()):
            return (True)
        else:
            return(False)




