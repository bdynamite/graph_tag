from flask import jsonify, request

from project import db, cache
from . import bp, errors


def cache_key():
    tags = list(set(request.json.get('tags', [])))
    tags.sort()
    key = '{0}{1}'.format(request.path, tags)
    return key


@bp.route('/graph_by_tag', methods=['GET'])
@cache.cached(key_prefix=cache_key)
def graph_by_tag():
    tags = list(set(request.json.get('tags', [])))
    if not tags:
        raise errors.ApiError(
            message='no tags passed'
        )
    sql_query_tags, tags_values = convert_for_raw_sql(tags)
    raw_query = '''
            SELECT graph_id
                FROM graph_tags
                WHERE graph_tags.tag_id {}
                GROUP BY graph_id
                HAVING SUM(1) = :len_tags;
        '''.format(sql_query_tags)
    result = db.session.execute(raw_query, {**tags_values, 'len_tags': len(tags)})
    return jsonify([r[0] for r in result])


def convert_for_raw_sql(items_list):
    if len(items_list) == 1:
        return '= :param', {'param': items_list[0]}
    params = []
    values = {}
    for i, item in enumerate(items_list):
        value_param = 'param_{}'.format(i)
        raw_param = ':param_{}'.format(i)
        params.append(raw_param)
        values[value_param] = item
    return 'IN ({})'.format(', '.join(params)), values
