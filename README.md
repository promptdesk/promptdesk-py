# PromptDesk Python SDK

## Overview

PromptDesk Python SDK is a pip package designed to facilitate the dynamic integration, development, optimization, and assessment of prompts and large language models (LLMs) within your Python applications.

## Installation

To install PromptDesk, use pip:

```bash
pip install promptdesk
```

## Usage

### Pinging the Service

Make sure the PromptDesk service is running by pinging it:

```python
import promptdesk

promptdesk.SERVICE_URL = "http://localhost:4000"

pong = promptdesk.ping()

print(pong)  # Should print "pong"
```

The SERVICE_URL defaults to "http://localhost:4000", so you can omit this line if you are running the service locally.

### Generating Text

You can generate text by using the generate method.

```python
import promptdesk

yoda_response = promptdesk.generate("yoda-test")

print(yoda_response)
```

Sample output:
```bash
Hmm, hello there, I am. Fine, I am. And you?
```

### Generating Text with Variables

You can generate text with variables by passing a dictionary of variables as the second argument to the generate method.

```python
import promptdesk

story = promptdesk.generate("short-story-generator", {
    "setting": "A dark and stormy night",
    "character": "A lonely farmer",
    "plot": "A farmer is visited by a stranger"
})

print(story)
```

Sample output:
```bash
On a dark and stormy night, a lonely farmer was tending to his crops, the sound of thunder echoing through the desolate fields. As lightning flashed, illuminating the eerie landscape, a mysterious stranger knocked on the farmers door seeking refuge from the tempestuous night. The farmer, wary but compassionate, welcomed the stranger, unknowingly inviting a twist of fate into his secluded existence.
```