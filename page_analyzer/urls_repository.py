import psycopg2
from psycopg2.extras import DictCursor, NamedTupleCursor
from dotenv import load_dotenv
import os


class URLError(Exception):
    pass


class URLSRepository:
    def __init__(self):
        load_dotenv()
        self.dsn = os.getenv('DATABASE_URL')
        self.conn = psycopg2.connect(self.dsn)

    def get_content(self):
        with self.conn as conn:
            with conn.cursor(cursor_factory=NamedTupleCursor) as cur:
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
                ORDER BY id DESC
                """)
                return cur.fetchall()

    def find_url(self, id):
        with self.conn as conn:
            with conn.cursor(cursor_factory=DictCursor) as cur:
                cur.execute("""
                    SELECT * FROM urls WHERE id = %s""", (id,))
                row = cur.fetchone()
                return dict(row) if row else None

    def save_url(self, url):
        with self.conn as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO urls (name) VALUES (%s)",
                    (url['url'], )
                )

    def is_available(self, url):
        with self.conn as conn:
            with conn.cursor() as cur:
                query = "SELECT id FROM urls WHERE name = %s"
                cur.execute(query, (url,))
                result = cur.fetchone()
                return result

    def save_check(self, ulr_id, status_code, h1, title, description):
        with self.conn as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO url_checks
                    (url_id, status_code, h1, title, description)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (ulr_id, status_code, h1, title, description)
                )

    def get_checks_desc(self, url_id):
        with self.conn as conn:
            with conn.cursor(cursor_factory=DictCursor) as cur:
                cur.execute(
                    """
                    SELECT id, status_code, COALESCE(h1, '') as h1,
                    COALESCE(title, '') as title, COALESCE(description, '') as
                    description,
                    created_at::text
                    FROM url_checks
                    WHERE url_id = %s
                    ORDER BY id DESC
                    """,
                    (url_id, )
                    )
                return cur.fetchall()
