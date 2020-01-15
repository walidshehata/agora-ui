from flask import render_template, redirect, flash, request, url_for
from flask_login import login_user, logout_user, login_required
from .forms import LoginForm, RegisterForm
from . import auth
from .. import agora_auth


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = agora_auth.authenticate(username=form.username.data, password=form.password.data)
        if user:
            flash(f'{user.display_name}, You have successfully logged in!!', 'success')
            login_user(user)
            next_url = request.args.get('next')
            if next_url is None or not next_url.startswith('/'):
                next_url = url_for('dashboard.index')
            return redirect(next_url)
        else:
            flash('Sorry, something went wrong!', 'danger')
    return render_template('auth/login.html', form=form, html_title='Login')


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    # if request.method == 'POST' and form.validate():
    if form.validate_on_submit():
        flash('All good')
        return redirect(url_for('home.index'))

    if form.errors:
        flash(form.errors, 'danger')

    return render_template('auth/register.html', form=form, html_title='Register')


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out')
    return redirect(url_for('home.index'))
