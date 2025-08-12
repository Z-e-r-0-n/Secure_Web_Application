# All DB queries will go here
# Example placeholders:
cursor=pymysql.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER", "root"),
        password=os.getenv("DB_PASSWORD", ""),  # keep this name since you used it
        database=os.getenv("DB_NAME", "secure_issue_tracker"),
        cursorclass=pymysql.cursors.DictCursor,
        autocommit=False,)
cur=cursor.cursor()
def create_user(username, password_hash, email, first_name, last_name):
    cursor.execute(
        "INSERT INTO users (username, password_hash, email, first_name, last_name) VALUES (%s, %s, %s, %s, %s)",
        (username, password_hash, email, first_name, last_name)
    ) 
    pass

def check_login(username, password_hash):
    cursor.execute(
        "SELECT * FROM users WHERE username = %s AND password_hash = %s",
        (username, password_hash)
    )
    list = cursor.fetchone()
    user=list(0)
    pas= list(1)
    if user==username and pas== password_hash:
        return True
    pass

def create_issue(user_id, title, content,tags):
    cursor.execute(
        "INSERT INTO issues (user_id, title, content,) VALUES (%s, %s, %s)",
        (user_id, title, content))
    cursor.commit()
    cursor.execute("select issue_id from issues where user_id = %s and title = %s", (user_id, title))
    issue_id = cursor.fetchone()['issue_id']
    for i in tags:
        cursor.execute("insert into tags (issue_id, tag_name) values (%s, %s)", (issue_id, tags))
    pass

def get_issues(user_id):
    cursor.execute("SELECT * FROM issues where user_id = %s", (user_id,))
    return cursor.fecthall()
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
    pass

def get_comments(issue_id):
    cursor.execute("SELECT * FROM comments WHERE issue_id = %s", (issue_id,))
    return cursor.fetchall()
    pass

def get_user_issues(user_id):
    cursor.execute("SELECT * FROM issues WHERE user_id = %s", (user_id,))
    return cursor.fetchall()
    pass

