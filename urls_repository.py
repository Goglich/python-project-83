import psycopg2
from psycopg2.extras import DictCursor


class URLError(Exception):
    pass


class DBConnection:
    def __init__(self, db_url, cursor_factory=None):
        self.db_url = db_url
        self.cursor_factory = cursor_factory

    def __enter__(self):
        self.db_url = psycopg2.connect(self.db_url)
        self.db_url.autocommit = True
        if self.cursor_factory:
            return self.db_url.cursor(cursor_factory=self.cursor_factory)
        return self.db_url.cursor()

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.db_url:
            self.db_url.close()

class URLSRepository:
    def __init__(self, db_url):
        self.db_url = db_url


    def get_content(self):
        with DBConnection(self.db_url, cursor_factory=DictCursor) as cur:
            cur.execute("SELECT * FROM urls order by id desc")
            result = [dict(row) for row in cur]
            return result

    def find(self, id):
        with DBConnection(self.db_url, cursor_factory=DictCursor) as cur:
            cur.execute("SELECT * FROM urls WHERE id = %s", (id,))
            row = cur.fetchone()
            return dict(row) if row else None

    def save(self, url):
        self._create(url)

    def availability_url(self, url):
        with DBConnection(self.db_url) as cur:
            query = "SELECT id FROM urls WHERE name = %s"
            cur.execute(query, (url,))
            result = cur.fetchone()
            return result


    def _create(self, url):
        with DBConnection(self.db_url) as cur:
            cur.execute(
                "INSERT INTO urls (name, created_at) VALUES (%s, %s) RETURNING id",
                (url['url'], url['created_at'])
            )
            id = cur.fetchone()[0]
            url['id'] = id