from pydantic import BaseModel, ConfigDict

from glik_plugin_local.entities.model import BaseModelConfig, ModelType


class Speech2TextModelConfig(BaseModelConfig):
    """
    Model class for speech2text model config.
    """

    model_type: ModelType = ModelType.SPEECH2TEXT

    model_config = ConfigDict(protected_namespaces=())


class Speech2TextResult(BaseModel):
    """
    Model class for rerank result.
    """

    result: str
