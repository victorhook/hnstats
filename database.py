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

        for post in posts:
            cursor.execute(
                f'INSERT INTO Post values (?, ?, ?, ?, ?, ?, ?, ?)',
                (sample_time,post.rank, post.title, post.site, post.score,
                 post.user, post.age, post.comments)
            )

        self.con.commit()

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

