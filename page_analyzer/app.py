from flask import Flask, render_template, request, url_for, redirect, flash
from dotenv import load_dotenv
import os
from page_analyzer.urls_repository import URLSRepository
from page_analyzer.validator import validate
from page_analyzer.utils import normalize_url, get_page_data


load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['DATABASE_URL'] = os.getenv('DATABASE_URL')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('page_not_found.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('server_error.html'), 500


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/urls')
def get_urls():
    repo = URLSRepository(app.config['DATABASE_URL'])
    with repo.conn:
        urls = repo.get_all_urls_info()
    repo.close_connection()
    return render_template('urls.html', urls=urls)


@app.post('/urls')
def new_url():
    repo = URLSRepository(app.config['DATABASE_URL'])
    form_data = request.form.to_dict()
    errors = validate(form_data['url'])
    if errors:
        flash(errors['name'], category='error')
        return render_template(
            'index.html'
            ), 422
    normalized_url = normalize_url(form_data['url'])
    with repo.conn:
        existing_url = repo.get_url(normalized_url)
        if existing_url:
            flash("Страница уже существует", category="info")
            return redirect(url_for("show", url_id=existing_url[0]))
        repo.save_url(normalized_url)
        new_url = repo.get_url(normalized_url)
        if new_url:
            flash("Страница успешно добавлена", category="success")
            return redirect(url_for("show", url_id=new_url[0]))
        else:
            flash("Ошибка при добавлении страницы", category="error")
            return redirect(url_for('index'))


@app.route('/urls/<url_id>')
def show(url_id):
    repo = URLSRepository(app.config['DATABASE_URL'])
    with repo.conn:
        url = repo.find_url(url_id)
        if not url:
            return render_template('page_not_found.html'), 404
        url_checks = repo.get_checks_desc(url_id)
    repo.close_connection()
    return render_template(
        'show.html',
        url=url,
        url_checks=url_checks
        )


@app.post('/urls/<url_id>/checks')
def check_url(url_id):
    repo = URLSRepository(app.config['DATABASE_URL'])
    with repo.conn:
        url = repo.find_url(url_id)
        if not url:
            return render_template(
                'page_not_found.html'
            ), 404
        status_code, tags = get_page_data(url)
        if not status_code:
            flash('Произошла ошибка при проверке', category="error")
            return redirect(url_for('show', url_id=url_id))
        repo.save_check(
                url_id,
                status_code,
                tags['h1'],
                tags['title'],
                tags['description']
            )
    repo.close_connection()
    flash("Страница успешно проверена", category="success")
    return redirect(url_for('show', url_id=url_id))
