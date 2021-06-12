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

    title = 'Pitches'
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


