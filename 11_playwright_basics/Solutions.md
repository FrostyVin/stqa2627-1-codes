### Part 2 solution

```py
from playwright.sync_api import Page, expect

def test_homepage_loads(page: Page):
    # Navigate to the local application
    page.goto("http://127.0.0.1:5000/")

    # Verify the page loaded correctly by checking the main heading
    heading = page.get_by_role("heading", name="Welcome to the Pet Shop!")
    expect(heading).to_be_visible()
```

### Part 3 solution

```py
import requests
from playwright.sync_api import Page, expect

def test_homepage_loads(page: Page):
    # Navigate to the local application
    page.goto("http://127.0.0.1:5000/")

    # Verify the page loaded correctly by checking the main heading
    heading = page.get_by_role("heading", name="Welcome to the Pet Shop!")
    expect(heading).to_be_visible()

def test_create_pet(page: Page):
    # Reset the database before testing
    requests.post("http://127.0.0.1:5000/pets/reset")

    page.goto("http://127.0.0.1:5000/")

    # Interact using user-facing locators
    page.get_by_placeholder("Name").fill("Buddy")
    page.get_by_placeholder("Category").fill("Dog")
    page.get_by_label("Gender:").select_option("MALE")
    page.get_by_label("Birthday:").fill("2024-01-01")

    # Click the create button by its accessible role and name
    page.get_by_role("button", name="Create").click()
```

### Part 4 solution

```py
def test_create_pet(page: Page):
    requests.post("http://127.0.0.1:5000/pets/reset")
    page.goto("http://127.0.0.1:5000/")

    page.get_by_placeholder("Name").fill("Buddy")
    page.get_by_placeholder("Category").fill("Dog")
    page.get_by_label("Gender:").select_option("MALE")
    page.get_by_label("Birthday:").fill("2024-01-01")
    page.get_by_role("button", name="Create").click()

    # Assert the flash message appears (Playwright auto-waits for this DOM update)
    flash_message = page.locator("#flash_message")
    expect(flash_message).to_have_text("Success")

    # Assert the new pet appears in the search results list
    results_section = page.locator("#search_results")
    expect(results_section).to_contain_text("Buddy")
    expect(results_section).to_contain_text("Dog")
```
