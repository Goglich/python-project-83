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
DATABASE_URL = os.getenv('DATABASE_URL')
repo = URLSRepository(DATABASE_URL)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('page_not_found.html'), 404


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/urls')
def get_urls():
    urls = repo.get_content()
    return render_template(
        'urls.html',
        urls=urls
        )


@app.post('/urls')
def new_url():
    data = request.form.to_dict()
    errors = validate(data)
    if errors:
        flash(errors['name'], category='error')
        return redirect(
            url_for('index')
            )
    data['url'] = utils.normalizating_url(data['url'])
    if repo.availability_url(data['url']):
        flash("Страница уже существует", category="info")
        return redirect(
            url_for(
                "show",
                id=repo.availability_url(data['url'])[0]
                )
            )
    data['created_at'] = datetime.now()
    repo.save(data)
    flash("Страница успешно добавлена", category="success")
    return redirect(url_for("show", id=repo.availability_url(data['url'])[0]))


@app.route('/urls/<id>')
def show(id):
    url = repo.find(id)
    if not url:
        return render_template('/page_not_found.html'), 404
    url_checks = repo.get_checks_desc(id)
    return render_template(
        'show.html',
        url=url,
        url_checks=url_checks
        )


@app.post('/urls/<id>/checks')
def check_url(id):
    if not repo.find(id):
        return render_template(
            '/page_not_found.html'
        ), 404
    status_code = utils.get_status_code(repo.find(id))
    if not status_code:
        flash('Произошла ошибка при проверке', category="error")
        return redirect(url_for('show', id=id))
    parsed_html = utils.html_parse(repo.find(id)['name'])
    repo.save_check(
            id,
            status_code,
            parsed_html['h1'],
            parsed_html['title'],
            parsed_html['description']
        )
    flash("Страница успешно проверена", category="success")
    return redirect(url_for('show', id=id))
