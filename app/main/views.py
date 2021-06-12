from flask import render_template, request, redirect, url_for, abort
from flask_login import login_required, current_user
from .forms import PitchForm, CommentForm, CategoryForm
from . import main
from .. import db
from ..models import Pitch, Comments, PitchCategory, Votes


#categories
@main.route('/')
def index():
    """
        function that returns index page
    """

    all_category = PitchCategory.get_categories()
    all_pitches = Pitch.query.order_by('-id').all()
    print(all_pitches)

    title = 'The Pitch Manifesto'
    return render_template('index.html',
                           title=title,
                           categories=all_category,
                           all_pitches=all_pitches)


#new pitch
@main.route('/category/new-pitch/<int:id>', methods=['GET', 'POST'])
@login_required
def new_pitch(id):
    """
    Function to add new pitch
    """

    form = PitchForm()
    category = PitchCategory.query.filter_by(id=id).first()

    if category is None:
        abort(404)

    if form.validate_on_submit():
        content = form.content.data
        new_pitch = Pitch(content=content,
                          category_id=category.id,
                          user_id=current_user.id)
        new_pitch.save_pitch()
        return redirect(url_for('.category', id=category.id))

    return render_template('new_pitch.html',
                           pitch_form=form,
                           category=category)


@main.route('/categories/<int:id>')
def category(id):
    category = PitchCategory.query.get(id)
    if category is None:
        abort(404)

    pitches = Pitch.get_pitches(id)
    return render_template('category.html', pitches=pitches, category=category)


#create new category
@main.route('/add/category', methods=['GET', 'POST'])
@login_required
def new_category():
    """
        function to create a category
    """

    form = CategoryForm()

    if form.validate_on_submit():
        name = form.name.data
        new_category = PitchCategory(name=name)
        new_category.save_category()

        return redirect(url_for('.index'))

    title = 'New category'
    return render_template('new_category.html',
                           category_form=form,
                           title=title)


#view single pitch alongside its comments
@main.route('/view-pitch/<int:id>', methods=['GET', 'POST'])
@login_required
def view_pitch(id):
    """
    Function the returns a pitch for a comment to be added
    """
    all_category = PitchCategory.get_categories()
    pitches = Pitch.query.get(id)

    if pitches is None:
        abort(404)
    #
    comment = Comments.get_comments(id)
    count_likes = Votes.query.filter_by(pitches_id=id, vote=1).all()
    count_dislikes = Votes.query.filter_by(pitches_id=id, vote=2).all()
    return render_template('view-pitch.html',
                           pitches=pitches,
                           comment=comment,
                           count_likes=len(count_likes),
                           count_dislikes=len(count_dislikes),
                           category_id=id,
                           categories=all_category)


#comment
@main.route('/write_comment/<int:id>', methods=['GET', 'POST'])
@login_required
def post_comment(id):
    """ 
    Function to post comments 
    """

    form = CommentForm()
    title = 'post comment'
    pitches = Pitch.query.filter_by(id=id).first()

    if pitches is None:
        abort(404)

    if form.validate_on_submit():
        opinion = form.opinion.data
        new_comment = Comments(opinion=opinion,
                               user_id=current_user.id,
                               pitches_id=pitches.id)
        new_comment.save_comment()
        return redirect(url_for('.view_pitch', id=pitches.id))

    return render_template('post_comment.html', comment_form=form, title=title)

