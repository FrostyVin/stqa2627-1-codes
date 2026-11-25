# Foundations of Modern Browser Automation with Playwright

In this exercise, we will build our first browser automation test suite using Playwright and Pytest. By the end of this lab, we will have a test script that:
1. Installs and configures the Playwright environment.
2. Launches a browser natively to interact with our local Flask Pet Shop application.
3. Interacts with web elements using resilient, user-facing smart locators (by labels, placeholders, and roles).
4. Validates UI states using built-in, auto-waiting assertions.
5. Captures and inspects execution traces when a test fails.

## Part 1: Prepare Your Python Environment

Playwright requires its own package and native browser binaries to run. Since we are testing our local Pet Shop app, we must also ensure Flask and `requests` are installed.

Your Tasks:
1. Ensure your `requirements.txt` file in the project root contains the following packages:
   ```text
   flask
   pytest
   pytest-playwright
   requests
   ```
2. Install the Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Download the native browser engines (Chromium, Firefox, WebKit) required by Playwright:
   ```bash
   playwright install
   ```

## Part 2: Boot the App and Create Your First Test Script

Playwright integrates seamlessly with Pytest using a built-in `page` fixture, which automatically handles launching an isolated browser context and closing it after each test.

Your Tasks:
1. Start your local Flask application in the background (or in a separate terminal):
   ```bash
   python app.py
   ```
2. Inside your project folder, create a `tests/` directory and add a new test file named `tests/test_pet_shop.py`.
3. Import `Page` and `expect` from `playwright.sync_api`.
4. Implement a test function `test_homepage_loads(page: Page)` that:
   - Navigates to `"http://127.0.0.1:5000/"` using `page.goto()`.
   - Locates the main heading `"Welcome to the Pet Shop!"` using `page.get_by_role()`.
   - Verifies that the heading is visible using `expect(...).to_be_visible()`.
5. Run pytest to verify your first test passes:
   ```bash
   pytest
   ```

## Part 3: Smart Locators and Core Interactions

Instead of relying on fragile IDs or XPath selectors, Playwright encourages user-facing locators that mimic how real users find elements on a page (by placeholders, labels, and accessible roles).

Your Tasks:
1. Open `tests/test_pet_shop.py` and import `requests`.
2. Implement a new test function `test_create_pet(page: Page)` that:
   - Resets the backend database before testing by sending a POST request to `"http://127.0.0.1:5000/pets/reset"`.
   - Navigates to `"http://127.0.0.1:5000/"`.
   - Fills the `"Name"` field with `"Buddy"` and the `"Category"` field with `"Dog"` using `page.get_by_placeholder()`.
   - Selects `"MALE"` in the `"Gender:"` dropdown using `page.get_by_label()` and `.select_option()`.
   - Fills the `"Birthday:"` field with `"2024-01-01"` using `page.get_by_label()`.
   - Clicks the `"Create"` button using `page.get_by_role()`.
3. Run pytest to confirm the interactions execute without errors:
   ```bash
   pytest
   ```

## Part 4: Auto-Waiting and Assertions

Playwright automatically waits for elements to be visible and actionable before interacting or asserting, eliminating the need for hardcoded `time.sleep()` calls.

Your Tasks:
1. Update `test_create_pet(page: Page)` in `tests/test_pet_shop.py` to add web-first assertions after clicking the `"Create"` button:
   - Locate the `#flash_message` element using `page.locator("#flash_message")` and verify its text equals `"Success"` using `expect(...).to_have_text()`.
   - Locate the `#search_results` element using `page.locator("#search_results")` and verify it contains both `"Buddy"` and `"Dog"` using `expect(...).to_contain_text()`.
2. Run the completed test script:
   ```bash
   pytest
   ```

## Part 5: Debugging with the Trace Viewer

When tests fail, Playwright provides a time-travel debugger called the Trace Viewer to inspect DOM snapshots, console logs, and network requests at every step.

Your Tasks:
1. Run your test suite with tracing enabled on failures:
   ```bash
   pytest --tracing=retain-on-failure
   ```
2. Intentionally break `test_create_pet` by changing the expected `#flash_message` text from `"Success"` to `"Failed"`, then run the same command again.
3. Open the generated trace archive in the Trace Viewer to inspect the exact moment of failure, the DOM snapshot, and the synced logs:
   ```bash
   playwright show-trace test-results\tests-test-pet-shop-py-test-create-pet-chromium\trace.zip
   ```
   *(Adjust the directory or file path if necessary for your OS/test name.)*
   
4. Revert the expected flash message back to `"Success"` and re-run `pytest` to confirm all tests pass.
