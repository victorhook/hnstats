import sqlite3
from typing import List
from datetime import datetime

from post import Post


class Database:

    def __init__(self, db_path: str = 'hnstats.db'):
        self.db_path = db_path

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, *ignore):
        self.close()

    def open(self):
        self.con = sqlite3.connect(self.db_path)

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

    def fetch(self, amount: int = None) -> List[Post]:
        cursor = self.con.cursor()
        results = cursor.execute('Select * from Post;').fetchall()
        posts = [Post(*res[1:]) for res in results]
        return posts

    def _save_post(self, cursor, post: Post, sample_time: str):
        cursor.execute(
            f'INSERT INTO Post values (?, ?, ?, ?, ?, ?, ?, ?, ?)',
            (sample_time,post.rank, post.url, post.title, post.site, post.score,
            post.user, post.age, post.comments)
        )

    def init_db(self):
        cursor = self.con.cursor()
        cursor.execute("""
            CREATE TABLE Post
            (
                sample_time DATETIME,
                rank INT,
                url VARCHAR(255),
                title VARCHAR(255),
                site VARCHAR(255),
                score INT,
                user VARCHAR(255),
                age INT,
                comments INT
            );
        """)
        self.con.commit()

if __name__ == '__main__':
    with Database() as db:
        posts = db.fetch(1)
        print(posts)