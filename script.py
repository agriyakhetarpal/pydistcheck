import subprocess
import tempfile
import os
import shutil

def check_debug_symbols_in_static_lib(library_path):
    # Create temporary directory
    temp_dir = tempfile.mkdtemp()
    try:
        # Extract all object files from the archive
        subprocess.run(['ar', 'x', library_path], cwd=temp_dir, check=True)
        
        has_debug_symbols = False
        # Check each object file
        for obj_file in os.listdir(temp_dir):
            if obj_file.endswith('.o'):
                obj_path = os.path.join(temp_dir, obj_file)
                result = subprocess.run(
                    ['readelf', '-S', obj_path], 
                    capture_output=True, 
                    text=True
                )
                
                if '.debug_' in result.stdout:
                    print(f"Debug symbols found in {obj_file}")
                    has_debug_symbols = True
        
        return has_debug_symbols
    finally:
        # Clean up
        shutil.rmtree(temp_dir)

# Usage
check_debug_symbols_in_static_lib("./librmm_cu12-24.10.0-py3-none-any/librmm/lib64/libspdlog.a")