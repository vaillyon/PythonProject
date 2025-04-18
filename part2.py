
import sqlite3

import time

import cherrypy


# class for web site
class MiniTwitter:
    def __init__(self):
        self.conn = None

        self.cursor = None
        self.init_db()

    # SQLite stores tweets
    def init_db(self):
        self.conn = sqlite3.connect("tweets.db", check_same_thread=False)
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS tweets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                message TEXT
            )
        """)
        self.conn.commit()

    # to close system
    def close_db(self):
        if self.conn:
            self.conn.close()

    # show tweets, new to old
    @cherrypy.expose
    def index(self):
        self.cursor.execute("SELECT timestamp, message FROM tweets ORDER BY id DESC")
        tweets = self.cursor.fetchall()
        html = "<h1>Mini Twitter</h1><a href='/new/'>Post a new tweet</a><br/><br/>"
        for timestamp, message in tweets:
            html += f"<p><strong>{timestamp}</strong>: {message}</p>"
        return html

    # add comment
    @cherrypy.expose
    def new(self, message=None):
        if message:
            timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
            self.cursor.execute("INSERT INTO tweets (timestamp, message) VALUES (?, ?)", (timestamp, message))
            self.conn.commit()
            raise cherrypy.HTTPRedirect("/")
        return """<form method='post'><textarea name='message'></textarea><br/><button type='submit'>Tweet</button></form>"""



if __name__ == "__main__":
    cherrypy.quickstart(MiniTwitter())

