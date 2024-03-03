from promptdesk import PromptDesk, Chain
import importlib.util
import pytest
import dotenv
import os

dotenv.load_dotenv()

pd = PromptDesk(
    service_url="http://localhost:4000/",
    api_key=os.getenv("PROMPTDESK_API_KEY")
)

pd_wrong_service_url = PromptDesk(
    service_url="http://localhost:4001/",
    api_key=os.getenv("PROMPTDESK_API_KEY")
)

pd_wrong_api_key = PromptDesk(
    service_url="http://localhost:4000/",
    api_key="this_is_a_wrong_api_key"
)

def test_ping_wrong_service_url():
    with pytest.raises(Exception) as e:
        pd_wrong_service_url.ping()

def test_ping_wrong_api_key():
    with pytest.raises(Exception) as e:
        r = pd_wrong_api_key.ping()
        print(r)

def test_prompt_without_api_key():
    with pytest.raises(Exception) as e:
        pd_wrong_api_key.generate("yoda-test")

def test_prompt_with_missing_variable():
    with pytest.raises(Exception) as e:
        pd.generate("short-story-test", {
            "setting": "a dark and stormy night",
            "plot": "knock on the door",
        })

def test_prompt_with_non_existent_model():
    with pytest.raises(Exception) as e:
        pd.generate("this_model_does_not_exist", {
            "setting": "a dark and stormy night",
            "plot": "knock on the door"
        })