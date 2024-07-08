"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session
from models import db, connect_db, User, Post, Tag, PostTag
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
    return render_template('users/list.html', users=users)


@app.route('/users/new')
def show_add_user_form():
    """Displays the form to create a new user."""

    return render_template('users/new.html')


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
    return render_template("users/details.html", user=user)


@app.route('/users/<int:user_id>/edit')
def show_edit_form(user_id):
    """Shows editable info about a single user."""

    user = User.query.get_or_404(user_id)
    return render_template("users/edit.html", user=user)


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
    tags = Tag.query.all()
    return render_template("posts/new.html", user=user, tags=tags)


@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def create_post(user_id):
    """Creates a post for the user."""

    user = User.query.get_or_404(user_id)
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    new_post = Post(title=request.form['title'], 
                    content=request.form['content'],
                    user=user,
                    tags=tags)
    
    db.session.add(new_post)
    db.session.commit()
    flash(f"Post '{new_post.title}' added.")

    return redirect(f"/users/{user_id}")


@app.route('/posts/<int:post_id>')
def posts_show(post_id):
    """Show a page with infor on a specific post."""

    post = Post.query.get_or_404(post_id)
    return render_template('posts/details.html', post=post)


@app.route('/posts/<int:post_id>/edit')
def show_post_edit_form(post_id):
    """Show a form to edit an existing post."""

    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    return render_template('posts/edit.html', post=post, tags=tags)


@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def saves_post_edit(post_id):
    """Saves the edits made to the post."""

    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']
    tag_ids = [int(num) for num in request.form.getlist("tags")]
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()
    
    db.session.add(post)
    db.session.commit()

    return redirect(f'/posts/{post_id}')


@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    """Deletes the post."""

    post = Post.query.get_or_404(post_id)
    user_id = post.user_code
    db.session.delete(post)
    db.session.commit()
    flash(f"{post.title} has been deleted")

    return redirect(f'/users/{user_id}')


########################################################################################################################### Routes for Tags


@app.route('/tags')
def show_tags():
    """List all tags with links to the details on each tag."""

    tags = Tag.query.all()
    return render_template('tags/list.html', tags=tags)


@app.route('/tags/<int:tag_id>')
def show_tag_details(tag_id):
    """Shows all posts connected to tag and links to edit or delete tag."""

    tag = Tag.query.get_or_404(tag_id)

    return render_template('tags/details.html', tag=tag)


@app.route('/tags/new')
def show_add_tag_form():
    """Shows the form to add a new tag."""

    posts = Post.query.all()
    return render_template('tags/new.html', posts=posts)


@app.route('/tags/new', methods=['POST'])
def create_tag():
    """Creates a new tag using the information in the form."""

    tag = Tag(name=request.form['name'])
    post_ids = [int(num) for num in request.form.getlist("posts")]
    tag.posts = Post.query.filter(Post.id.in_(post_ids)).all()
    db.session.add(tag)
    db.session.commit()

    return redirect('/tags')


@app.route('/tags/<int:tag_id>/edit')
def show_edit_tag_form(tag_id):
    """Shows the form to edit a tag."""

    tag = Tag.query.get_or_404(tag_id)
    posts = Post.query.all()
    return render_template('tags/edit.html', tag=tag, posts=posts)


@app.route('/tags/<int:tag_id>/edit', methods=['POST'])
def save_edit(tag_id):
    """Saves the edits made to the tag and returns to tag details."""

    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['name']
    post_ids = [int(num) for num in request.form.getlist("posts")]
    tag.posts = Post.query.filter(Post.id.in_(post_ids)).all()
    
    db.session.add(tag)
    db.session.commit()
    flash(f"Tag {tag.name} edited.")

    return redirect(f'/tags/{tag_id}')


@app.route('/tags/<int:tag_id>/delete', methods=['POST'])
def delete_tag(tag_id):
    """Deletes the tag."""

    tag = Tag.query.get_or_404(tag_id)
    db.session.delete(tag)
    db.session.commit()
    flash(f"Tag {tag.name} deleted.")

    return redirect('/tags')

# if __name__ == '__main__':
#     app.run(debug=True)