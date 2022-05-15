"""End to End Test For Error Message"""

import pytest


@pytest.mark.parametrize("task", ["Text To Text", "Translation"])
@pytest.mark.parametrize("debug", [True, False])
def test_text_success(task, debug, page):
    # choose the return text model
    model = page.locator("text=invalid-task-model")
    model.click()
    return_text_model = page.locator("text=return-error-message")
    return_text_model.click()

    # locate the sidebar
    sidebar = page.locator('section[data-testid="stSidebar"]')

    # open the selector
    # here, instead of using:
    # task_selector = sidebar.locator(
    #     'div[data-baseweb="select"]:below(:text("Select the Task"))'
    # )
    # we choose to select the 'Text To Text' spefically, just in case
    # the task selection is clicked too fast and streamlit re-select the
    # default task of the model again.
    task_selector = sidebar.locator("text='Text To Text'")
    task_selector.click()

    # choose the task
    task = page.locator("li[role='option']").locator(f"text='{task}'")
    task_selector.wait_for(timeout=10000)
    task.click()

    # enable debug
    if debug:
        sidebar.locator("text='Debug'").click()

    # fill the text area
    page.fill("textarea", "Hello.")
    main_div = page.locator("section.main")

    # click run button
    run_btn = main_div.locator("text=Run")
    run_btn.click()

    # wait for the result
    result = main_div.locator('div.stAlert:has-text("Error Message")')
    result.wait_for(timeout=10000)

    assert result.count() == 1

    # wait for debug expander
    if debug:
        debug_expander = main_div.locator(
            'div[data-testid="stExpander"]:has-text("Debug")'
        )
        debug_expander.wait_for(timeout=10000)
        assert debug_expander.count() == 1
