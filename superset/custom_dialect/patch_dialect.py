import logging

from sqlalchemy.engine import reflection  
from sqlalchemy.dialects import registry
from sqlalchemy_dremio.flight import DremioDialect_flight
from sqlalchemy.types import ARRAY, String, Integer, Date, Boolean, Numeric  # import more types as necessary

# Define a custom type map that handles ARRAY and potentially other custom types
custom_type_map = {
    'ARRAY': ARRAY(String),  # Assuming array elements are strings; adjust as needed
    # Add other types as necessary
}
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

logger.info("Registering custom Dremio dialect...")



class CustomDremioDialect(DremioDialect_flight):
    @reflection.cache
    def get_columns(self, connection, table_name, schema=None, **kw):
        if schema:
            query = f"DESCRIBE \"{schema}\".\"{table_name}\""
        else:
            query = f"DESCRIBE \"{table_name}\""
        result = connection.execute(query)
        
        columns = []
        for col in result:
            col_name, col_type = col[0], col[1].upper()
            # Translate the Dremio type to a SQLAlchemy type
            sa_type = self.translate_type(col_type)
            
            # Append column information
            columns.append({
                "name": col_name,
                "type": sa_type,
                "nullable": True,  # Assuming all columns are nullable, adjust as needed
                "default": None    # Default values are typically not part of a DESCRIBE output
            })
        return columns

    def translate_type(self, dtype):
        # Custom mapping from Dremio type to SQLAlchemy type
        # Add or modify mappings based on actual Dremio types encountered
        type_map = {
            'VARCHAR': String,
            'INTEGER': Integer,
            'NUMERIC': Numeric,
            'DATE': Date,
            'BOOLEAN': Boolean,
            'ARRAY': lambda: ARRAY(String),  # Assuming arrays of strings, adjust as necessary
            # Add more types as necessary
        }
        return type_map.get(dtype, String)()  # Default to String if type is unknown



registry.register("dremio_custom.flight", "custom_dialect.patch_dialect", "CustomDremioDialect")


logger.info("Custom Dremio dialect registered successfully.")
