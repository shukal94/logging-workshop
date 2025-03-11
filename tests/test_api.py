import logging

POST_ID = 1
USER_ID = 1

LOGGER = logging.getLogger("test")


def test_posts(json_placeholder_api):
    LOGGER.info("Get all posts")
    json = json_placeholder_api.get_posts()
    assert json is not None, "Nothing has been returned."


def test_posts_by_user_id(json_placeholder_api):
    LOGGER.info(f"Get all posts by {USER_ID}")
    json = json_placeholder_api.get_posts(user_id=USER_ID)
    assert json is not None, "Nothing has been returned."


def test_post_by_id(json_placeholder_api):
    LOGGER.info(f"Get post by id={POST_ID}")
    json = json_placeholder_api.get_post_by_id(POST_ID)
    assert json is not None, "Nothing has been returned."


def test_add_post(json_placeholder_api):
    payload = {
        "title": "Sample title",
        "body": "Sample body",
        "userId": USER_ID
    }
    LOGGER.info(f"Create a new post.")
    json = json_placeholder_api.create_post(payload=payload)
    assert json["title"] == payload["title"], "Resource was not created."


def test_update_post(json_placeholder_api):
    payload = {
        "id": POST_ID,
        "title": "Sample title",
        "body": "Sample body",
        "userId": USER_ID
    }
    LOGGER.info(f"Update post with id={POST_ID}")
    json = json_placeholder_api.update_post(post_id=POST_ID, payload=payload)
    assert json["title"] == payload["title"], "Resource was not updated."


def test_update_part_of_post(json_placeholder_api):
    payload = {
        "title": "Sample title"
    }
    LOGGER.info(f"Update post with id={POST_ID}")
    json = json_placeholder_api.patch_post(post_id=POST_ID, payload=payload)
    assert json["title"] == payload["title"], "Resource was not updated."


def test_delete_post(json_placeholder_api):
    LOGGER.info(f"Update post with id={POST_ID}")
    json = json_placeholder_api.delete_post(post_id=POST_ID)
    assert json is not None, "Resource was not deleted."
