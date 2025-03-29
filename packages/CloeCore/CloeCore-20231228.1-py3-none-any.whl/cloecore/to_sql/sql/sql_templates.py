from jinja2 import PackageLoader

from cloecore.utils import templating_engine

package_loader = PackageLoader("cloecore.to_sql.sql", "Templates")
env_sql = templating_engine.get_jinja_env(package_loader)
