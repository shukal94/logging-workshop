COMPANY_NAME = "Solvd Inc."
DATA_TO_INSERT = (4, 'Google', 30, 'Somewhere in Nowhere', 1000)


def test_select_all(test_db_client):
    result = test_db_client.get_companies()
    for row in result:
        print(row)
    assert result is not None, "Query failed!"


def test_select_by_name(test_db_client):
    result = test_db_client.get_company_by_name(name=COMPANY_NAME)
    print(result)
    assert result is not None, "Query failed!"


def test_insert(test_db_client):
    test_db_client.add_company(company=DATA_TO_INSERT)
    result = test_db_client.get_company_by_name("Google")
    print(result)
    assert result is not None, "Query failed!"
