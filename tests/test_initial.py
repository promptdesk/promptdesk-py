import promptdesk
import importlib.util
import pytest

def test_import():
    #make sure that the module is imported
    assert importlib.util.find_spec("promptdesk") is not None

def test_default_service_url():
    #make sure the default SERVICE_URL is set to the correct value
    assert promptdesk.SERVICE_URL == "http://localhost:4000"

def test_ping():
    #make sure that the service is running and responding to ping
    assert promptdesk.ping() == "pong"

def test_prompt_without_variables():
    #make sure that a non-variable prompt is generated correctly
    result = promptdesk.generate("yoda-test")
    assert "you" in result

#should generate an error because the plot variable is missing
def test_prompt_with_variable():
    with pytest.raises(ValueError) as e:

        result = promptdesk.generate("short-story-generator", {
            "setting": "a dark and stormy night",
            "character": "a mysterious stranger"
        })

        assert "A 'plot' value is required." in str(e.value)

#should generate an error because the plot variable is missing
def test_prompt_with_variable():
    with pytest.raises(ValueError) as e:

        result = promptdesk.generate("short-story-generator", {
            "setting": "a dark and stormy night",
            "plot": "knock on the door"
        })

        assert "A 'character' value is required." in str(e.value)

def test_prompt_with_variable():
    #make sure that a non-variable prompt is generated correctly
    result = promptdesk.generate("short-story-generator", {
        "setting": "a dark and stormy night",
        "character": "a mysterious stranger",
        "plot": "knock on the door"
    })
    print(result)
    #check if result contains more than 20 words
    assert len(result.split()) > 20