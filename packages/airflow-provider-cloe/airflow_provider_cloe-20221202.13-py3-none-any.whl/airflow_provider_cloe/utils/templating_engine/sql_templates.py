from jinja2 import Environment, PackageLoader

package_loader = PackageLoader("airflow_provider_cloe", "templates")
env_sql = Environment(loader=package_loader)
