import sqlite3
from typing import List
from datetime import datetime

from post import Post


class Database:

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, *ignore):
        self.close()

    def open(self):
        self.con = sqlite3.connect('hnstats.db')

    def close(self):
        self.con.close()

    def save(self, posts: List[Post]):
        cursor = self.con.cursor()
        sample_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        saved = 0

        while saved < len(posts):
            try:
                self._save_post(cursor, posts[saved], sample_time)
                saved += 1
            except sqlite3.OperationalError:
                print('Found no previous tables, creating new one...')
                self.init_db()

        self.con.commit()

    def _save_post(self, cursor, post: Post, sample_time: str):
        cursor.execute(
            f'INSERT INTO Post values (?, ?, ?, ?, ?, ?, ?, ?)',
            (sample_time,post.rank, post.title, post.site, post.score,
            post.user, post.age, post.comments)
        )

    def init_db(self):
        cursor = self.con.cursor()
        cursor.execute("""
            CREATE TABLE Post
            (
                sample_time DATETIME,
                rank INT,
                title VARCHAR(255),
                site VARCHAR(255),
                score INT,
                user VARCHAR(255),
                age INT,
                comments INT
            );
        """)
        self.con.commit()

