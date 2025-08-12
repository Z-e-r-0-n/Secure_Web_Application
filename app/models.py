
import os
import pymysql
import pymysql.cursors

# make "cursor" the REAL cursor (so your functions keep working)
conn = pymysql.connect(
    host=os.getenv("DB_HOST", "localhost"),
    user=os.getenv("DB_USER", "root"),
    password=os.getenv("DB_PASSWORD", ""),
    database=os.getenv("DB_NAME", "secure_issue_tracker"),
    # IMPORTANT: no DictCursor -> fetchone() returns a tuple (matches your code)
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
    conn.commit()  # fix: commit on the connection
    cursor.execute("SELECT issue_id FROM issues WHERE user_id = %s AND title = %s", (user_id, title))
    issue_id = cursor.fetchone()[0]  # tuple fetch
    for i in tags:
        cursor.execute("INSERT INTO tags (issue_id, tag_name) VALUES (%s, %s)", (issue_id, i))
    conn.commit()
    pass

def get_issues(user_id):
    cursor.execute("SELECT * FROM issues WHERE user_id = %s", (user_id,))
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
    cursor.execute("SELECT * FROM issues WHERE user_id = %s", (user_id,))
    return cursor.fetchall()
    pass
