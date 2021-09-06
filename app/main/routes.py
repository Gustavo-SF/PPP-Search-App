

from flask import render_template, redirect, url_for, request
from flask_login import login_required

from app.main import bp
from app.models import Material
from app.main.forms import SearchForm
from app.search import get_materials_by_id, get_materials_by_query

@bp.route('/', methods=['GET', 'POST'])
@bp.route('/search', methods=['GET', 'POST'])
@login_required
def search():
    form = SearchForm()
    if form.validate_on_submit():
        if form.type_of_search.data == "1":
            cluster_of_materials = get_materials_by_id(form.q.data)
        elif form.type_of_search.data == "2":
            cluster_of_materials = get_materials_by_query(form.q.data)
        return render_template("results.html", searched_material=form.q.data, materials=cluster_of_materials)
    return render_template('search.html', title='Search Page', form=form)
    