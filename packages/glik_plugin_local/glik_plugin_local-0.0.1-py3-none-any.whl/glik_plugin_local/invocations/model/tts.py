from binascii import unhexlify
from collections.abc import Generator

from glik_plugin_local.core.entities.invocation import InvokeType
from glik_plugin_local.core.runtime import BackwardsInvocation
from glik_plugin_local.entities.model.tts import TTSModelConfig, TTSResult


class TTSInvocation(BackwardsInvocation[TTSResult]):
    def invoke(self, model_config: TTSModelConfig, content_text: str) -> Generator[bytes, None, None]:
        """
        Invoke tts
        """
        for data in self._backwards_invoke(
            InvokeType.TTS,
            TTSResult,
            {
                **model_config.model_dump(),
                "content_text": content_text,
            },
        ):
            yield unhexlify(data.result)
