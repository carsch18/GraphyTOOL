# agents.py - Code Execution and Validation Agents

import os
import subprocess
import re
import tempfile

def validate_code(code: str) -> tuple[bool, str]:
    """Validate Manim code structure"""
    if not code or not code.strip():
        return False, "Empty code provided"
    
    # Check for basic Manim imports
    if "from manim import" not in code and "import manim" not in code:
        return False, "Missing Manim import statement"
    
    # Check for scene class
    if not re.search(r"class\s+\w+\s*\([^)]*Scene[^)]*\)", code):
        return False, "No Scene class found"
    
    # Check for construct method
    if "def construct(self)" not in code:
        return False, "Missing construct method"
    
    return True, "Code structure is valid"

def extract_scene_class(code: str) -> str:
    """Extract the scene class name from code"""
    match = re.search(r"class\s+(\w+)\s*\([^)]*Scene[^)]*\)", code)
    return match.group(1) if match else "DemoScene"

def clean_code(code: str) -> str:
    """Clean and extract Python code from markdown blocks"""
    # Remove markdown code blocks if present
    match = re.search(r"```python\n(.*?)```", code, re.DOTALL)
    if match:
        return match.group(1).strip()
    return code.strip()

def execute_code(code: str, quality: str = "720p") -> tuple[bool, str, str]:
    """
    Execute Manim code and return results
    
    Returns:
        (success: bool, result: str, log: str)
        - If success: result is video path, log is execution output
        - If failure: result is error reason, log is error details
    """
    
    # Step 1: Validate input
    if not code or not code.strip():
        return False, "Empty Code", "No code provided for execution"
    
    clean_code_content = clean_code(code)
    
    # Step 2: Validate code structure
    is_valid, validation_msg = validate_code(clean_code_content)
    if not is_valid:
        return False, "Invalid Code Structure", validation_msg
    
    # Step 3: Extract scene class name
    scene_class = extract_scene_class(clean_code_content)
    
    # Step 4: Create temporary file
    temp_dir = "temp_animations"
    os.makedirs(temp_dir, exist_ok=True)
    
    script_path = os.path.join(temp_dir, "demo_scene.py")
    with open(script_path, "w") as f:
        f.write(clean_code_content)
    
    # Step 5: Set up Manim execution
    quality_settings = {
        "480p": "-ql",
        "720p": "-qm", 
        "1080p": "-qh"
    }
    
    quality_flag = quality_settings.get(quality, "-qm")
    
    # Expected output path
    output_dir = os.path.join("media", "videos", "demo_scene")
    quality_subdir = {"480p": "480p15", "720p": "720p30", "1080p": "1080p60"}[quality]
    output_path = os.path.join(output_dir, quality_subdir, f"{scene_class}.mp4")
    
    # Step 6: Execute Manim
    command = ["manim", script_path, scene_class, quality_flag]
    
    try:
        # Ensure output directory exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Run Manim with timeout
        process = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=120,  # 2 minute timeout
            cwd=os.getcwd()
        )
        
        # Collect execution log
        execution_log = f"Command: {' '.join(command)}\n"
        execution_log += f"Return Code: {process.returncode}\n\n"
        execution_log += f"STDOUT:\n{process.stdout}\n\n"
        execution_log += f"STDERR:\n{process.stderr}"
        
        # Check if execution was successful
        if process.returncode == 0 and os.path.exists(output_path):
            return True, output_path, execution_log
        else:
            error_reason = "Manim Execution Failed"
            if process.returncode != 0:
                error_reason = f"Manim returned error code {process.returncode}"
            elif not os.path.exists(output_path):
                error_reason = "Output video file not found"
            
            return False, error_reason, execution_log
            
    except subprocess.TimeoutExpired:
        return False, "Execution Timeout", "Manim execution exceeded 2 minute timeout"
    
    except FileNotFoundError:
        return False, "Manim Not Found", "Manim is not installed or not in PATH"
    
    except Exception as e:
        return False, "Unexpected Error", f"An unexpected error occurred: {str(e)}"

def cleanup_temp_files():
    """Clean up temporary files"""
    temp_dir = "temp_animations"
    if os.path.exists(temp_dir):
        import shutil
        shutil.rmtree(temp_dir)