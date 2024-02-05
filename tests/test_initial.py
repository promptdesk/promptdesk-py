from promptdesk import PromptDesk, Chain
import importlib.util
import pytest
import dotenv
import os

dotenv.load_dotenv()

pd = PromptDesk(
    service_url="http://localhost:4000",
    api_key=os.getenv("PROMPTDESK_API_KEY")
)

def test_import():
    #make sure that the module is imported
    assert importlib.util.find_spec("promptdesk") is not None

def test_ping():
    #make sure that the service is running and responding to ping
    assert pd.ping() == "pong"

def test_prompt_without_api_key():
    pd_no_key = PromptDesk(
        api_key=None
    )
    with pytest.raises(Exception) as e:
        result = pd_no_key.generate("yoda-test")
        assert "you" in result or "Hello" in result
    #assert that error exists
    assert e.value is not None

def test_prompt_with_api_key():
    result = pd.generate("yoda-test")
    assert "you" in result or "Hello" in result

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

        print(result)

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

def test_prompt_with_variable_classification():
    #make sure that a non-variable prompt is generated correctly
    result = pd.generate("is_positive", {
        "text": "I am super happy"
    }, classification={
        True: ["positive", "happy"],
        False: ["negative", "sad"]
    })
    assert result == True
    result = pd.generate("is_positive", {
        "text": "I am super sad"
    }, classification={
        True: ["positive", "happy"],
        False: ["negative", "sad"]
    })
    assert result == False

def test_init_chain():
    pd.chain = Chain("test-chain")
    assert pd.chain.name == "test-chain"
    assert pd.chain.uuid != None
    assert "-" in pd.chain.uuid

def test_prompt_with_chain():
    pd.chain = Chain("test-chain")
    result = pd.generate("yoda-test")
    assert "you" in result or "Hello" in result
    assert pd.chain.uuid != None
    assert "-" in pd.chain.uuid

def test_cache():
    #this should take very little time since the result is cached
    result = None
    for x in range(1,100):
        result = pd.generate("short-story", {
            "setting": "a dark and stormy night",
            "character": "a mysterious stranger",
            "plot": "knock on the door"
        }, cache=True)
    #check if result contains more than 20 words
    assert len(result.split()) > 20

def test_prompt_local_promptdesk():
    local_pd = PromptDesk(
        service_url="http://localhost:4000",
        api_key=os.getenv("PROMPTDESK_API_KEY"),
        local=True,
        path="./tests/promptdesk"
    )
    assert os.path.exists("./tests/promptdesk")
    assert os.path.exists("./tests/promptdesk/prompts")
    assert os.path.exists("./tests/promptdesk/models")

def test_prompt_local_prompt():
    local_pd = PromptDesk(
        service_url="http://localhost:4000",
        api_key=os.getenv("PROMPTDESK_API_KEY"),
        local=True,
        path="./tests/promptdesk",
        env={
            "OPEN_AI_KEY": os.getenv("OPEN_AI_KEY")
        }
    )
    result = local_pd.generate("yoda-test")
    assert "you" in result or "Hello" in result

def test_prompt_local_prompt_with_variables():
    local_pd = PromptDesk(
        service_url="http://localhost:4000",
        api_key=os.getenv("PROMPTDESK_API_KEY"),
        local=True,
        path="./tests/promptdesk"
    )
    result = local_pd.generate("short-story", {
        "setting": "a dark and stormy night",
        "character": "a mysterious stranger",
        "plot": "knock on the door"
    }, env={
            "OPEN_AI_KEY": os.getenv("OPEN_AI_KEY")
    })
    #check if result contains more than 20 words
    assert len(result.split()) > 10

def test_convert_to_obj():
    assert pd.convert_to_obj("{'a': 1}") == {'a': 1}
    assert pd.convert_to_obj('{"a": 1}') == {'a': 1}
    assert pd.convert_to_obj("{\"a\": 1}") == {'a': 1}
    assert pd.convert_to_obj('''{&apos;a&apos;\n\n\n\t\t \t
                                     : 1}''') == {'a': 1}
    assert pd.convert_to_obj("[1, 2, 3]") == [1, 2, 3]
    assert pd.convert_to_obj("     [1, 2   , 3    ]   ") == [1, 2, 3]