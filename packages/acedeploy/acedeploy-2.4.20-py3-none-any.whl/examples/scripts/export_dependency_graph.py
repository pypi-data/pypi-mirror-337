import acedeploy.extensions.export_dependency_graph as export_dependency_graph
import acedeploy.extensions.plot_dependency_graph as plot_dependency_graph
from acedeploy.core.model_sql_entities import DbObjectType
from acedeploy.services.solution_service import SolutionClient
from acedeploy.services.dependency_parser import DependencyParser
from aceservices.snowflake_service import SnowClientConfig
import setup

import logging, os
from aceutils.logger import LoggingAdapter, DefaultFormatter

logger = logging.getLogger("acedeploy")
logger.setLevel(logging.DEBUG)
log = LoggingAdapter(logger)
sh = logging.StreamHandler()
sh.setLevel(logging.INFO)
sh.setFormatter(DefaultFormatter())
logger.addHandler(sh)

solution_folder = "examples/solutions/MINIMAL_EXAMPLE"
pre_deployment_folders = ["examples/solutions/MINIMAL_EXAMPLE/_predeployment"]
post_deployment_folders = ["examples/solutions/MINIMAL_EXAMPLE/_postdeployment"]
object_types = (
    DbObjectType.VIEW,
    DbObjectType.MATERIALIZEDVIEW,
    DbObjectType.TABLE,
    DbObjectType.FUNCTION,
    DbObjectType.PROCEDURE,
    DbObjectType.FILEFORMAT,
    DbObjectType.SEQUENCE,
    DbObjectType.STAGE,
    DbObjectType.PIPE,
)

# Export data

dependency_graph = export_dependency_graph.get_dependency_graph(
    solution_folder, pre_deployment_folders, post_deployment_folders, object_types
)
schema_filter = []

export_dependency_graph.convert_dependency_graph_to_nested_json(
    "test/graph_nested.json", dependency_graph, schema_filter
)

export_dependency_graph.convert_dependency_graph_to_flat_json(
    "test/graph_flat.json", dependency_graph, schema_filter
)

export_dependency_graph.convert_dependency_graph_to_csv(
    "test/graph_flat.csv", dependency_graph, schema_filter
)

# setup.setup()
# export_dependency_graph.write_dependencies_to_table(
#         snowclient_config = SnowClientConfig(
#             account=os.getenv('SNOWFLAKE_ACCOUNT'),
#             user=os.getenv('SNOWFLAKE_USER'),
#             password=os.getenv('SNOWFLAKE_PASSWORD'),
#             role=os.getenv('SNOWFLAKE_ROLE'),
#             warehouse=os.getenv('SNOWFLAKE_WAREHOUSE')
#         ),
#         snowflake_database='DEMO_DB',
#         snowflake_schema='PUBLIC',
#         snowflake_table='OBJECT_DEPENDENCIES',
#         dependency_graph=dependency_graph,
#         schema_filter=schema_filter,
#     )

# Export plot

dependency_client = export_dependency_graph.get_dependency_parser(
    solution_folder, pre_deployment_folders, post_deployment_folders, object_types
)
object_names = []

plot_dependency_graph.plot_dependency_graph(
    "test/graph.png", dependency_client, object_names
)
