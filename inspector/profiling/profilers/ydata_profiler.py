import typing
from abc import ABCMeta

from ydata_profiling.config import Settings

from . import Profiler

if typing.TYPE_CHECKING:
    from ...systems.connectors.sql_connector import SQLConnector


class YDataProfiler(Profiler, metaclass=ABCMeta):
    connector: "SQLConnector"

    def prepare_config(self) -> Settings:
        user_settings = self.profile.parameters.get("settings", {})
        settings = Settings()
        settings.progress_bar = False
        settings.update(user_settings)

        return settings
