from flask import render_template, request, redirect, url_for, abort
from flask_login import login_required, current_user
from wtforms import form
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
    all_pitches = Pitch.query.order_by('id').all()
    print(all_pitches)

    title = 'The Pitch Manifesto'
    return render_template('index.html',
                           title=title,
                           categories=all_category,
                           all_pitches=all_pitches)


#new pitch
@login_required
@main.route('/pitch/newpitch', methods=['POST', 'GET'])
@login_required
def new_pitch():
    form = PitchForm()
    if form.validate_on_submit():
        title = form.pitch_title.data
        category = form.pitch_category.data
        yourPitch = form.pitch_comment.data

        #update pitch instance
        new_pitch = Pitch(pitch_title=title,
                          pitch_category=category,
                          pitch_comment=yourPitch,
                          user=current_user)

        #save pitch
        new_pitch.save_pitch()
        return redirect(url_for('.index'))

    title = 'NEW PITCH'
    return render_template('pitch.html', title=title, pitchform=form)


@main.route('/categories/<int:id>')
def category(id):
    category = PitchCategory.query.get(id)
    if category is None:
        abort(404)

    pitches = Pitch.get_pitches(id)
    return render_template('category.html', pitches=pitches, category=category)


@main.route('/category/Interview', methods=['GET'])
def getInterviewPitch():
    pitches = Pitch.get_pitches('interview')

    return render_template('pitches/interview.html', interviewPitches=pitches)


@main.route('/category/Pickuplines', methods=['GET'])
def getLinesPitch():
    pitches = Pitch.get_pitches('pickup')
    return render_template('pitches/lines.html', pickupPitches=pitches)


@main.route('/category/Product', methods=['GET'])
def getProductPitch():
    pitches = Pitch.get_pitches('product')
    return render_template('pitches/product.html', productPitches=pitches)


@main.route('/category/Business', methods=['GET'])
def getBusinessPitch():
    pitches = Pitch.get_pitches('business')
    return render_template('pitches/business.html', businessPitches=pitches)


@main.route('/category/Funny', methods=['GET'])
def getFunnyPitch():
    pitches = Pitch.get_pitches('funny')
    return render_template('pitches/funny.html', funnyPitches=pitches)


@main.route('/category/promotional', methods=['GET'])
def getPromoPitch():
    pitches = Pitch.get_pitches('promotion')
    return render_template('pitches/promo.html', promoPitches=pitches)


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
@main.route('/comment/<int:id>', methods=['POST', 'GET'])
@login_required
def post_comment(id):
    pitche = Pitch.getPitchId(id)
    comments = Comments.get_comments(id)

    if request.args.get("like"):
        pitche.likes = pitche.likes + 1

        db.session.add(pitche)
        db.session.commit()

        return redirect(".comment".format(pitch_id=category.id))

    elif request.args.get("dislike"):
        pitche.dislikes = pitche.dislikes + 1

        db.session.add(pitche)
        db.session.commit()

        return redirect(".comment".format(pitch_id=category.id))

    form = CommentForm()
    if form.validate_on_submit():
        comment = form.opinion.data

        new_comment = Comments(opinion=comment,
                               user_id=current_user.id,
                               pitches_id=pitche.id)

        new_comment.save_comment()

        return redirect(url_for('main.post_comment', id=pitche.id))
    return render_template('comment.html',
                           commentform=form,
                           comments=comments,
                           pitch=pitche)


#upvoting/downvoting pitches
# @main.route('/pitch/upvote/<int:id>&<int:vote_type>')

