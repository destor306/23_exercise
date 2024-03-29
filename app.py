from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag

app = Flask(__name__)

# order matter, this comes first
# this connects to database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///users_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "This is demo"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
deubg = DebugToolbarExtension(app)

connect_db(app)


@app.route('/')
def root():
    """Show home page"""
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template('home.html', posts=posts)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html')


@app.route('/users')
def list_users():
    """Shows list of all pets in db"""
    users = User.query.all()
    return render_template('list.html', users=users)


@app.route('/users/new')
def add_user_form():
    """Show form to add user"""
    return render_template('add_user.html')


@app.route('/users/new', methods=["POST"])
def create_user():
    """Create User and retriece query"""
    firstname = request.form['first_name']
    lastname = request.form['last_name']
    imgurl = request.form['imageurl']
    if not imgurl:
        imgurl = 'Ace.jpg'
    newUser = User(first_name=firstname, last_name=lastname, image_url=imgurl)
    db.session.add(newUser)
    db.session.commit()
    flash(f"User {newUser.full_name} added.")
    return redirect('/users')

# "/users/{{ user.id }}


@app.route('/users/<int:user_id>')
def show_profile(user_id):
    """Show profile of a user"""
    user = User.query.get_or_404(user_id)
    return render_template('profile.html', user=user)

# formaction="/users/{{ user.id }}/edit"


@app.route('/users/<int:user_id>/edit')
def edit_page(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('edit.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=["POST"])
def edit_user(user_id):
    user = User.query.get_or_404(user_id)
    user.first_name = request.form['first_name']
    user.last_name = request.form['last_name']
    user.image_url = request.form['image_url']
    db.session.add(user)
    db.session.commit()
    flash(f"User {user.full_name} edited")
    return redirect('/users')


@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    flash(f"User {user.full_name} deleted")
    db.session.delete(user)
    db.session.commit()

    return redirect('/users')


@app.route('/users/<int:user_id>/posts/new')
def add_post(user_id):
    """Show form to add a post for that user"""
    user = User.query.get_or_404(user_id)
    tags = Tag.query.all()

    return render_template('add_post.html',  user=user, tags=tags)


@app.route('/users/<int:user_id>/posts/new', methods=["POST"])
def handle_post(user_id):
    """Handle add form; add post and redirect to the user detail page"""
    user = User.query.get_or_404(user_id)
    title = request.form['title']
    post_content = request.form['post_content']
    tag_ids = [int(id) for id in request.form.getlist("tags")]
    tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    # Get the current timestamp

    new_post = Post(title=title, content=post_content,
                    user_id=user.id, tags=tags)
    db.session.add(new_post)
    db.session.commit()
    flash(f"Post {new_post.title} added")
    return redirect(f'/users/{user_id}')


@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """Show a post. Show buttons to edit and delete the post"""
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', post=post)


@app.route('/posts/<int:post_id>/edit')
def edit_post_page(post_id):
    """Show form to edit a post, and to cancel (back to user page)"""
    post = Post.query.get_or_404(post_id)
    tags = Tag.query.all()
    return render_template('edit_post.html', post=post, tags=tags)


@app.route('/posts/<int:post_id>/edit', methods=["POST"])
def handle_edit_page(post_id):
    """Handle editing of a post. Redirect back to the post view"""
    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['post_content']

    tags_ids = [int(id) for id in request.form.getlist('tags')]
    tags = Tag.query.filter(Tag.id.in_(tags_ids)).all()
    post.tags = tags
    db.session.add(post)
    db.session.commit()
    flash(f"Post {post.title} edited")

    return redirect(f'/posts/{post_id}')


@app.route('/posts/<int:post_id>/delete', methods=["POST"])
def delete_post(post_id):
    """Delete the post"""
    post = Post.query.get_or_404(post_id)
    flash(f"Post {post.title} deleted")

    db.session.delete(post)
    db.session.commit()
    return redirect(f'/users/{post.user_id}')


# post tag, and Tag

@app.route("/tags")
def show_tags():
    """list all tags, with links to the tag detail page"""
    tags = Tag.query.all()
    return render_template('tagslist.html', tags=tags)


@app.route("/tags/<tag_id>")
def show_tag(tag_id):
    """show detail about a tag, have links to edit form and delete"""
    tag = Tag.query.get_or_404(tag_id)

    return render_template('tag.html', tag=tag)


@app.route("/tags/new")
def add_tag():
    """Shows a form to add a new tag"""
    return render_template('add_tag.html')


@app.route("/tags/new", methods=["POST"])
def post_tag():
    """Process add form, add tag, and redirect to tag list"""
    name = request.form["name"]
    newTag = Tag(name=name)
    db.session.add(newTag)
    db.session.commit()
    flash(f"Tag {newTag.name} added.")
    return redirect('/tags')


@app.route("/tags/<tag_id>/edit")
def edit_tag_form(tag_id):
    """Show edit form for a tag"""
    tag = Tag.query.get_or_404(tag_id)
    return render_template('edit_tag.html', tag=tag)


@app.route("/tags/<tag_id>/edit", methods=["POST"])
def edit_tag(tag_id):
    """Process edit form, edit tag, and redirect to the tags list"""
    new_name = request.form["name"]
    tag = Tag.query.get_or_404(tag_id)
    tag.name = new_name
    db.session.add(tag)
    db.session.commit()
    flash(f"Tag {tag.id} edited")
    return redirect('/tags')


@app.route("/tags/<tag_id>/delete", methods=["POST"])
def delete_tag(tag_id):
    """Delete a tag"""
    tag = Tag.query.get_or_404(tag_id)
    flash(f"Tag {tag.id} deleted")

    db.session.delete(tag)
    db.session.commit()
    return redirect('/tags')
