from flask import render_template, redirect, url_for, abort
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


#upvoting/downvoting pitches
@main.route('/pitch/upvote/<int:id>&<int:vote_type>')
@login_required
def upvote(id, vote_type):
    """
    View function to add votes to table
    """
    # Query for user
    votes = Votes.query.filter_by(user_id=current_user.id).all()
    print(f'The new vote is {votes}')
    to_str = f'{vote_type}:{current_user.id}:{id}'
    print(f'The current vote is {to_str}')

    if not votes:
        new_vote = Votes(vote=vote_type,
                         user_id=current_user.id,
                         pitches_id=id)
        new_vote.save_vote()
        # print(len(count_likes))
        print('YOU HAVE new VOTED')

    for vote in votes:
        if f'{vote}' == to_str:
            print('YOU CANNOT VOTE MORE THAN ONCE')
            break
        else:
            new_vote = Votes(vote=vote_type,
                             user_id=current_user.id,
                             pitches_id=id)
            new_vote.save_vote()
            print('YOU HAVE VOTED')
            break

    return redirect(url_for('.view_pitch', id=id))
