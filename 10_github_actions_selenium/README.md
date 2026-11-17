# Automated Acceptance Testing and Deployment Pipeline using GitHub Actions

We are going to build an Automated Acceptance Testing and Deployment Pipeline using GitHub Actions. By the end of this lab, you will have a pipeline that automatically:
1. Checks out the repository code and sets up Python.
2. Installs required dependencies (`flask`, `selenium`, `behave`, `requests`, etc.).
3. Boots up the Flask application in the background and verifies its availability.
4. Runs BDD / Acceptance tests using Behave and Selenium.
5. Generates an HTML test report and deploys it live to GitHub Pages.

## Part 1: Prepare Your Project

1. Ensure your repository contains the provided Flask application and acceptance test files structured correctly:
    ```text
    |- app.py
    |- behave.ini
    |- templates/
        |- index.html
    |- features/
        |- pet_shop.feature
        |- environment.py
        |- steps/
            |- pet_shop_steps.py
    ```
2. Ensure you have a `requirements.txt` file in your project root containing the necessary packages:
    ```text
    flask
    selenium
    behave
    behave-html-pretty-formatter
    requests
    ```
3. Commit these files and push them to your GitHub repository:
    ```bash
    git add .
    git commit -m "Add app and test files"
    git push origin main
    ```

## Part 2: Create the Workflow

GitHub looks for special workflow configuration files inside a specific directory structure.

1. Inside your project folder, create these nested folders:
    ```text
    |- .github/
        |- workflows/
    ```
2. Inside `.github/workflows/`, create a file named `behave_deploy.yaml`.
3. For now, create a basic "Hello World" version of the YAML file to test that your workflow triggers properly:
    ```yaml
    name: Acceptance Tests and Deployment Workflow

    on:
      push:
        branches: [main]

    jobs:
      deploy-report:
        runs-on: ubuntu-latest
        steps:
          - name: Say Hello
            run: echo "The workflow is working!"
    ```
4. Commit and push the file, then check the **Actions** tab on GitHub to confirm it runs.

## Part 3: Setting Up Code Checkout and Python Environment

Now, let's configure the runner to pull your repository and prepare the Python runtime.

1. Update your `behave_deploy.yaml` file with the checkout and setup steps, including the required GitHub Actions permissions:
    ```yaml
    name: Acceptance Tests and Deployment Workflow

    on:
      push:
        branches: [main]

    permissions:
      contents: read
      pages: write
      id-token: write

    jobs:
      deploy-report:
        runs-on: ubuntu-latest
        steps:
          - name: Checkout Code
            uses: actions/checkout@v3

          - name: Set up Python
            uses: actions/setup-python@v4
            with:
              python-version: '3.12'

          - name: Install Dependencies
            run: |
              python -m pip install --upgrade pip
              if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
    ```

## Part 4: Running the Flask App and Selenium/Behave Tests

Next, we need to run the web application locally on the runner and execute our browser-based acceptance tests against it.

1. Add the steps to start the Flask app in the background, poll it until it responds, run the Behave tests, and package the test report:
    ```yaml
          - name: Start Flask App
            run: |
              # The '&' runs the app in the background
              python app.py &
              
              # Wait for the server to be ready
              echo "Waiting for server..."
              for i in {1..10}; do
                curl -s http://127.0.0.1:5000 > /dev/null && echo "Server is up!" && break
                sleep 2
              done

          - name: Run Selenium Tests (Behave)
            run: behave -f html-pretty -o index.html

          - name: Upload Report
            if: always()
            uses: actions/upload-pages-artifact@v4
            with:
              path: .
    ```

## Part 5: Deploying the Test Report to GitHub Pages

Next, add a deployment job that publishes the generated test report (`index.html`) to GitHub Pages.

1. Append the `deploy` job to your `behave_deploy.yaml` file:
    ```yaml
      deploy:
        needs: deploy-report
        if: always()
        environment:
          name: github-pages
          url: ${{ steps.deployment.outputs.page_url }}
        runs-on: ubuntu-latest
        steps:
          - name: Setup Pages
            uses: actions/configure-pages@v5

          - name: Deploy to GitHub Pages
            id: deployment
            uses: actions/deploy-pages@v4
    ```
2. Commit and push your completed `behave_deploy.yaml` file to GitHub. Go to the **Actions** tab to watch the pipeline execute successfully and check your deployed GitHub Pages URL!


## Part 6: Add Badge to Readme Page

Finally, add a badge that shows the workflow status in the `README.md` file.

1. Add the following into the README.md file of your repository:
    ```
    # Pet Shop Application

    Build status:
    [![Acceptance Tests and Deployment Workflow](https://github.com/[YOUR_GITHUB_USERNAME]/[YOUR_REPO_NAME]/actions/workflows/[YOUR_YAML_FILE_NAME]/badge.svg)](https://github.com/[YOUR_GITHUB_USERNAME]/[YOUR_REPO_NAME]/actions/workflows/[YOUR_YAML_FILE_NAME])
    ```
    Replace [YOUR_GITHUB_USERNAME], [YOUR_REPO_NAME], and [YOUR_YAML_FILE_NAME] with appropriate strings.

2. Commit and push your completed `README.md` file to GitHub. Go to the **Code** tab to see the badge showing the status of your workflow!
