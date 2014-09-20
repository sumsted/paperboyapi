__author__ = 'scottumsted'
from datetime import datetime
import uuid
import logging
from data import dbpool


class PaperboyModel():
    def __init__(self):
        logging.basicConfig(level=logging.INFO)

    def add_story(self, story):
        con, cur = dbpool.get_connection()
        result = None
        try:
            sql = ""
            cur.execute(sql, story)
            if cur.rowcount > 0:
                result = cur.fetchone()['id']
        except Exception, e:
            logging.error('add_story: ' + e.message)
            pass
        finally:
            con.commit()
            dbpool.put_connection(con)
        return result

    def get_stories(self):
        con, cur = dbpool.get_connection()
        result = None
        try:

            sql = "select id, source_name source, s_date date, s_title title, s_summary summary, s_author author, "\
                "s_link link, s_media_content media_content " \
                "from story order by id desc limit 50;"
            cur.execute(sql, {})
            result = cur.fetchall()
        except Exception, e:
            logging.error('get_stories: ' + e.message)
        finally:
            con.commit()
            dbpool.put_connection(con)
        return result