from flask import Flask, render_template, request, url_for, redirect, flash
from dotenv import load_dotenv
import os
from .urls_repository import URLSRepository
from .validator import validate
from datetime import datetime
from . import utils


load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('page_not_found.html'), 404


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/urls')
def get_urls():
    repo = URLSRepository()
    urls = repo.get_content()
    return render_template(
        'urls.html',
        urls=urls
        )


@app.post('/urls')
def new_url():
    repo = URLSRepository()
    form_data = request.form.to_dict()
    errors = validate(form_data['url'])
    if errors:
        flash(errors['name'], category='error')
        return redirect(
            url_for('index')
            )
    normalized_url = utils.normalize_url(form_data['url'])
    existing_url_id = repo.is_available(normalized_url)

    if existing_url_id:
        flash("Страница уже существует", category="info")
        return redirect(url_for("show", url_id=existing_url_id[0]))

    data_to_save = {
        'url': normalized_url,
        'created_at': datetime.now()
    }
    repo.save_url(data_to_save)
    new_url_id = repo.is_available(normalized_url)

    if new_url_id:
        flash("Страница успешно добавлена", category="success")
        return redirect(url_for("show", url_id=new_url_id[0]))
    else:
        flash("Ошибка при добавлении страницы", category="error")
        return redirect(url_for('index'))


@app.route('/urls/<url_id>')
def show(url_id):
    repo = URLSRepository()
    url = repo.find_url(url_id)
    if not url:
        return render_template('/page_not_found.html'), 404
    url_checks = repo.get_checks_desc(url_id)
    return render_template(
        'show.html',
        url=url,
        url_checks=url_checks
        )


@app.post('/urls/<id>/checks')
def check_url(id):
    repo = URLSRepository()
    url = repo.find_url(id)
    if not url:
        return render_template(
            '/page_not_found.html'
        ), 404
    status_code, tags = utils.get_page_data(url)
    if not status_code:
        flash('Произошла ошибка при проверке', category="error")
        return redirect(url_for('show', id=id))
    repo.save_check(
            id,
            status_code,
            tags['h1'],
            tags['title'],
            tags['description']
        )
    flash("Страница успешно проверена", category="success")
    return redirect(url_for('show', url_id=id))
