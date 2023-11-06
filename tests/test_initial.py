import promptdesk as pd
import importlib.util
import pytest
import dotenv
import os

dotenv.load_dotenv()

def test_import():
    #make sure that the module is imported
    assert importlib.util.find_spec("promptdesk") is not None

def test_default_service_url():
    assert pd.SERVICE_URL == "https://app.promptdesk.ai"

def test_ping():
    #make sure that the service is running and responding to ping
    assert pd.ping() == "pong"

def test_prompt_without_api_key():
    with pytest.raises(Exception) as e:
        result = pd.generate("yoda-test")
        assert "you" in result
    assert 'API_KEY is not set' in str(e.value)

def test_prompt_with_api_key():
    pd.API_KEY = os.getenv("API_KEY")
    result = pd.generate("yoda-test")
    assert "you" in result

def test_list():
    #make sure that the list of prompts is returned
    prompts = pd.list()
    assert len(prompts) > 0

#should generate an error because the plot variable is missing
def test_prompt_with_missing_variable():
    with pytest.raises(Exception) as e:

        result = pd.generate("short-story", {
            "setting": "a dark and stormy night",
            "plot": "knock on the door"
        })

    assert 'Variable "character" not found in prompt.' in str(e.value)

def test_prompt_with_variable():
    #make sure that a non-variable prompt is generated correctly
    result = pd.generate("short-story", {
        "setting": "a dark and stormy night",
        "character": "a mysterious stranger",
        "plot": "knock on the door"
    })
    #check if result contains more than 20 words
    assert len(result.split()) > 20

def test_convert_to_obj():
    assert pd.convert_to_obj("{'a': 1}") == {'a': 1}
    assert pd.convert_to_obj('{"a": 1}') == {'a': 1}
    assert pd.convert_to_obj("{\"a\": 1}") == {'a': 1}
    assert pd.convert_to_obj('''{&apos;a&apos;\n\n\n\t\t \t
                                     : 1}''') == {'a': 1}
    assert pd.convert_to_obj("[1, 2, 3]") == [1, 2, 3]
    assert pd.convert_to_obj("     [1, 2   , 3    ]   ") == [1, 2, 3]

def test_init_chain():
    chain = pd.Chain("test-chain")
    assert chain.name == "test-chain"
    assert chain.uuid != None
    assert "-" in chain.uuid

def test_prompt_with_chain():
    chain = pd.Chain("test-chain")
    result = pd.generate("yoda-test", chain=chain)
    assert "you" in result
    assert chain.uuid != None
    assert "-" in chain.uuid