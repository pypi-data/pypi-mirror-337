from jinja2 import Environment, PackageLoader

package_loader = PackageLoader("cloe_snowflake_feature_db_clone", "templates")
env_sql = Environment(loader=package_loader)
