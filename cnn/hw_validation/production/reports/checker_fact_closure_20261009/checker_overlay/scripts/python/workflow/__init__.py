"""仅覆盖经过本工程验证的规格入口，其他工作流仍使用原运行时。"""
from pkgutil import extend_path

__path__ = extend_path(__path__, __name__)
