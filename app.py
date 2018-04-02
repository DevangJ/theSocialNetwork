from flask import Flask, g, render_template, flash, redirect, url_for, abort
from flask_bcrypt import check_password_hash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
import forms
import models

DEBUG = True
PORT = 8000
HOST = '0.0.0.0'
THREADED = True

app = Flask(__name__)
app.secret_key = 'thisisareallylongkeythatnooneknows'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.anonymous_user = models.Anonymous


#Fetch User
@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None


#Save Current User
@app.before_request
def before_request():
    g.db = models.DATABASE
    g.db.connect()
    g.user = current_user


@app.after_request
def after_request(response):
    g.db.close()
    return response

# Register User
@app.route('/register', methods=('GET', 'POST'))
def register():
    form = forms.RegisterForm()
    if form.validate_on_submit():
        flash("Registration Successful", "success")
        models.User.create_user(username=form.username.data, email=form.email.data, password=form.password.data)
        return redirect(url_for('index'))
    return render_template('register.html', form=form)


#Login User
@app.route('/login', methods=('GET', 'POST'))
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            user = models.User.get(models.User.email == form.email.data)
        except models.DoesNotExist:
            flash("Your email or password doesn't match!", "error")
        else:
            if check_password_hash(user.password, form.password.data):
                login_user(user)
                flash("Logged in", "success")
                return redirect(url_for('index'))
            else:
                flash("Your email or password doesn't match!", "error")
    return render_template('login.html', form=form)


#Logout User
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You've been logged out! Come back soon!", "success")
    return redirect(url_for('index'))


#Make New Post
@app.route('/new_post', methods = ('GET', 'POST'))
@login_required
def post():
    form = forms.PostForm()
    if form.validate_on_submit():
        models.Post.create(user = g.user._get_current_object(),
                          content = form.content.data.strip())
        flash('Your Message has been posted!', 'Success')
        return redirect(url_for('index'))
    return render_template('post.html', form = form)


#Home Page
@app.route('/')
def index():
    stream = models.Post.select().limit(100)
    return render_template('stream.html', stream = stream)


#Displays Posts
@app.route('/stream')
@app.route('/stream/<username>')
def stream(username = None):
    template = 'stream.html'
    if username and username != current_user.username:
        try:
            user = models.User.select().where(models.User.username**username).get()
            stream = user.posts.limit(100)
        except models.DoesNotExist:
            abort(404)
        else:
            stream = user.posts.limit(100)
    else:
        stream = current_user.get_stream().limit(100)
        user = current_user
    if username:
        template = 'user_stream.html'
    return render_template(template, stream = stream, user = user)


#Follow A User
@app.route('/follow/<username>')
@login_required
def follow(username):
    try:
        to_user = models.User.get(models.User.username**username)
    except models.DoesNotExist:
        abort(404)
    else:
        try:
            models.Relationship.create(
                from_user = g.user._get_current_object(),
                to_user = to_user
            )
        except models.IntegrityError:
            pass
        else:
            flash("You are now following {}!".format(to_user.username), 'success')
    return redirect(url_for('stream', username = to_user.username))


#Unfollow A User
@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
    try:
        to_user = models.User.get(models.User.username**username)
    except models.DoesNotExist:
        abort(404)
    else:
        try:
            models.Relationship.get(
                from_user = g.user._get_current_object(),
                to_user = to_user
            ).delete_instance()
        except models.IntegrityError:
            pass
        else:
            flash("You unfollowed {}!".format(to_user.username), 'success')
    return redirect(url_for('stream', username = to_user.username))


'''
@app.route('/like/<username>')
@login_required
def like(username):
    try:
        to_post = models.Post.get(models.Post.post_id**post_id)
    except models.DoesNotExist:
        abort(404)
    else:
        try:
            models.Like.create(
                from_user = g.user._get_current_object(),
                to_post = to_post
            )
        except models.IntegrityError:
            pass
        else:
            flash("You Liked {}'s post!'!".format(to_post.user), 'success')
    return redirect(url_for('stream', username = to_post.user))
'''


#Display Single Post
@app.route('/post/<int:post_id>')
def view_post(post_id):
    posts = models.Post.select().where(models.Post.id == post_id)
    if posts.count() == 100:
        abort(404)
    return render_template('stream.html', stream = posts, use = 1)


#Handle 404 Errors
@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


#Main Function
if __name__ == '__main__':
    models.initialize()
    try:
        models.User.create_user(
            username='Devang J',
            email='devang.j1998@gmail.com',
            password='admin123',
            admin=True
        )
    except ValueError:
        pass
    app.run(debug=DEBUG, host=HOST, port=PORT, threaded=THREADED)
