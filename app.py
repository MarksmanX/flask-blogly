"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session
from models import db, connect_db, User, Post
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'OHSOsecrettt'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

connect_db(app)

with app.app_context():
    db.create_all()


@app.route('/')
def redirect_to_users():
   return redirect('/users')


@app.route('/users')
def list_users():
    """Shows list all users in db."""

    users = User.query.all()
    return render_template('list.html', users=users)


@app.route('/users/new')
def show_add_user_form():
    """Displays the form to create a new user."""

    return render_template('form.html')


@app.route('/users/new', methods=['POST'])
def create_user():
    """Creates a new user."""

    first = request.form["first_name"]
    last = request.form["last_name"]
    image = request.form["image_url"] 
    

    new_user = User(first_name=first, last_name=last, image_url=image)
    db.session.add(new_user)
    db.session.commit()

    return redirect(f"/users/{new_user.id}")


@app.route('/users/<int:user_id>')
def show_user(user_id):
    """Show details about a single user."""

    # posts = user.post
    user = User.query.get_or_404(user_id)
    return render_template("details.html", user=user)


@app.route('/users/<int:user_id>/edit')
def show_edit_form(user_id):
    """Shows editable info about a single user."""

    user = User.query.get_or_404(user_id)
    return render_template("edit.html", user=user)


@app.route('/users/<int:user_id>/edit', methods=['POST'])
def edit_user(user_id):
    """Saves the information about the user to the database and returns to homepage."""

    user = User.query.get_or_404(user_id)
    user.first_name = request.form["first_name"]
    user.last_name = request.form["last_name"]
    user.image_url = request.form["image_url"]

    db.session.add(user)
    db.session.commit()
    flash(f"User {user.full_name} edited.")

    return redirect('/users')


@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    """Deletes the user."""

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    flash(f"User {user.full_name} deleted.")
    
    return redirect('/users')

##############################################################
# Posts route


@app.route('/users/<int:user_id>/posts/new')
def show_post_form(user_id):
    """Shows form for making a post to user."""

    user = User.query.get_or_404(user_id)
    return render_template("posts/new.html", user=user)


@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def create_post(user_id):
    """Creates a post for the user."""

    user = User.query.get_or_404(user_id)

    new_post = Post(title=request.form['title'], 
                    content=request.form['content'],
                    user=user)
    db.session.add(new_post)
    db.session.commit()
    flash(f"Post '{new_post.title}' added.")

    return redirect(f"/users/{user_id}")


@app.route('/posts/<int:post_id>')
def posts_show(post_id):
    """Show a page with infor on a specific post."""

    post = Post.query.get_or_404(post_id)
    return render_template('posts/show.html', post=post)


@app.route('/posts/<int:post_id>/edit')
def posts_edit(post_id):
    """Show a form to edit an existing post."""

    post = Post.query.get_or_404(post_id)
    return render_template('posts/edit.html', post=post)


# @app.route()

if __name__ == '__main__':
    app.run(debug=True)