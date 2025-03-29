from jinja2 import PackageLoader

from cloecore.utils import templating_engine

package_loader = PackageLoader("cloecore.to_airflow", "templates")
env_air = templating_engine.get_jinja_env(package_loader)
