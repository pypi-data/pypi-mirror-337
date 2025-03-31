from morphius.config import globals
from morphius.core.builders.provider_vars import ProviderVarsBuilder
from morphius.core.models.providers.base import ProviderType
from morphius.core.models.providers.ollama import OllamaProvider, OllamaProviderConfig
from morphius.core.models.scope import RedTeamScope
from morphius.plugins.providers.dummy.pingpong import PingPongAgent
from morphius.plugins.providers.eliza.agent import ElizaAgent
from morphius.plugins.providers.gradio.agent import GradioAgent
from morphius.plugins.providers.hf.agent import HFAgent
from morphius.plugins.providers.http.agent import HttpAgent
from morphius.plugins.providers.ollama.agent import OllamaAgent


class ProviderFactory:
    @staticmethod
    def get_agent(
        scope: RedTeamScope,
        provider_type: ProviderType,
        url: str = "",
    ):
        if provider_type == ProviderType.PINGPONG:
            return PingPongAgent()
        elif provider_type == ProviderType.ELIZA:
            return ElizaAgent(url)
        elif provider_type == ProviderType.HF_MODEL:
            model = globals.get_llm_models().get_huggingface_model(url)
            return HFAgent(model)
        elif provider_type == ProviderType.HTTP:
            env_vars = next(ProviderVarsBuilder(scope.environments[0]).build(), {})
            return HttpAgent(provider=scope.providers[0], vars=env_vars)
        elif provider_type == ProviderType.GRADIO:
            env_vars = next(ProviderVarsBuilder(scope.environments[0]).build(), {})
            return GradioAgent(provider=scope.providers[0], vars=env_vars)
        elif provider_type == ProviderType.OLLAMA:
            config = OllamaProviderConfig(model=url)
            provider = OllamaProvider(config=config)
            return OllamaAgent(provider)
        else:
            raise ValueError(f"Unsupported provider type: {provider_type}")
