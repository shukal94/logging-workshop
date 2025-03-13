import logging

COMPANY_NAME = "Solvd Inc."
DATA_TO_INSERT = (4, 'Google', 30, 'Somewhere in Nowhere', 1000)

LOGGER = logging.getLogger("test")


def test_select_all(test_db_client):
    LOGGER.info("Get all the companies and validate result is not empty")
    result = test_db_client.get_companies()
    assert result is not None, "Query failed!"


def test_select_by_name(test_db_client):
    LOGGER.info(f"Get by name '{COMPANY_NAME}' and validate result is not empty")
    result = test_db_client.get_company_by_name(name=COMPANY_NAME)
    assert result is not None, "Query failed!"


def test_insert(test_db_client):
    LOGGER.info("Creating a new company.")
    test_db_client.add_company(company=DATA_TO_INSERT)

    LOGGER.info("Validating the new company created.")
    result = test_db_client.get_company_by_name("Google")
    assert result is not None, "Query failed!"
