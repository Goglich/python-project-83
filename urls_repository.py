import psycopg2
from psycopg2.extras import DictCursor, NamedTupleCursor


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
        with DBConnection(self.db_url, cursor_factory=NamedTupleCursor) as cur:
            cur.execute("""
            SELECT
            urls.id,
            urls.name,
            urls.created_at,
            MAX(url_checks.created_at) as last_check,
            url_checks.status_code
            FROM urls
            LEFT JOIN url_checks ON urls.id = url_checks.url_id
            GROUP BY urls.id, url_checks.status_code
            ORDER BY created_at DESC
            """)
            return cur.fetchall()

    def find(self, id):
        with DBConnection(self.db_url, cursor_factory=DictCursor) as cur:
            cur.execute("""
                SELECT * FROM urls WHERE id = %s""", (id,))
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
                "INSERT INTO urls (name) VALUES (%s) RETURNING id",
                (url['url'], )
            )
            id = cur.fetchone()[0]
            url['id'] = id

    def save_check(self, ulr_id, status_code):
        with DBConnection(self.db_url) as cur:
            cur.execute(
                "INSERT INTO url_checks (url_id, status_code) VALUES (%s, %s) RETURNING id",
                (ulr_id, status_code)
            )

    def get_checks_desc(self, url_id):
        with DBConnection(self.db_url, cursor_factory=DictCursor) as cur:
            cur.execute ("""
                SELECT id, status_code, COALESCE(h1, '') as h1,
                COALESCE(title, '') as title, COALESCE(description, '') as
                description,
                created_at::text
                FROM url_checks
                WHERE url_id = %s
                ORDER BY id DESC
                """,
                (url_id,)
                )
            return cur.fetchall()
