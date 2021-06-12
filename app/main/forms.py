from wtforms import StringField, TextAreaField, SubmitField, SelectField
from flask_wtf import FlaskForm
from wtforms.validators import Required


class PitchForm(FlaskForm):
    """
    form for creating a pitch
    """
    content = TextAreaField('WRITE YOUR PITCH')
    submit = SubmitField('SUBMIT')


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
