from flask import jsonify, request
from project import db, cache
from . import bp, errors


def cache_key():
    tags = list(set(request.json.get('tags')))
    tags.sort()
    key = '{0}{1}'.format(request.path, tags)
    return key


@bp.route('/graph_by_tag', methods=['GET'])
@cache.cached(key_prefix=cache_key)
def graph_by_tag():
    tags = set(request.json.get('tags'))
    if not tags:
        raise errors.ApiError(
            message='no tags passed'
        )
    raw_query = '''
            SELECT graph_id
                FROM graph_tags
                WHERE graph_tags.tag_id IN ({0})
                GROUP BY graph_id
                HAVING SUM(1) = {1};
        '''.format(', '.join(tags), len(tags))
    result = db.session.execute(raw_query, {'tags': tags, 'tags_len': len(tags)})
    return jsonify([r[0] for r in result])
