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
def latest_json():
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
