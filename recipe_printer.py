import tempfile
import os
import subprocess
from typing import Dict, Any

def print_recipe(recipe_data: Dict[str, Any], formatted_text: str) -> None:
    """Print the recipe to the default printer"""
    # Create a temporary file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.txt', mode='w') as temp_file:
        temp_file.write(f"{recipe_data['title']}\n\n")
        temp_file.write(f"{recipe_data['description']}\n\n")
        temp_file.write(formatted_text)
        temp_file_path = temp_file.name
    
    try:
        # Print the file using the system's default print command
        if os.name == 'nt':  # Windows
            os.startfile(temp_file_path, 'print')
        else:  # Linux/Mac
            subprocess.run(['lpr', temp_file_path])
    except Exception as e:
        print(f"Error printing: {e}")
    finally:
        # Clean up the temporary file
        try:
            os.unlink(temp_file_path)
        except:
            pass
