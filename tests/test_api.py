def test_posts(json_placeholder_api):
    json = json_placeholder_api.get_posts()
    assert json is not None, "Nothing has been returned."
