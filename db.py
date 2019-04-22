# import mysql.connector
import psycopg2
import os
from flask_bcrypt import generate_password_hash, check_password_hash


# DB connections and calls
# Connect To Database

# for mysql
# def connectDB(host='localhost', database='thesocialnetwork', user='root', password='1234'):
#     return mysql.connector.connect(host=host, database=database, user=user, password=password)

# for postgresql local
# def connectDB(host='localhost', database='thesocialnetwork', user='root', password='1234', port='5432'):
#   return psycopg2.connect("host="+host+" dbname="+database+" user="+user+" password="+password+" port="+port)

# for heroku postgresql
 DATABASE_URL = os.environ['DATABASE_URL']
 def connectDB():
     return psycopg2.connect(DATABASE_URL, sslmode='require')


# Disconnect From Database
def disconnectDB(conn):
    conn.close()


# Execute A Query
def executeDB(conn, sql, values):
    cursor = conn.cursor()
    cursor.execute(sql, values)
    conn.commit()
    return cursor.lastrowid


# Query The Database
def queryDB(conn, sql):
    cursor = conn.cursor()
    cursor.execute(sql)
    try:
        rows = cursor.fetchall()
    except:
        rows = []
    cursor.close()
    return rows


# Register and Login
# Register User
def register_user(username, password, email, dob, bio):
    c = connectDB()
    password = generate_password_hash(password)
    password = str(password, "utf-8")
    executeDB(c, "insert into members values(default, %s, %s, %s, %s, %s)", (username, password, email, dob, bio))
    disconnectDB(c)
    return True


# Login User
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


# Update Member
def update_member(user_id, username, email, dob, bio):
    c = connectDB()
    user_id = str(user_id)
    executeDB(c, "update members set username=%s, email=%s, bio=%s, dob=%s where user_id=%s", (username, email, bio, dob, user_id))
    disconnectDB(c)
    return True


# Update Password
def update_password(user_id, password):
    c = connectDB()
    user_id = str(user_id)
    password = generate_password_hash(password)
    password = str(password, "utf-8")
    executeDB(c, "update members set password=%s where user_id=%s", (password, user_id))
    disconnectDB(c)
    return True


# Delete Member
def delete_member(user_id):
    c = connectDB()
    user_id = str(user_id)
    executeDB(c, "delete from members where user_id="+user_id, ())
    flush_follow(user_id)
    flush_posts(user_id)
    flush_comments_for_user(user_id)
    disconnectDB(c)
    return True


# Posts Related
# Add Post
def add_post(user_id, article):
    c = connectDB()
    user_id = str(user_id)
    executeDB(c, "insert into posts values(default,"+user_id+",%s, now())", (article,))
    disconnectDB(c)
    return True


# Delete Post
def delete_post(post_id):
    c = connectDB()
    post_id = str(post_id)
    executeDB(c, "delete from posts where post_id="+post_id, ())
    flush_likes(post_id)
    flush_comments(post_id)
    disconnectDB(c)
    return True


# Edit Post
def edit_post(article, post_id):
    c = connectDB()
    post_id = str(post_id)
    executeDB(c, "update posts set article=%s where post_id="+post_id, (article,))
    disconnectDB(c)
    return True


# Post List
def post_list():
    c = connectDB()
    result = queryDB(c, "select * from posts")
    disconnectDB(c)
    return result


# Post list Of Followers
def post_list_by_id(user_id):
    c = connectDB()
    user_id = str(user_id)
    result = queryDB(c, "select * from posts where user_id in (select to_id from follows where from_id="+user_id+")")
    disconnectDB(c)
    return result


# Post List Of Current User ID
def post_list_by_my_id(user_id):
    c = connectDB()
    user_id = str(user_id)
    result = queryDB(c, "select * from posts where user_id ="+user_id)
    disconnectDB(c)
    return result


# Post List By Post ID
def post_list_by_post_id(post_id):
    c = connectDB()
    post_id = str(post_id)
    result = queryDB(c, "select * from posts where post_id ="+post_id)
    disconnectDB(c)
    return result


# Comments
# Add Comment
def add_comment(post_id, user_id, comment):
    c = connectDB()
    post_id = str(post_id)
    user_id = str(user_id)
    executeDB(c, "insert into comments values(default,"+post_id+","+user_id+",%s, now())", (comment,))
    disconnectDB(c)
    return True


# Comment List By Post ID
def comment_list_by_post_id(post_id):
    c = connectDB()
    post_id = str(post_id)
    result = queryDB(c, "select * from comments where post_id ="+post_id)
    disconnectDB(c)
    return result


# Delete comment
def delete_comment_by_comment_id(comment_id):
    c = connectDB()
    comment_id = str(comment_id)
    executeDB(c, "delete from comments where comment_id="+comment_id, ())
    disconnectDB(c)
    return True


# Like, Unlike and Like List
# Like Post
def like_post(user_id, post_id):
    c = connectDB()
    user_id, post_id = str(user_id), str(post_id)
    executeDB(c, "insert into likes values("+user_id+", "+post_id+")", ())
    disconnectDB(c)
    return True


# Unlike Post
def unlike_post(user_id, post_id):
    c = connectDB()
    user_id, post_id = str(user_id), str(post_id)
    executeDB(c, "delete from likes where user_id="+user_id+" and post_id="+post_id, ())
    disconnectDB(c)
    return True


# Like List
def like_list_by_post_id(post_id):
    c = connectDB()
    post_id = str(post_id)
    result = queryDB(c, "select user_id from likes where post_id = "+post_id)
    result1 = [x[0] for x in result]
    disconnectDB(c)
    return result1


# Follow, Unfollow and Follower/Following List
# Follow User
def follow_user(from_id, to_id):
    c = connectDB()
    from_id, to_id = str(from_id), str(to_id)
    executeDB(c, "insert into follows values("+from_id+", "+to_id+")", ())
    disconnectDB(c)
    return True


# Unfollow User
def unfollow_user(from_id, to_id):
    c = connectDB()
    from_id, to_id = str(from_id), str(to_id)
    executeDB(c, "delete from follows where from_id="+from_id+" and to_id="+to_id, ())
    disconnectDB(c)
    return True


# Follower List
def follower_list(user_id):
    c = connectDB()
    user_id = str(user_id)
    result = queryDB(c, "select username from members where user_id in (select from_id from follows where to_id="+user_id+")")
    result1 = [x[0] for x in result]
    disconnectDB(c)
    return result1


# Following List
def following_list(user_id):
    c = connectDB()
    user_id = str(user_id)
    result = queryDB(c, "select username from members where user_id in (select to_id from follows where from_id="+user_id+")")
    result1 = [x[0] for x in result]
    disconnectDB(c)
    return result1


# Members info
def member_info(user_id):
    c = connectDB()
    user_id = str(user_id)
    result = queryDB(c, "select * from members where user_id="+user_id)
    disconnectDB(c)
    return result


# Fetch All Username
def username_fetch():
    c = connectDB()
    result = queryDB(c, "select username from members")
    result1 = [x[0] for x in result]
    disconnectDB(c)
    return result1


# Fetch Username Except Input
def username_not_mine_fetch(username):
    c = connectDB()
    result = queryDB(c, "select username from members where username!='"+username+"'")
    result1 = [x[0] for x in result]
    disconnectDB(c)
    return result1


# Fetch Username by User ID
def username_fetch_by_id(user_id):
    c = connectDB()
    user_id = str(user_id)
    result = queryDB(c, "select username from members where user_id = "+user_id)
    result = result[0][0]
    disconnectDB(c)
    return result


# Fetch User ID By Username
def user_id_fetch_by_name(username):
    c = connectDB()
    username = str(username)
    result = queryDB(c, "select user_id from members where username = '"+username+"'")
    result = result[0][0]
    disconnectDB(c)
    return result


# Fetch All Emails
def email_fetch():
    c = connectDB()
    result = queryDB(c, "select email from members")
    disconnectDB(c)
    return result


# Fetch All Emails Except Input
def email_not_mine_fetch(email):
    c = connectDB()
    result = queryDB(c, "select email from members where email!='"+email+"'")
    result1 = [x[0] for x in result]
    disconnectDB(c)
    return result1


# List Members
def members_list():
    c = connectDB()
    result = queryDB(c, "select username, email, dob, bio from members")
    disconnectDB(c)
    return result


# Flush tables
# Flush Posts
def flush_posts(user_id):
    c = connectDB()
    user_id = str(user_id)
    result = post_list_by_my_id(user_id)
    post_list = [x[0] for x in result]
    for post in post_list:
        flush_likes(post)
        flush_comments(post)
    executeDB(c, "delete from posts where user_id="+user_id, ())
    disconnectDB(c)
    return True


# Flush Follows
def flush_follow(user_id):
    c = connectDB()
    user_id = str(user_id)
    executeDB(c, "delete from follows where from_id="+user_id+" or to_id="+user_id, ())
    disconnectDB(c)
    return True


# Flush Likes
def flush_likes(post_id):
    c = connectDB()
    post_id = str(post_id)
    executeDB(c, "delete from likes where post_id="+post_id, ())
    disconnectDB(c)
    return True


# Flush Comments
def flush_comments(post_id):
    c = connectDB()
    post_id = str(post_id)
    executeDB(c, "delete from comments where post_id="+post_id, ())
    disconnectDB(c)
    return True


def flush_comments_for_user(user_id):
    c = connectDB()
    user_id = str(user_id)
    executeDB(c, "delete from comments where user_id="+user_id, ())
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
    # timestamp	timestamp [CURRENT_TIMESTAMP]
# Follow
    # from_id   int(11)
    # to_id     int(11)
# Comments
    # comment_id    int(11) Auto Increment
    # post_id       int(11)
    # user_id       int(11)
    # comment_text  mediumtext
    # timestamp     timestamp [CURRENT_TIMESTAMP]
