from glik_plugin_local.core.entities.invocation import InvokeType
from glik_plugin_local.core.runtime import BackwardsInvocation
from glik_plugin_local.entities.model import EmbeddingInputType
from glik_plugin_local.entities.model.text_embedding import TextEmbeddingResult, TextEmbeddingModelConfig


class TextEmbeddingInvocation(BackwardsInvocation[TextEmbeddingResult]):
    def invoke(
        self,
        model_config: TextEmbeddingModelConfig,
        texts: list[str],
        input_type: EmbeddingInputType = EmbeddingInputType.QUERY,
    ) -> TextEmbeddingResult:
        """
        Invoke text embedding
        """
        for data in self._backwards_invoke(
            InvokeType.TextEmbedding,
            TextEmbeddingResult,
            {
                **model_config.model_dump(),
                "texts": texts,
                "input_type": input_type.value,
            },
        ):
            return data

        raise Exception("No response from text embedding")
