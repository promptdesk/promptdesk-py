# Contributing to PromptDesk

Thank you for your interest in contributing to PromptDesk Python SDK! Here's a step-by-step guide to get started:

## Setup

### Before you begin

Before you can start contributing, please ensure you have a PromptDesk development environment set up. If you haven't already, follow the [Contributing guide](https://promptdesk.ai/docs/contributing) to set up the PromptDesk development environment.

### Step 1: Fork the Repository

To contribute to PromptDesk, you'll need to fork the repository. Click on the "Fork" button at the top right corner of the repository page. This will create a copy of the repository under your GitHub account.

### Step 2: Clone the Repository

Once you have forked the repository, you'll need to clone it to your local machine. Open your terminal and navigate to the directory where you want to clone the repository. Then run the following command:

```
git clone git@github.com:your-username/promptdesk.git
```

Replace `your-username` with your GitHub username.

Go to the root directory of the cloned repository:

```
cd promptdesk-py
```

Open your favourite code editor to view source code files and make changes.

### Step 3: Setup Environment

Create a `.env` file in the root directory of the repository and add the following environment variables:

```
PROMPTDESK_API_KEY=[DEVELOPMENT_API_KEY]
OPEN_AI_KEY=[OPEN_AI_API_KEY]
```

### Step 4: Run Poetry Test

To ensure that your development environment is set up correctly, run the following command in your terminal:

```
poetry run pytest
```

You may need to install Poetry if you haven't already.

## Making Changes

### Step 1: Make Changes and Test

Now you're ready to make changes to the codebase. You can start by fixing bugs, adding new features, or improving the documentation. Make sure to create a new branch for your changes. You can do this by running the following command in your terminal:

```
git checkout -b my-branch-name
```

Replace `my-branch-name` with a descriptive name for your branch.

### Step 2: Submit a Pull Request

When you're ready to submit your changes, push your branch to your forked repository:

```
git push origin my-branch-name
```

Then, navigate to the repository on GitHub and click on the "New Pull Request" button. Follow the instructions to submit your pull request.

## Thank you!

If you have any questions or feedback please reach out to us at feedback@promptdesk.ai.

Thank you for your interest in contributing to PromptDesk! We appreciate your support.