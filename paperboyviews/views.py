__author__ = 'scottumsted'
from flask import render_template, make_response, request, json
from paperboyviews import app, pdb
import logging


def _padded_jsonify(callback, *args, **kwargs):
    content = str(callback) + '(' + json.dumps(dict(*args, **kwargs)) + ')'
    return app.response_class(content, mimetype='application/json')


def _regular_jsonify(o):
    content = json.dumps(o)
    return app.response_class(content, mimetype='application/json')


@app.route('/stories/', methods=['GET', 'POST'])
def stories():
    result = []
    callback = request.args.get('callback', None)
    try:
        stories = pdb.get_stories()
        if stories is not None:
            result = stories
    except Exception, e:
        result = []
    if callback is None:
        result = _regular_jsonify(result)
    else:
        result = _padded_jsonify(callback, {'stories': result})
    return result


@app.route('/topics/', methods=['GET', 'POST'])
def topics():
    result = []

    callback = request.args.get('callback', None)
    try:
        topics = pdb.get_topics()
        related_stories = []
        for topic in topics:
            topic_result = {'related_stories': []}
            topic_stories = pdb.get_topic_story_by_topic(topic['id'])
            i = 0
            for i, topic_story in enumerate(topic_stories):
                story = pdb.get_story(topic_story['story_id'])
                if not i:
                    topic_result.update(story)
                else:
                    topic_result['related_stories'].append({'source': story['source'], 'link': story['link']})
            result.append(topic_result)
    except Exception, e:
        result = []
    if callback is None:
        result = _regular_jsonify(result)
    else:
        result = _padded_jsonify(callback, {'topics': result})
    return result

@app.route('/story/<path>', methods=['GET'])
def tick(key):
    url = pdb.get_story_by_path(path)
    if url is not None:
        return redirect(url)
    else:
        return 'Not Found', 404