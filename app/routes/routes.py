# routes.py

from flask import flash, redirect, request, render_template, url_for, get_flashed_messages
from flask_login import login_required, login_user, logout_user
from flask_principal import Permission, RoleNeed

from app.models.login_form import LoginForm
from app.models.registration_form import RegistrationForm
from app.models.user import User
from app.app import db 

from ..services.services import (
    proxy_image_logic
)

def configure_routes(app, login_manager):
    @app.route('/')
    @login_required
    def index():
        return render_template('index.html')

    @app.route('/settings')
    def settings():
        return render_template('settings.html')

    @app.route('/image/')
    def proxy_image():
        url = request.args.get('url')
        return proxy_image_logic(url)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        form = LoginForm()
        if form.validate_on_submit():
            try:
                username = form.username.data
                password = form.password.data
                user = User.query.filter_by(username=username).first()
                if user and user.check_password(password):
                    login_user(user)
                    return redirect(url_for('index'))
                else:
                    flash('Invalid username or password', 'error')
            except Exception as e:
                flash('Login failed due to an unexpected error', 'error')
        return render_template('login.html', form=form)
    
    @app.route('/register', methods=['GET', 'POST'])
    def register():
        form = RegistrationForm()
        if form.validate_on_submit():
            user = User(username=form.username.data)
            user.set_password(form.password.data)
            # Check if this is the first user
            if User.query.count() == 0:
                user.roles = 'admin'
            else:
                user.roles = 'user'
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('login'))
        return render_template('register.html', form=form)

    @app.route('/logout')
    @login_required 
    def logout():
        logout_user() 
        flash('You have been logged out.', 'info')
        return redirect(url_for('login')) 