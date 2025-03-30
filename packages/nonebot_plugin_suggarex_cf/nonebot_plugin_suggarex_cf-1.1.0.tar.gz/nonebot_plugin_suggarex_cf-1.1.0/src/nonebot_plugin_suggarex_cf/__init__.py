from nonebot.plugin import PluginMetadata
from nonebot.plugin import require, PluginMetadata

__plugin_meta__ = PluginMetadata(
    name="SuggarChat CloudFlare协议扩展附属插件",
    description="适用于SuggarChat插件的CloudFlare协议适配器实现，SuggarChat附属插件",
    usage="",
    type="library",
    homepage="https://github.com/JohnRichard4096/nonebot_plugin_suggaradapter_cf",
    supported_adapters={"~onebot.v11"},
)

require("nonebot_plugin_suggarchat")

from .core import *
