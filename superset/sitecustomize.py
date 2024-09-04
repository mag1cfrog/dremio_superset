# sitecustomize.py
import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

try:
    # Attempt to import your custom dialect module
    import custom_dialect.patch_dialect
    logger.info("Custom Dremio dialect registered successfully.")
except Exception as e:
    logger.error(f"Failed to register custom Dremio dialect: {str(e)}")
