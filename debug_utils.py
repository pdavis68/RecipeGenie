import json
import os
import datetime
from typing import Any, Dict

def log_error(error_message: str, data: Any = None) -> None:
    """
    Log error information to a debug file
    
    Args:
        error_message: The error message to log
        data: Optional data to include in the log
    """
    debug_dir = "debug_logs"
    os.makedirs(debug_dir, exist_ok=True)
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{debug_dir}/error_{timestamp}.log"
    
    with open(filename, 'w') as f:
        f.write(f"ERROR: {error_message}\n\n")
        if data is not None:
            f.write("DATA:\n")
            try:
                if isinstance(data, dict) or isinstance(data, list):
                    f.write(json.dumps(data, indent=2))
                else:
                    f.write(str(data))
            except Exception as e:
                f.write(f"Could not serialize data: {str(e)}\n")
                f.write(f"Data type: {type(data)}\n")
                f.write(f"Data representation: {repr(data)}\n")

def save_recipe_data(recipe_data: Any) -> None:
    """
    Save recipe data for debugging purposes
    
    Args:
        recipe_data: The recipe data to save
    """
    debug_dir = "debug_logs"
    os.makedirs(debug_dir, exist_ok=True)
    
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{debug_dir}/recipe_data_{timestamp}.json"
    
    with open(filename, 'w') as f:
        try:
            if isinstance(recipe_data, dict):
                json.dump(recipe_data, f, indent=2)
            else:
                f.write(f"Non-dict data: {repr(recipe_data)}")
        except Exception as e:
            f.write(f"Error saving recipe data: {str(e)}\n")
            f.write(f"Data type: {type(recipe_data)}\n")
            f.write(f"Data representation: {repr(recipe_data)}\n")
