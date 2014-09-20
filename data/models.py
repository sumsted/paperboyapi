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
            insert_sql = "insert into story (source_id, source_name, source_url, path, times_updated, s_id, s_date, s_title, s_summary, s_author, s_link, s_tags, s_media_content, created, updated) " \
                "values (%(_source_id)s, %(_source_name)s, %(_source_url)s, %(_path)s, 0, %(_id)s, %(_published_parsed)s, %(title)s, %(_summary)s, %(_author)s, %(link)s, %(_tags)s, %(_media_content)s, now(), now()) " \
                "returning id"
            check_sql = "select count(*) num_stories from story where s_id=%(_id)s or (s_title=%(title)s and s_title<>'')"

            cur.execute(check_sql, story)
            if cur.rowcount > 0:
                match = True if cur.fetchone()['num_stories'] > 0 else False
                if not match:
                    cur.execute(insert_sql, story)
                    if cur.rowcount > 0:
                        result = cur.fetchone()['id']
                else:
                    pass
                    #print 'id:%s, title:%s, source:%s'%(story['_id'], story['title'], story['_source_name'])
            else:
                pass # bummer
                #print 'id:%s, title:%s, source:%s'%(story['_id'], story['title'], story['_source_name'])

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

    def get_active_sources(self):
        con, cur = dbpool.get_connection()
        result = None
        try:

            sql = "select id, name, url, type from source where active=true order by id"
            cur.execute(sql, {})
            result = cur.fetchall()
        except Exception, e:
            logging.error('get_active_sources: ' + e.message)
        finally:
            con.commit()
            dbpool.put_connection(con)
        return result
