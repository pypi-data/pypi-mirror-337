from pydantic import BaseModel, ConfigDict

from glik_plugin_local.entities.model import BaseModelConfig, ModelType


class ModerationModelConfig(BaseModelConfig):
    """
    Model class for moderation model config.
    """

    model_type: ModelType = ModelType.MODERATION

    model_config = ConfigDict(protected_namespaces=())


class ModerationResult(BaseModel):
    """
    Model class for moderation result.
    """

    result: bool
