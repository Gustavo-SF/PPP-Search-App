

from flask import render_template, redirect, url_for
from flask_login import login_required

from app.main import bp
from app.models import Material
from app.main.forms import SearchForm

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    form = SearchForm()
    if form.validate_on_submit():
        return redirect(url_for("main.results"))
    return render_template('search.html', title='Search Page', form=form)
    


@bp.route('/results')
@login_required
def results():
    materials = [
        Material(id="00001", description="This is number one"),
        Material(id="00002", description="This is number two!")
    ]
    return render_template("results.html", materials=materials)