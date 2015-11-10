from .config import Config
from . import exceptions


class WithConfig(object):

    """Ensure that a config is present and valid."""

    CONFIG_REQUIRES = ('api_key', 'token')

    def __init__(self, config=None):

        self.config = config or Config.read()

        if self.config is None:
            raise exceptions.ConfigNotFoundError

        if not all([self.config.get(key) for
                    key in self.CONFIG_REQUIRES]):
            raise exceptions.ConfigValueError(required=self.CONFIG_REQUIRES)
