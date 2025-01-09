import mysql.connector
from dotenv import load_dotenv
import os
from utils.logger import get_logger

logger = get_logger(__name__)

def kill_all_connections():
    """Kill all existing MySQL connections for the current user before starting the application."""
    try:
        # Load environment variables
        load_dotenv()
        
        # Create a temporary connection to MySQL
        connection = mysql.connector.connect(
            host=os.getenv('DB_HOST'),
            user=os.getenv('DB_USER'),
            password=os.getenv('DB_PASSWORD'),
            database=os.getenv('DB_NAME'),
            port=int(os.getenv('DB_PORT', 3307))
        )
        
        cursor = connection.cursor()
        
        # Get all process IDs except the current connection
        cursor.execute("""
            SELECT id 
            FROM information_schema.processlist 
            WHERE user = %s 
            AND id != CONNECTION_ID()
        """, (os.getenv('DB_USER'),))
        
        process_ids = cursor.fetchall()
        
        # Kill each connection
        for process_id in process_ids:
            try:
                cursor.execute(f"KILL {process_id[0]}")
                logger.info(f"Killed connection: {process_id[0]}")
            except mysql.connector.Error as e:
                logger.warning(f"Could not kill connection {process_id[0]}: {e}")
        
        logger.info("Successfully cleaned up existing connections")
        
    except mysql.connector.Error as e:
        logger.error(f"Error managing connections: {e}")
    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'connection' in locals():
            connection.close()