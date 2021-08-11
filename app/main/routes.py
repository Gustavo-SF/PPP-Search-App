

from flask import render_template, g, redirect, url_for
from flask_login import login_required, current_user

from app.main import bp
from app.models import Material
from app.main.forms import SearchForm

@bp.route('/')
@bp.route('/index')
@login_required
def index():
    return render_template('index.html', title='Home Page')


@bp.route('/results')
@login_required
def results():
    materials = [
        Material(id="00001", description="This is number one"),
        Material(id="00002", description="This is number two!")
    ]
    return render_template("results.html", materials=materials)

@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        g.search_form = SearchForm()


@bp.route('/search')
@login_required
def search():
    if not g.search_form.validate():
        return redirect(url_for('main.index'))
    return redirect(url_for('main.results'))