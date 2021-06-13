from flask import render_template, request, redirect, url_for, abort
from flask_login import login_required, current_user
from wtforms import form
from .forms import PitchForm, CommentForm, CategoryForm
from . import main
from .. import db
from ..models import Pitch, Comments


#categories
@main.route('/')
def index():
    """
        function that returns index page
    """

    all_pitches = Pitch.query.order_by('id').all()
    print(all_pitches)

    title = 'The Pitch Manifesto'
    return render_template('index.html', title=title, all_pitches=all_pitches)


#new pitch
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


likes = 0
dislikes = 0
#view single pitch alongside its comments
@main.route('/comment/<int:id>', methods=['POST', 'GET'])
@login_required
def post_comment(id):
    pitche = Pitch.getPitchId(id)
    comments = Comments.get_comments(id)

    if request.args.get("like"):
        pitch = Pitch.query.filter_by(user_id=current_user.id)
        pitch.likes += 1
        print(pitch.likes)

        db.session.add(pitch.likes)
        db.session.commit()
        return str(pitch.likes)

    elif request.args.get("dislike"):
        pitche.dislikes += 1

        db.session.add()
        db.session.commit()

        return redirect(".comment")

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


@main.route('/pitch/upvote/<int:id>&<int:vote>')
@login_required
def vote(id, vote):
    counter = 0

    pitche = Pitch.getPitchId(id)
    # vote = .get_vote(id)
    counter += 1
    print(counter)
    new_vote = Pitch(likes=counter)
    new_vote.save_vote()

    return str(new_vote)

    # votes = Votes.query.filter_by(user_id=current_user.id).all()
    # print(f'The new vote is {votes}')
    # to_str=f'{vote_type}:{current_user.id}:{id}'
    # print(f'The current vote is {to_str}')


# def vote(id,vote_type):
#     """
#     View function that adds one to the vote_number column in the votes table
#     """
#     # Query for user
#     votes = Votes.query.filter_by(user_id=current_user.id).all()
#     to_str=f'{vote_type}:{current_user.id}:{id}'

#     if not votes:
#         new_vote = Votes(vote=vote_type, user_id=current_user.id, pitches_id=id)
#         new_vote.save_vote()
#         # print(len(count_likes))
#         print('YOU HAVE new VOTED')

#     for vote in votes:
#         if f'{vote}' == to_str:
#             print('YOU CANNOT VOTE MORE THAN ONCE')
#             break
#         else:
#             new_vote = Votes(vote=vote_type, user_id=current_user.id, pitches_id=id)
#             new_vote.save_vote()
#             print('YOU HAVE VOTED')
#             break
#     return redirect(url_for('.post_comment', id=id))
