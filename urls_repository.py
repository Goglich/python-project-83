import psycopg2
from psycopg2.extras import DictCursor


class URLError(Exception):
    pass


class URLSRepository:
    def __init__(self, conn):
        self.conn = conn

    def get_content(self):
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute("SELECT * FROM urls order by id desc")
            return [dict(row) for row in cur]

    def find(self, id):
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute("SELECT * FROM urls WHERE id = %s", (id,))
            row = cur.fetchone()
            return dict(row) if row else None

    def get_by_term(self, search_term=''):
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            cur.execute("""
                    SELECT * FROM urls
                    WHERE name ILIKE %s OR created_at ILIKE %s
                """, (f'%{search_term}%', f'%{search_term}%'))
            return cur.fetchall()

    def save(self, url):
        # if self.availability_url(url['url']):
        #     raise URLError("Страница уже существует")
        # else:
        self._create(url)

    def availability_url(self, url):
        with self.conn.cursor(cursor_factory=DictCursor) as cur:
            query = "SELECT id FROM urls WHERE name = %s"
            cur.execute(query, (url,))
            return cur.fetchone()

    def _update(self, url):
        with self.conn.cursor() as cur:
            cur.execute(
                "UPDATE urls SET name = %s, created_at = %s WHERE id = %s",
                (url['name'], url['created_at'], url['id'])
            )
        self.conn.commit()

    def _create(self, url):
        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO urls (name, created_at) VALUES (%s, %s) RETURNING id",
                (url['url'], url['created_at'])
            )
            id = cur.fetchone()[0]
            url['id'] = id
        self.conn.commit()