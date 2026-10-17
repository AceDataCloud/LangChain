"""Official LangChain standard unit suites. These do not issue network calls."""

from langchain_acedatacloud import AceAPIClient, ChatAceDataCloud
from langchain_gpt_image_acedatacloud import GPTImageGenerate
from langchain_happyhorse_acedatacloud import HappyHorseGenerate
from langchain_nano_banana_acedatacloud import NanoBananaGenerate
from langchain_seedance_acedatacloud import SeedanceGenerate
from langchain_suno_acedatacloud import SunoGenerate
from langchain_tests.unit_tests.chat_models import ChatModelUnitTests
from langchain_tests.unit_tests.tools import ToolsUnitTests


class TestChatAceDataCloudStandard(ChatModelUnitTests):
    @property
    def chat_model_class(self):
        return ChatAceDataCloud

    @property
    def chat_model_params(self):
        return {"api_key": "standard-test-key", "model": "gpt-4o-mini"}

    @property
    def init_from_env_params(self):
        return (
            {"ACEDATACLOUD_API_TOKEN": "env-test-key"},
            {"model": "gpt-4o-mini"},
            {"openai_api_key": "env-test-key", "model_name": "gpt-4o-mini"},
        )

    @property
    def has_structured_output(self):
        # Feature is not claimed until validated against actual account models.
        return False


class ServiceStandard(ToolsUnitTests):
    @property
    def tool_constructor_params(self):
        return {"client": AceAPIClient("standard-test-key")}

    @property
    def tool_invoke_params_example(self):
        return {"prompt": "sunrise"}


class TestSunoStandard(ServiceStandard):
    @property
    def tool_constructor(self):
        return SunoGenerate


class TestSeedanceStandard(ServiceStandard):
    @property
    def tool_constructor(self):
        return SeedanceGenerate


class TestHappyHorseStandard(ServiceStandard):
    @property
    def tool_constructor(self):
        return HappyHorseGenerate


class TestGPTImageStandard(ServiceStandard):
    @property
    def tool_constructor(self):
        return GPTImageGenerate


class TestNanoBananaStandard(ServiceStandard):
    @property
    def tool_constructor(self):
        return NanoBananaGenerate
