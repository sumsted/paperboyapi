import string

__author__ = 'scottumsted'
from datetime import datetime
from time import mktime
import random
import feedparser
from fuzzywuzzy import fuzz
from BeautifulSoup import BeautifulSoup
from bot import pdb


class PaperBot():
    def __init__(self):
        self._sources = pdb.get_active_sources()

    def start(self):
        print 'Start feed curator'
        self.curate()
        print 'Stop feed curator'
        # TODO need to add topic identification

    def curate(self):
        punc = set(string.punctuation)
        story_count = 0
        for source in self._sources:
            feed = feedparser.parse(source['url'])
            if 'entries' in feed:
                entries = feed['entries']
                for entry in entries:
                    story = {}
                    story['_source_id'] = source['id']
                    story['_source_name'] = source['name']
                    story['_source_url'] = source['url']
                    story['_path'] = self.generate_path()
                    if 'tags' in entry:
                        story['_tags'] = ''.join([tag['term'] for tag in entry['tags']])
                    else:
                        story['_tags'] = ''
                    media_content_url = ''
                    if 'media_content' in entry:
                        for media_content in entry['media_content']:
                            media_content_url = media_content['url']
                            break
                    if media_content_url == '':
                        if 'links' in entry:
                            for link in entry['links']:
                                if 'type' in link and 'href' in link and 'image' in link['type']:
                                    media_content_url = link['href']
                                    break
                    story['_media_content'] = media_content_url
                    if 'published_parsed' in entry:
                        story['_published_parsed'] = datetime.fromtimestamp(mktime(entry['published_parsed']))
                    else:
                        story['_published_parsed'] = datetime.utcnow()
                    if 'author' in entry:
                        story['_author'] = entry['author']
                    else:
                        story['_author'] = ''
                    if 'summary' in entry:
                        story['_summary'] = self.remove_markup(entry['summary'])
                        story['_fuzzy_summary'] = ''.join(sorted(
                            ['%s ' % w.upper() for w in ''.join([c for c in story['_summary'] if c not in punc]).split()
                             if len(w) > 3 and w.isalpha()]))
                    else:
                        story['_summary'] = ''
                        story['_fuzzy_summary'] = ''
                    if 'id' in entry:
                        story['_id'] = entry['id']
                    else:
                        story['_id'] = entry['link']
                    story.update(entry)
                    id = pdb.add_story(story)
                    if id is not None:
                        fuzzy_summaries = pdb.get_fuzzy_summaries(id)
                        for summary in fuzzy_summaries:
                            score = fuzz.partial_token_set_ratio(summary['fuzzy_summary'], story['_fuzzy_summary'])
                            if score >= 50:
                                topic_id = pdb.get_topic_story(summary['id'])
                                if topic_id is not None:
                                    pdb.add_topic_story(topic_id, id, score)
                                else:
                                    topic_id = pdb.add_topic(summary['s_title'])
                                    pdb.add_topic_story(topic_id, summary['id'], score)
                                    pdb.add_topic_story(topic_id, id, score)
                                break
                    story_count += 1
                    if not story_count % 50:
                        print 'story_count: %d' % story_count
        print 'story_count: %d' % story_count

    def assign_topic(self):
        pass

    def generate_path(self, size=8):
        uidPot = 'ABCDEFGIJKLMNOPQRSTUVWXYZ0123456789abcdefghijklmnopqrstuvwxyz'
        uid = '';
        l = len(uidPot) - 1
        for i in range(size):
            uid = uid + uidPot[random.randint(0, l)]
        return uid

    def remove_markup(self, s):
        r = ''.join(BeautifulSoup(s, convertEntities=BeautifulSoup.HTML_ENTITIES).findAll(text=True))
        return r


if __name__ == '__main__':
    pb = PaperBot()
    pb.start()