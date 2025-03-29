from jinja2 import PackageLoader

from .get_jinja_env import get_jinja_env

package_loader = PackageLoader("cloecore.utils", "Templates")
env = get_jinja_env(package_loader)
