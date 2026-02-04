def test_print_response_params(client):
    """
    This is just so you can see what type of detail you get in a response object.
    Don't use this in your tests!
    """
    response = client.get("/")
    print("Printing response.headers:")
    print(response.headers)
    print('\n Printing response.headers["Content-Type"]:')
    print(response.headers['Content-Type'])
    print("Printing response.status_code:")
    print(response.status_code)
    print("Printing response.data:")
    print(response.data)
    print("Printing response.json:")
    print(response.json)


def test_home_page_loads(client):
    """
    GIVEN a test client
    WHEN the 'home' page is requested
    THEN check that the response is 200
    AND check the page title contains the word "Paralympics"
    """
    response = client.get("/")
    assert response.status_code == 200
    assert b"<title>Paralympics" in response.data


def test_locations_fails_post_request(client):
    """
    GIVEN a Flask test client
    WHEN a POST request is made to /locations
    THEN the status code should be 405
    """
    response = client.post("/locations")
    assert response.status_code == 405


def test_participants_form_post_success(client):
    """
    GIVEN a Flask test client
    WHEN a POST request is made to /participants with valid form data
    THEN the status code should be 200
    """
    # Simulate posting the form with multiple selected types
    data = {"paralympics_types": ["winter", "summer"]}
    resp = client.post("/participants", data=data)
    assert resp.status_code == 200
