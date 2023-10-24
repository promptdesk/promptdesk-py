import promptdesk
import importlib.util
import pytest
import dotenv
import os

dotenv.load_dotenv()

def test_import():
    #make sure that the module is imported
    assert importlib.util.find_spec("promptdesk") is not None

def test_default_service_url():
    assert promptdesk.SERVICE_URL == "https://app.promptdesk.ai"

def test_ping():
    #make sure that the service is running and responding to ping
    assert promptdesk.ping() == "pong"

def test_prompt_without_api_key():
    with pytest.raises(Exception) as e:
        result = promptdesk.generate("yoda-test")
        assert "you" in result
    assert 'API_KEY is not set' in str(e.value)

def test_prompt_with_api_key():
    promptdesk.API_KEY = os.getenv("API_KEY")
    result = promptdesk.generate("yoda-test")
    assert "you" in result

#should generate an error because the plot variable is missing
def test_prompt_with_missing_variable():
    with pytest.raises(Exception) as e:

        result = promptdesk.generate("short-story", {
            "setting": "a dark and stormy night",
            "plot": "knock on the door"
        })

    assert 'Variable "character" not found in prompt.' in str(e.value)

def test_prompt_with_variable():
    #make sure that a non-variable prompt is generated correctly
    result = promptdesk.generate("short-story", {
        "setting": "a dark and stormy night",
        "character": "a mysterious stranger",
        "plot": "knock on the door"
    })
    print(result)
    #check if result contains more than 20 words
    assert len(result.split()) > 20

def test_convert_to_obj():
    assert promptdesk.convert_to_obj("{'a': 1}") == {'a': 1}
    assert promptdesk.convert_to_obj("[1, 2, 3]") == [1, 2, 3]
    assert promptdesk.convert_to_obj("     [1, 2, 3]   ") == [1, 2, 3]
    assert promptdesk.convert_to_obj("{\"a\": 1}") == {'a': 1}
    assert promptdesk.convert_to_obj('''{&apos;a&apos;\n\n\n
                                     : 1}''') == {'a': 1}