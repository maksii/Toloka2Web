"""Registration form for new user accounts."""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo, ValidationError, Length

from app.models.user import User


class RegistrationForm(FlaskForm):
    """Form for handling new user registration.

    Attributes:
        username: Username field
        password: Password field
        confirm_password: Password confirmation field
        submit: Form submit button
    """

    username = StringField(
        "Username",
        validators=[
            DataRequired(),
            Length(
                min=3, max=80, message="Username must be between 3 and 80 characters"
            ),
        ],
    )
    password = PasswordField(
        "Password",
        validators=[
            DataRequired(),
            Length(min=8, message="Password must be at least 8 characters long"),
        ],
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[
            DataRequired(),
            EqualTo("password", message="Passwords must match"),
        ],
    )
    submit = SubmitField("Register")

    def validate_username(self, username: StringField) -> None:
        """Validate that the username is not already taken.

        Args:
            username: The username field to validate

        Raises:
            ValidationError: If the username is already taken
        """
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError("Please use a different username.")
