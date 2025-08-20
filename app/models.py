
import os
import pymysql
import pymysql.cgursors

conn = pymysql.connect(
    host=os.getenv("DB_HOST", "localhost"),
    user=os.getenv("DB_USER", "root"),
    password=os.getenv("DB_PASSWORD", "root"),
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
    tags = tags or []  # 
    cursor.execute(
        "INSERT INTO issues (user_id, title, content) VALUES (%s, %s, %s)",
        (user_id, title, content)
    )
    issue_id = cursor.lastrowid
    for i in tags:
        cursor.execute("INSERT INTO tags (issue_id, tag_name) VALUES (%s, %s)", (issue_id, i))
    conn.commit()


def get_userid(username):
    cursor.execute("select user_id from users where username=%s",(username,))
    return cursor.fetchone()

def get_issues(user_id):
    cursor.execute("SELECT issue_id, title, content, created_at FROM issues WHERE user_id = %s  ORDER BY created_at DESC, issue_id DESC", (user_id,))
    return cursor.fetchall()

# check
def get_tags_for_user(user_id):
    cursor.execute("SELECT DISTINCT tag_name FROM tags WHERE issue_id IN (SELECT issue_id FROM issues WHERE user_id = %s)", (user_id,))
    return [row[0] for row in cursor.fetchall()]

# check
def get_issues_by_tag_for_user(user_id, tag_name):
    cursor.execute("SELECT i.issue_id, i.title, i.content, i.created_at FROM issues i JOIN tags t ON i.issue_id = t.issue_id WHERE i.user_id = %s AND t.tag_name = %s ORDER BY i.created_at DESC, i.issue_id DESC", (user_id, tag_name))
    return cursor.fetchall()

# check
def get_issue_by_id(issue_id):
    cursor.execute("SELECT issue_id, title, content, created_at, user_id FROM issues WHERE issue_id = %s", (issue_id,))
    return cursor.fetchone()

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

def friendsr(user1,user2):
    cursor.execute("Insert into requests (user1,user2,status) values (%s,%s,%s)", (user1, user2,"pending"))
    conn.commit()
    pass

def friendsra(user1,user2):
    cursor.execute("update requests set status ='accepted' where (user1= %s and user2= %s)", (user1,user2))
    conn.commit()

def friendsch(user1,user2):
        cursor.execute("select * from requests where (user1= %s and user2 = %s) or (user1= %s and user2=%s)",(user1,user2,user2,user1))
        if (cursor.fetchone()):
            return (True)
        else:
            return(False)
        
def friendse(username):
    cursor.execute("""
        SELECT user1, user2
        FROM requests
        WHERE status='accepted' AND (user1=%s OR user2=%s)
    """, (username, username))
    rows = cursor.fetchall()
    friends = []
    for u1, u2 in rows:
        friend = u2 if u1 == username else u1
        friends.append(friend)
    return friends

def requests(username):
    cursor.execute("""
        SELECT user2
        FROM requests
        WHERE user1=%s AND status='pending'
    """, (username,))
    return [r[0] for r in cursor.fetchall()]

def requests_in(username):
    cursor.execute("""
        SELECT user1
        FROM requests
        WHERE user2=%s AND status='pending'
    """, (username,))
    return [r[0] for r in cursor.fetchall()]

def friends_decline(user1, user2):
    cursor.execute(
        "DELETE FROM requests WHERE user1=%s AND user2=%s AND status='pending'",
        (user1, user2),
    )
    conn.commit()

def friends_cancel(user1, user2):
    cursor.execute(
        "DELETE FROM requests WHERE user1=%s AND user2=%s AND status='pending'",
        (user1, user2),
    )
    conn.commit()

def friends_remove(user1, user2):
    cursor.execute(
        "DELETE FROM requests WHERE status='accepted' AND ((user1=%s AND user2=%s) OR (user1=%s AND user2=%s))",
        (user1, user2, user2, user1),
    )
    conn.commit()



def get_all_tags_global():
    cursor.execute("SELECT DISTINCT tag_name FROM tags ORDER BY tag_name")
    return [r[0] for r in cursor.fetchall()]

#check 
def search_recent_issues_global(q, limit=10):
    like = f"%{q}%"
    cursor.execute("""
        SELECT issue_id, title, content, created_at
        FROM issues
        WHERE title LIKE %s OR content LIKE %s
        ORDER BY created_at DESC, issue_id DESC
        LIMIT %s
    """, (like, like, limit))
    return cursor.fetchall()

def get_global_issues(limit=10):
    cursor.execute("""
        select issue_id, title, content, created_at
        FROM issues
        ORDER BY created_at DESC, issue_id DESC
        LIMIT %s
    """, (limit,))
    return cursor.fetchall()

def idkwhattoname( tag_name,limit=10):
    cursor.execute("SELECT i.issue_id, i.title, i.content, i.created_at FROM issues i JOIN tags t ON i.issue_id = t.issue_id WHERE t.tag_name = %s Limit %s", (tag_name , limit, ))
    return cursor.fetchall()

def getusername(user_id):
    cursor.execute("select username from users where user_id != %s",(user_id,))
    return cursor.fetchall()#replaced remove at last


def get_username_by_id(user_id):
    cursor.execute("SELECT username FROM users WHERE user_id=%s", (user_id,))
    row = cursor.fetchone()
    return row[0] if row else None

def search_users(query, exclude_username=None):
    like = f"%{query}%"
    if exclude_username:
        cursor.execute(
            "SELECT username FROM users WHERE username LIKE %s AND username != %s",
            (like, exclude_username),
        )
    else:
        cursor.execute("SELECT username FROM users WHERE username LIKE %s", (like,))
    return [r[0] for r in cursor.fetchall()]





