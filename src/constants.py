# sql check, set, create, drop schema
CHECK_SCHEMA_SQL = 'SELECT EXISTS(SELECT 1 FROM information_schema.schemata WHERE schema_name = \'public\') as result'  # noqa Q003
CREATE_SCHEMA = 'CREATE SCHEMA "public"'
DROP_SCHEMA = 'DROP SCHEMA "public" cascade'

BASIC_HEADERS = {'Content-Type': 'application/json'}
ALEMBIC_INI_FILE = 'alembic.ini'
ALEMBIC_INI_SCRIPT_LOCATION = 'src/infra/adapters/database/migration'
ALEMBIC_INI_VERSION_LOCATIONS = 'src/infra/adapters/database/migration/versions'
DEFAULT_SORT_COLUMN = 'id'
DEFAULT_SORT_TYPE = 'desc'
DEFAULT_OFFSET = 0
ORDER_BY_DESC = 'desc'
ORDER_BY_ASC = 'asc'

# as a query criteria for Trace to logs
COMPOSE_SERVICE = 'compose_service'
