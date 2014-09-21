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
            insert_sql = "insert into story (source_id, source_name, source_url, path, times_updated, s_id, s_date, s_title, s_summary, s_author, s_link, s_tags, s_media_content, created, updated, fuzzy_summary) " \
                         "values (%(_source_id)s, %(_source_name)s, %(_source_url)s, %(_path)s, 0, %(_id)s, %(_published_parsed)s, %(title)s, %(_summary)s, %(_author)s, %(link)s, %(_tags)s, %(_media_content)s, now(), now(), %(_fuzzy_summary)s) " \
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
            sql = "select id, source_name source, s_date date, s_title title, s_summary summary, s_author author, " \
                  "'/story/'||path link, s_media_content media_content " \
                  "from story order by id desc limit 50;"
            cur.execute(sql, {})
            result = cur.fetchall()
        except Exception, e:
            logging.error('get_stories: ' + e.message)
        finally:
            con.commit()
            dbpool.put_connection(con)
        return result

    def get_story(self, id):
        con, cur = dbpool.get_connection()
        result = None
        try:
            sql = "select id, source_name source, s_date date, s_title title, s_summary summary, s_author author, " \
                  "'/story/'||path link, s_media_content media_content " \
                  "from story where id = %(id)s"
            cur.execute(sql, {'id':id})
            result = cur.fetchone()
        except Exception, e:
            logging.error('get_stories: ' + e.message)
        finally:
            con.commit()
            dbpool.put_connection(con)
        return result

    def get_story_by_path(self, path):
        con, cur = dbpool.get_connection()
        result = None
        try:
            sql = "select id, source_name source, s_date date, s_title title, s_summary summary, s_author author, " \
                  "'/story/'||path link, s_media_content media_content " \
                  "from story where path = %(path)s"
            cur.execute(sql, {'path':path})
            result = cur.fetchone()
        except Exception, e:
            logging.error('get_stories: ' + e.message)
        finally:
            con.commit()
            dbpool.put_connection(con)
        return result

    def get_fuzzy_summaries(self, except_id=None):
        con, cur = dbpool.get_connection()
        result = None
        try:
            sql_id = "select id, s_title, fuzzy_summary from story where s_date > now() - '24 hours'::interval and id != %(id)s"
            sql_no_id = "select id, s_title, fuzzy_summary from story where s_date > now() - '24 hours'::interval "
            if except_id is not None:
                cur.execute(sql_id, {'id':except_id})
            else:
                cur.execute(sql_no_id, {})
            result = cur.fetchall()
        except Exception, e:
            logging.error('get_fuzzy_summaries: ' + e.message)
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

    def get_topic_story(self, id):
        con, cur = dbpool.get_connection()
        result = None
        try:
            sql = "select topic_id from topic_story where story_id = %(id)s"
            cur.execute(sql, {'id': id})
            if cur.rowcount > 0:
                result = cur.fetchone()['topic_id']
        except Exception, e:
            logging.error('get_active_sources: ' + e.message)
        finally:
            con.commit()
            dbpool.put_connection(con)
        return result

    def add_topic(self, name):
        con, cur = dbpool.get_connection()
        result = None
        try:
            sql = "insert into topic (name, created, updated) values (%(name)s, now(), now()) returning id"
            cur.execute(sql, {'name': name})
            if cur.rowcount > 0:
                result = cur.fetchone()['id']
        except Exception, e:
            logging.error('get_active_sources: ' + e.message)
        finally:
            con.commit()
            dbpool.put_connection(con)
        return result

    def add_topic_story(self, topic_id, id, score):
        con, cur = dbpool.get_connection()
        result = None
        try:
            sql = "insert into topic_story (topic_id, story_id, created, score) values (%(topic_id)s, %(story_id)s, now(), %(score)s) returning id"
            cur.execute(sql, {'topic_id': topic_id, 'story_id': id, 'score': score})
            if cur.rowcount > 0:
                result = cur.fetchone()['id']
        except Exception, e:
            logging.error('get_active_sources: ' + e.message)
        finally:
            con.commit()
            dbpool.put_connection(con)
        return result

    def get_topics(self):
        con, cur = dbpool.get_connection()
        result = None
        try:
            sql = "select id from topic where created > now() - '24 hours'::interval order by id desc"
            cur.execute(sql, {})
            result = cur.fetchall()
        except Exception, e:
            logging.error('get_topics: ' + e.message)
        finally:
            con.commit()
            dbpool.put_connection(con)
        return result

    def get_topic_story_by_topic(self, id):
        con, cur = dbpool.get_connection()
        result = None
        try:
            sql = "select distinct story_id from topic_story where topic_id = %(id)s order by story_id desc"
            cur.execute(sql, {'id': id})
            result = cur.fetchall()
        except Exception, e:
            logging.error('get_active_sources: ' + e.message)
        finally:
            con.commit()
            dbpool.put_connection(con)
        return result