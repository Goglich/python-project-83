from flask import Flask, render_template, request, url_for, redirect, flash
from dotenv import load_dotenv
import os
import psycopg2
from urls_repository import URLSRepository
from validator import validate
from datetime import datetime
import utils

load_dotenv()
app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
DATABASE_URL = os.getenv('DATABASE_URL')
conn = psycopg2.connect(DATABASE_URL)
repo = URLSRepository(conn)

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
        return render_template(
            '/urls.html',
            url=data,
            errors=errors
            ), 422
    data['url'] = utils.normalizating_url(data['url'])
    if repo.availability_url(data['url']):
        flash("Страница уже существует", category="info")
        return redirect(url_for("show", id=repo.availability_url(data['url'])[0]))
    data['created_at'] = datetime.now()
    repo.save(data)
    flash("Страница успешно добавлена", category="success")
    return redirect(url_for('get_urls'))

@app.route('/urls/<id>')
def show(id):
    url = repo.find(id)
    if not url:
        return 'page not found', 404
    return render_template(
        'show.html', 
        url=url
        )