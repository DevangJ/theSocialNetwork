from flask import Flask, render_template, flash, redirect, url_for, abort, session, request
from flask_bcrypt import check_password_hash
import forms
import db
from flask_wtf.csrf import CSRFProtect
DEBUG = True
PORT = 8000
HOST = '0.0.0.0'
THREADED = True

app = Flask(__name__)
app.secret_key = 'thisisareallylongkeythatnooneknows'
csrf = CSRFProtect(app)


# Home Page
@app.route('/')
def index():
    if session.get('login'):
        user = db.members_list()
        stream = db.post_list()[:100]
        return render_template('stream.html', stream=stream, user=user)
    else:
        return redirect(url_for('login'))


# Register User
@app.route('/register', methods=('GET', 'POST'))
def register():
    form = forms.RegisterForm()
    if form.validate_on_submit():
        db.register_user(form.username.data, form.password.data, form.email.data, form.dob.data, 'Tell us a bit about yourself')
        flash("Registration Successful", "success")
        return redirect(url_for('index'))
    return render_template('register.html', form=form)


# Login User
@app.route('/login', methods=('GET', 'POST'))
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        result = db.login_user(form.email.data, form.password.data)
        if result:
            session['login'] = True
            session['user_id'] = result[0]
            session['username'] = result[1]
            session['email'] = result[3]
            session['dob'] = result[4].strftime('%d-%m-%y')
            flash('Logged in', 'success')
            return redirect(url_for('index'))
        else:
            flash("Your email or password doesn't match!", "error")
    return render_template('login.html', form=form)


# Logout User
@app.route('/logout')
def logout():
    if session['login']:
        session['login'] = False
        session['user_id'] = 0
        session['username'] = ''
        session['email'] = ''
        session['dob'] = ''
        flash("You've been logged out! Come back soon!", "success")
        return redirect(url_for('index'))


# Make New Post
@app.route('/new_post', methods=('GET', 'POST'))
def post():
    if session['login']:
        form = forms.PostForm()
        if form.validate_on_submit():
            db.add_post(user_id=str(session['user_id']), article=form.content.data.strip())
            flash('Your Message has been posted!', 'success')
            return redirect(url_for('index'))
        return render_template('post.html', form=form)


# Delete Post
@app.route('/delete/<post_id>')
def delete_clicked_post(post_id):
    if session['login']:
        db.delete_post(post_id)
        return redirect(request.referrer)


# Edit Post
@app.route('/edit/<int:post_id>', methods=('GET', 'POST'))
def edit_clicked_post(post_id):
    if session['login']:
        form = forms.PostForm(content=db.post_list_by_post_id(post_id)[0][2])
        if form.validate_on_submit():
            db.edit_post(post_id=post_id, article=form.content.data.strip())
            flash('Your Post has been edited!', 'success')
            return redirect(url_for('index'))
        return render_template('post.html', form=form)


# Display Single Post
@app.route('/post/<int:post_id>')
def view_post(post_id):
    posts = db.post_list_by_post_id(post_id)
    if len(posts) == 100:
        abort(404)
    return render_template('stream.html', stream=posts, use=1)


# Displays Posts
@app.route('/stream')
@app.route('/stream/<int:user_id>')
def stream(user_id=None):
    template = 'stream.html'
    if user_id and user_id != session['user_id']:
        user = db.member_info(str(user_id))
        stream = db.post_list_by_my_id(user_id)[:100]
    else:
        user = db.member_info(str(session['user_id']))
        stream = db.post_list_by_id(str(session['user_id']))[:100]
    if user_id:
        template = 'user_stream.html'
    return render_template(template, stream=stream, user=user)


# Follow A User
@app.route('/follow/<user_id>')
def follow(user_id):
    if session['login']:
        try:
            to_user = db.member_info(user_id)
        except to_user is False:
            abort(404)
        else:
            db.follow_user(session['user_id'], to_user[0][0])
            flash("You are now following {}!".format(to_user[0][1]), 'success')
        return redirect(request.referrer)


# Unfollow A User
@app.route('/unfollow/<user_id>')
def unfollow(user_id):
    if session['login']:
        try:
            to_user = db.member_info(user_id)
        except to_user is False:
            abort(404)
        else:
            db.unfollow_user(session['user_id'], to_user[0][0])
            flash("You unfollowed {}!".format(to_user[0][1]), 'success')
        return redirect(request.referrer)


# Like Post
@app.route('/like/<post_id>')
def like(post_id):
    if session['login']:
        try:
            to_post = db.post_list_by_post_id(post_id)
        except to_post is False:
            abort(404)
        else:
            db.like_post(session['user_id'], to_post[0][0])
        return redirect(request.referrer)


# Unlike Post
@app.route('/unlike/<post_id>')
def unlike(post_id):
    if session['login']:
        if session['login']:
            try:
                to_post = db.post_list_by_post_id(post_id)
            except to_post is False:
                abort(404)
            else:
                db.unlike_post(session['user_id'], to_post[0][0])
            return redirect(request.referrer)


# Show Profile
@app.route('/profile/<user_id>')
def profile(user_id):
    user = db.member_info(user_id)
    return render_template('profile.html', user=user)


# Settings
@app.route('/settings')
def settings():
    return render_template('settings.html')


# Edit Profile
@app.route('/settings/profile_edit', methods=('GET', 'POST'))
def settings_profile_edit():
    if session['login']:
        user = db.member_info(session['user_id'])
        form = forms.ProfileForm(x=user[0][0], username=user[0][1], email=user[0][3], dob=user[0][4], bio=user[0][5])
        if form.validate_on_submit():
            if (form.username.data in db.username_not_mine_fetch(session['username'])):
                flash("Username is already in use!", "error")
            elif (form.email.data in db.email_not_mine_fetch(session['email'])):
                flash("Email is already in use!", "error")
            else:
                result = db.update_member(session['user_id'], form.username.data, form.email.data, form.dob.data, form.bio.data)
                if result:
                    session['username'] = form.username.data
                    session['email'] = form.email.data
                    session['dob'] = form.dob.data
                    flash('Edited', 'success')
                    return redirect(url_for('settings'))
        return render_template('profile_edit.html', form=form)


# Set New Password
@app.route('/settings/new_password', methods=('GET', 'POST'))
def settings_new_password():
    if session['login']:
        form = forms.PasswordForm()
        user = db.member_info(session['user_id'])
        if form.validate_on_submit():
            if check_password_hash(user[0][2], form.currentpassword.data):
                db.update_password(user[0][0], form.newpassword.data)
                flash('New password set', 'success')
                return redirect(url_for('settings'))
            else:
                flash("Incorrect Password!", "error")
        return render_template('password_edit.html', form=form)


# Delete Account
@app.route('/settings/delete_account', methods=('GET', 'POST'))
def settings_delete_account():
    if session['login']:
        form = forms.DeleteForm()
        user = db.member_info(session['user_id'])
        if form.validate_on_submit():
            if check_password_hash(user[0][2], form.password.data):
                db.delete_member(user[0][0])
                flash('Account Deleted', 'success')
                logout()
                return redirect(url_for('index'))
            else:
                flash("Incorrect Password!", "error")
        return render_template('delete_account.html', form=form)


# Display Members
@app.route('/stream_member')
def stream_member():
    stream = db.username_fetch()
    return render_template('stream_members.html', stream=stream)


# Following List
@app.route('/stream_member/following')
def stream_member_following():
    stream = db.following_list(session['user_id'])
    return render_template('stream_members.html', stream=stream)


# Follower List
@app.route('/stream_member/follower')
def stream_member_follower():
    stream = db.follower_list(session['user_id'])
    return render_template('stream_members.html', stream=stream)


# Handle 404 Errors
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


# Global function declarations
app.jinja_env.globals.update(username_fetch_by_id=db.username_fetch_by_id)
app.jinja_env.globals.update(following_list=db.following_list)
app.jinja_env.globals.update(follower_list=db.follower_list)
app.jinja_env.globals.update(post_list_by_id=db.post_list_by_id)
app.jinja_env.globals.update(like_list_by_post_id=db.like_list_by_post_id)
app.jinja_env.globals.update(post_list_by_my_id=db.post_list_by_my_id)
app.jinja_env.globals.update(user_id_fetch_by_name=db.user_id_fetch_by_name)


# Main Function
if __name__ == '__main__':
    app.run(debug=DEBUG, host=HOST, port=PORT, threaded=THREADED)
