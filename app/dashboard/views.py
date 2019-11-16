from flask import render_template
from flask_login import login_required
from . import dashboard


@dashboard.route('/')
@login_required
def dashboard():
    return render_template('dashboard/dashboard.html', html_title='Nutanix Dashboard')
