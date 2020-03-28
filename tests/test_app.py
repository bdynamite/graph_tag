
def test_no_tags(test_client, init_database):
    rv = test_client.get('/api/v1/graph_by_tag', json={
        'trags': ['four', 'five']
    })
    json_data = rv.get_json()
    assert json_data['message'] == 'no tags passed'


def test_two_wrong_tags(test_client, init_database):
    rv = test_client.get('/api/v1/graph_by_tag', json={
        'tags': ['four', 'five']
    })
    json_data = rv.get_json()
    assert json_data == []


def test_one_tag(test_client, init_database):
    rv = test_client.get('/api/v1/graph_by_tag', json={
        'tags': ['one']
    })
    json_data = rv.get_json()
    assert json_data == ['G100000', 'G100001', 'G100002']


def test_two_tags(test_client, init_database):
    rv = test_client.get('/api/v1/graph_by_tag', json={
        'tags': ['one', 'two']
    })
    json_data = rv.get_json()
    print(rv, json_data)
    assert json_data == ['G100001', 'G100002']
