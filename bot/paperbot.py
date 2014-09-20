__author__ = 'scottumsted'
from datetime import datetime
from time import mktime
import random
import feedparser
from bot import pdb


class PaperBot():
    def __init__(self):
        self._sources = pdb.get_active_sources()

    def start(self):
        self.curate()
        # TODO need to add topic identification

    def curate(self):
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
                        story['_summary'] = entry['summary']
                    else:
                        story['_summary'] = ''
                    if 'id' in entry:
                        story['_id'] = entry['id']
                    else:
                        story['_id'] = entry['link']
                    story.update(entry)
                    pdb.add_story(story)
                    story_count += 1
        print 'story_count: %d'%story_count
    def assign_topic(self):
        pass

    def generate_path(self, size=8):
        uidPot = 'ABCDEFGIJKLMNOPQRSTUVWXYZ0123456789abcdefghijklmnopqrstuvwxyz'
        uid = '';
        l = len(uidPot) - 1
        for i in range(size):
            uid = uid + uidPot[random.randint(0, l)]
        return '/story/' + uid


if __name__ == '__main__':
    pb = PaperBot()
    pb.start()