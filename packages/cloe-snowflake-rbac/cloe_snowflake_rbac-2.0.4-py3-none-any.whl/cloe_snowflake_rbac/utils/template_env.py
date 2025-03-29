from jinja2 import Environment, PackageLoader

package_loader = PackageLoader("cloe_snowflake_rbac", "templates")
env_sql = Environment(loader=package_loader)
