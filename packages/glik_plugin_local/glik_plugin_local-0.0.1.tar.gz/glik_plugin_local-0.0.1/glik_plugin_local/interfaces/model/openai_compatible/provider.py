import logging

from glik_plugin_local.interfaces.model import ModelProvider

logger = logging.getLogger(__name__)


class OAICompatProvider(ModelProvider):
    def validate_provider_credentials(self, credentials: dict) -> None:
        pass
