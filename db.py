import mysql.connector
from flask_bcrypt import generate_password_hash, check_password_hash

#DB connections and calls
def connectDB(host='localhost', database='thesocialnetwork', user='root', password='1234'):
    return mysql.connector.connect(host=host, database=database, user=user, password=password)

def disconnectDB(conn):
    conn.close()

def executeDB(conn, sql, values):
    cursor = conn.cursor()
    cursor.execute(sql, values)
    conn.commit()

def queryDB(conn, sql):
    cursor = conn.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    cursor.close()
    return rows


#Register and Login
def register_user(username, password, email, dob, bio):
    c = connectDB()
    password = generate_password_hash(password)
    executeDB(c, "insert into members values(0, %s, %s, %s, %s, %s)", (username, password, email, dob, bio))
    disconnectDB(c)
    return True

def login_user(email, password):
    c = connectDB()
    result = queryDB(c, "select * from members where email ='"+email+"'")
    disconnectDB(c)
    if result:
        if check_password_hash(result[0][2], password):
            return result[0]
        else:
            return False
    else:
        return False

def update_member(user_id, username, email, dob, bio):
    c = connectDB()
    user_id = str(user_id)
    executeDB(c,"update members set username=%s, email=%s, bio=%s, dob=%s where user_id=%s",(username, email, bio, dob, user_id))
    disconnectDB(c)
    return True

def update_password(user_id, password):
    c = connectDB()
    user_id = str(user_id)
    password = generate_password_hash(password)
    executeDB(c,"update members set password=%s where user_id=%s",(password, user_id))
    disconnectDB(c)
    return True

#Posts Related
def add_post(user_id, article):
    c = connectDB()
    user_id = str(user_id)
    executeDB(c,"insert into posts values(0,"+user_id+",%s, now())",(article,))
    disconnectDB(c)
    return True

def delete_post(post_id):
    c = connectDB()
    post_id = str(post_id)
    executeDB(c,"delete from posts where post_id="+post_id,())
    flush_likes(post_id)
    disconnectDB(c)
    return True

def edit_post(article, post_id):
    c = connectDB()
    post_id = str(post_id)
    executeDB(c,"update posts set article='"+article+"' where post_id="+post_id,())
    disconnectDB(c)
    return True


def post_list():
    c = connectDB()
    result = queryDB(c,"select * from posts")
    disconnectDB(c)
    return result

def post_list_by_id(user_id):
    c = connectDB()
    user_id = str(user_id)
    result = queryDB(c,"select * from posts where user_id in (select to_id from follows where from_id="+user_id+")")
    disconnectDB(c)
    return result


def post_list_by_my_id(user_id):
    c = connectDB()
    user_id = str(user_id)
    result = queryDB(c,"select * from posts where user_id ="+user_id)
    disconnectDB(c)
    return result


def post_list_by_post_id(post_id):
    c = connectDB()
    post_id = str(post_id)
    result = queryDB(c,"select * from posts where post_id ="+post_id)
    disconnectDB(c)
    return result


#Like, Unlike and Like List
def like_post(user_id,post_id):
    c = connectDB()
    user_id, post_id = str(user_id), str(post_id)
    executeDB(c,"insert into likes values("+user_id+", "+post_id+")",())
    disconnectDB(c)
    return True

def unlike_post(user_id,post_id):
    c = connectDB()
    user_id, post_id = str(user_id), str(post_id)
    executeDB(c,"delete from likes where user_id="+user_id+" and post_id="+post_id,())
    disconnectDB(c)
    return True

def like_list_by_post_id(post_id):
    c = connectDB()
    post_id = str(post_id)
    result = queryDB(c,"select user_id from likes where post_id = "+post_id)
    result1 = [x[0] for x in result]
    disconnectDB(c)
    return result1


#Follow, Unfollow and Follower/Following List
def follow_user(from_id,to_id):
    c = connectDB()
    from_id, to_id = str(from_id), str(to_id)
    executeDB(c,"insert into follows values("+from_id+", "+to_id+")",())
    disconnectDB(c)
    return True

def unfollow_user(from_id,to_id):
    c = connectDB()
    from_id, to_id = str(from_id), str(to_id)
    executeDB(c,"delete from follows where from_id="+from_id+" and to_id="+to_id,())
    disconnectDB(c)
    return True

def follower_list(user_id):
    c = connectDB()
    user_id = str(user_id)
    result = queryDB(c,"select username from members where user_id in (select from_id from follows where to_id="+user_id+")")
    disconnectDB(c)
    return result

def following_list(user_id):
    c = connectDB()
    user_id = str(user_id)
    result = queryDB(c,"select username from members where user_id in (select to_id from follows where from_id="+user_id+")")
    result1 = [x[0] for x in result]
    disconnectDB(c)
    return result1

#members info
def member_info(user_id):
    c = connectDB()
    user_id = str(user_id)
    result = queryDB(c,"select * from members where user_id="+user_id)
    disconnectDB(c)
    return result

def username_fetch():
    c = connectDB()
    result = queryDB(c,"select username from members")
    disconnectDB(c)
    return result

def username_not_mine_fetch(username):
    c = connectDB()
    result = queryDB(c,"select username from members where username!='"+username+"'")
    result1 = [x[0] for x in result]
    disconnectDB(c)
    return result1

def username_fetch_by_id(user_id):
    c = connectDB()
    user_id = str(user_id)
    result = queryDB(c,"select username from members where user_id = "+user_id)
    result = result[0][0]
    disconnectDB(c)
    return result

def email_fetch():
    c = connectDB()
    result = queryDB(c,"select email from members")
    disconnectDB(c)
    return result

def email_not_mine_fetch(email):
    c = connectDB()
    result = queryDB(c,"select email from members where email!='"+email+"'")
    result1 = [x[0] for x in result]
    disconnectDB(c)
    return result1

def members_list():
    c = connectDB()
    result = queryDB(c,"select username, email, dob, bio from members")
    disconnectDB(c)
    return result

#Flush tables
def flush_posts(user_id):
    c = connectDB()
    user_id = str(user_id)
    executeDB(c,"delete from posts where user_id="+user_id,())
    disconnectDB(c)
    return True

def flush_follow(user_id):
    c = connectDB()
    user_id = str(user_id)
    executeDB(c,"delete from follows where from_id="+user_id+" or to_id="+user_id,())
    disconnectDB(c)
    return True

def flush_likes(post_id):
    c = connectDB()
    post_id = str(post_id)
    executeDB(c,"delete from likes where post_id="+post_id,())
    disconnectDB(c)
    return True

# members
#     user_id	int(11) Auto Increment
#     username	text
#     password	text
#     email	text
#     bio	text
#     dob	date

# likes
    # user_id	int(11)
    # post_id	int(11)

# Post
    # user_id	int(11)
    # post_id	int(11) Auto Increment
    # article	mediumtext
    # date_time	timestamp [CURRENT_TIMESTAMP]
# Follow
