
from flask import render_template, url_for, flash, redirect, request, abort, Blueprint
from jobmanager import db
from jobmanager.posts.forms import PostForm
from jobmanager.models import Post
from flask_login import current_user, login_required

post_bp = Blueprint('posts', __name__)


@post_bp.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()

    if form.validate_on_submit():
        cur_post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(cur_post)
        db.session.commit()
        flash('Your post has been created', 'success')
        return redirect(url_for('main.home'))

    return render_template('create_post.html', title='New posts',
                           form=form, legend='New posts'
                           )


@post_bp.route("/post/<int:post_id>")
def view_post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@post_bp.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('The post has been updated!', 'success')
        return redirect(url_for('posts.view_post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update posts',
                           form=form, legend='Update posts'
                           )

@post_bp.route("/post/<int:post_id>/delete", methods=['GET','POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('The post has been deleted!', 'success')
    return redirect(url_for('main.home'))
