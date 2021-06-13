from wtforms import StringField, TextAreaField, SubmitField, SelectField
from flask_wtf import FlaskForm
from wtforms.validators import Required


class PitchForm(FlaskForm):
    """
    form for creating a pitch
    """
    pitch_title = StringField('Title', validators=[Required()])
    pitch_category = SelectField('Category',
                                 choices=[('Select category',
                                           'Select category'),
                                          ('interview', 'Interview'),
                                          ('product', 'Product'),
                                          ('business', 'Business'),
                                          ('funny', 'Funny'),
                                          ('promotion', 'Promotion'),
                                          ('pickup', 'Pickup Lines')],
                                 validators=[Required()])
    pitch_comment = TextAreaField('Your Pitch')
    submit = SubmitField('Submit')


class CategoryForm(FlaskForm):
    """
    classify a pitch
    """
    name = StringField('Category Name', validators=[Required()])
    submit = SubmitField('Create')


class CommentForm(FlaskForm):
    """
        form for creating a pitch comment
    """
    opinion = TextAreaField('COMMENT ON PITCH')
    submit = SubmitField('SUBMIT')
