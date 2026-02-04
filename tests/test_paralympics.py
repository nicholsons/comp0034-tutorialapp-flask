from playwright.sync_api import Page, expect


def test_page_has_body(page: Page, app_server):
    """
    GIVEN a server URL (app_server fixture yields the URL)
    WHEN the 'home' page is requested
    THEN the page body should be visible
    """
    page.goto(app_server)
    expect(page.locator("body")).to_be_visible()


def test_line_chart_displays(page: Page, app_server):
    """
    GIVEN a server URL
    WHEN the 'trends' page is requested
    AND the sports data is chosen
    THEN a plotly line chart should be visible
    """
    # GIVEN a server when the trends page is requested
    page.goto(f"{app_server}/trends")
    # AND the sports data is chosen
    page.locator("#selected_type").select_option("sports")
    # THEN a plotly line chart should be visible
    expect(page.locator(".js-plotly-plot")).to_be_visible()


def test_answer_question_correct(page: Page, app_server):
    """
    GIVEN a server URL
    WHEN the 'home' page is requested
    AND the answer to a question is selected and submitted and is correct
    THEN a new question should be displayed
    """
    page.goto(app_server)
    page.get_by_role("radio", name="Lillehammer").check()
    page.get_by_role("button", name="Submit answer").click()
    expect(page.get_by_text("How many participants were")).to_contain_text("?")


def test_new_question_submitted(page: Page, app_server):
    """
    GIVEN a server URL
    WHEN the question page is requested
    AND textarea with id="question_text" has the text for a new question entered
    AND option_text_1 to option_text_4 are completed
    AND one of is_correct_1 to is_correct_4 is True
    AND "submit" is clicked
    THEN if the requests to the REST API with a new question and 4 responses are successful, a
    response should be displayed with text "Question saved!".
    """
    page.goto(f"{app_server}/question")
    page.locator("#question_text").fill("New question")
    page.locator("#option_text_1").fill("A is correct")
    page.locator("#option_text_2").fill("B is incorrect")
    page.locator("#option_text_3").fill("C is incorrect")
    page.locator("#option_text_4").fill("D is incorrect")
    page.locator("#is_correct_1").check()
    page.locator("#submit").click()
    expect(page.get_by_text("Question saved!")).to_be_visible()
