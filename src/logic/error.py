from src.custom_logging import setup_logger

logger = setup_logger(__name__)

class ProviderError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class LanguageError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class ContinueLoopError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)

class DownloadError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)