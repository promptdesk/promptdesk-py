<div align="center">
  <a href="https://promptdesk.ai" target="_blank">
  <div>
    <source media="(prefers-color-scheme: dark)" srcset="https://promptdesk.ai/branding/logo.png">
    <img alt="PromptDesk Logo" src="https://promptdesk.ai/branding/logo.png" width="280"/>
  </div>
  </a>
</div>

<br/>

<p align="center">
  <img src="https://github.com/promptdesk/promptdesk/actions/workflows/main.yml/badge.svg">
  <a href="https://pypi.org/project/promptdesk/">
    <img src="https://badge.fury.io/py/promptdesk.svg" alt="pypi">
  </a>
  <a href="https://www.npmjs.com/package/promptdesk">
    <img src="https://badge.fury.io/js/promptdesk.svg" alt="npm">
  </a>
  <a href="https://hub.docker.com/r/promptdesk/promptdesk">
    <img src="https://badgen.net/badge/icon/docker?icon=docker&label" alt="docker">
  </a>
  <a href="https://hub.docker.com/r/promptdesk/promptdesk">
    <img src="https://img.shields.io/docker/pulls/promptdesk/promptdesk.svg" alt="docker pulls">
  </a>
  <a href="https://www.gnu.org/licenses/agpl-3.0">
    <img src="https://img.shields.io/badge/License-AGPL_v3-blue.svg" alt="AGPLv3">
  </a>
</p>

<h1 align="center">Unlock Bold Innovation with Simplified AI</h1>

<div align="center">
PromptDesk is 100% free and open-source minimalist tool to facilitate the creation, organization, integration, and evaluation of prompts, prompt-based applications, agents and Large Language Models (LLMs).
</div>
    </br>
  <p align="center">
    <a href="https://promptdesk.ai/docs" rel="dofollow"><strong>Explore the docs »</strong></a>
    <br />
      <br/>
    <a href="https://promptdesk.ai/features">Features</a>
    ·
      <a href="https://promptdesk.ai/docs/walkthroughs">Walkthroughs</a>
    ·
  <a href="https://promptdesk.ai/podcast">Podcast</a>
    ·
    <a href="https://promptdesk.ai/articles">Articles</a>
    ·
    <a href="https://promptdesk.ai/contributors">Contributors</a>
    ·
    <a href="https://github.com/promptdesk/promptdesk/discussions">Community</a>
  </p>

  
  
  <p align="center">
  Available in: <a href="https://github.com/promptdesk/promptdesk-py">Python</a> - <a href="https://github.com/promptdesk/promptdesk-js">JavaScript</a>
  </p>
</div>

If you like this project, please consider giving this repo a ⭐️ star.

![Alt Text](https://promptdesk.ai/screenshots/completed-prompt.png)

## Features

- 🤝 Cross-team Collaboration
- 🔐 Data Privacy and Security
- 🌐 Any model, any scale
- 👨‍💻 Python and Javascript SDK
- 🏠 Local or Proxied Calls 
- 📈 Comprehensive Logs
- ♾️ Unlimited Models
- 🚀 Easy to set up and integrate (5 minutes)

## 🚀 Getting Started

We recommend starting with the [Quickstart guide](https://promptdesk.ai/docs/quickstart). You can also jump straight to [building prompts](https://promptdesk.ai/docs/building-prompts/) or start integrating prompts in [python](https://promptdesk.ai/docs/python-pip-package) or [javascript](https://promptdesk.ai/docs/javascript-npm-package).
### Quickstart

Run the following commands to install PromptDesk OS in your CLI:

```shell
wget https://raw.githubusercontent.com/promptdesk/promptdesk/main/quickstart/setup.sh
chmod +x setup.sh && ./setup.sh
```

**Please ensure that port 80 and 443 (optional) is available on your system. If you have a web server running, you may need to stop it before running the setup script.**

Open your web browser and navigate to [http://localhost](http://localhost), the IP address, or the domain name provided to access PromptDesk OS. Initial setup will require a valid OpenAI API key for installation testing purposes.

More installation options are available in the [PromptDesk OS GitHub Repository](https://github.com/promptdesk/promptdesk/tree/main/quickstart).

## Python SDK

To install PromptDesk, use pip:

```shell
pip install promptdesk
```

You can call the prompt you build in the application by using the generate method.

```python
from promptdesk import PromptDesk

pd = PromptDesk(
    api_key = "YOUR_PROMPTDESK_API_KEY", #find in /settings
    service_url = "http://localhost"
)

story = pd.generate("short-story-test", {
    "setting": "dark and stormy night",
    "character": "lonely farmer",
    "plot": "visited by a stranger"
})

print(story)
```

## 🔗 Important Links

For more information about PromptDesk, please refer to the following resources:

- [Documentation](https://promptdesk.ai/docs/)
- [Application GitHub Repository](https://github.com/promptdesk/promptdesk)
- [Python GitHub Repository](https://github.com/promptdesk/promptdesk-py)
- [PyPI Package](https://pypi.org/project/promptdesk/)
- [npm Package](https://www.npmjs.com/package/promptdesk)
- [Docker Hub](https://hub.docker.com/r/promptdesk/promptdesk/)
- [Official Website](https://promptdesk.ai/)
