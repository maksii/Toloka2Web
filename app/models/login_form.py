"""Login form for user authentication."""
from flask_wtf import FlaskForm
from wtforms import BooleanField, StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, ValidationError

from app.models.user import User

class LoginForm(FlaskForm):
    """Form for handling user login.
    
    Attributes:
        username: Username field
        password: Password field
        remember_me: Remember login checkbox
        submit: Form submit button
    """
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign in')

    def validate_username(self, username: StringField) -> None:
        """Validate that the username exists.
        
        Args:
            username: The username field to validate
            
        Raises:
            ValidationError: If the username doesn't exist
        """
        user = User.query.filter_by(username=username.data).first()
        if user is None:
            raise ValidationError("Username doesn't exist")