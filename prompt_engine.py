# prompt_engine.py - AI Workflow Orchestrator

import os
import requests
import json
from agents import execute_code

def load_prompt_template(template_name: str) -> str:
    """Load prompt template from prompts directory"""
    try:
        template_path = os.path.join("prompts", f"{template_name}.txt")
        with open(template_path, "r") as f:
            return f.read()
    except Exception as e:
        return f"# ERROR: Could not load template {template_name}: {e}"

def stream_from_ollama(prompt: str, model: str):
    """Stream response from Ollama API"""
    try:
        data = {
            "model": model,
            "prompt": prompt,
            "stream": True
        }
        
        with requests.post("http://localhost:11434/api/generate", json=data, stream=True) as response:
            response.raise_for_status()
            
            for line in response.iter_lines():
                if line:
                    chunk = json.loads(line)
                    if 'response' in chunk:
                        yield "data", chunk['response']
                    if chunk.get('done'):
                        break
                        
    except Exception as e:
        yield "error", f"API call failed: {e}"

def run_generation_workflow(user_prompt: str, model: str):
    """
    Main AI workflow with self-healing capabilities
    """
    max_attempts = 3
    current_code = ""
    
    # Step 1: Initial code generation
    yield "status", "Generating initial code with AI..."
    
    template = load_prompt_template("generate")
    full_prompt = template.format(user_prompt=user_prompt)
    
    code_buffer = ""
    for event_type, chunk in stream_from_ollama(full_prompt, model):
        if event_type == "data":
            code_buffer += chunk
            yield "code_chunk", chunk
        else:
            yield "error", chunk
            return
    
    current_code = code_buffer
    yield "code_final", current_code
    
    # Step 2: Execution and self-healing loop
    for attempt in range(max_attempts):
        yield "status", f"Executing code (attempt {attempt + 1}/{max_attempts})..."
        
        success, result, log = execute_code(current_code)
        
        if success:
            yield "success", {
                "path": result,
                "log": log,
                "code": current_code
            }
            return
        
        # If failed, yield failure info
        yield "failure", {
            "reason": result,
            "log": log,
            "attempt": attempt + 1
        }
        
        # If this was the last attempt, give up
        if attempt >= max_attempts - 1:
            yield "final_failure", "Maximum attempts reached. Could not generate working code."
            return
        
        # Step 3: AI debugging
        yield "status", f"AI is debugging the code (attempt {attempt + 1})..."
        
        debug_template = load_prompt_template("debug")
        debug_prompt = debug_template.format(
            user_prompt=user_prompt,
            faulty_code=current_code,
            error_log=log
        )
        
        debug_code_buffer = ""
        for event_type, chunk in stream_from_ollama(debug_prompt, model):
            if event_type == "data":
                debug_code_buffer += chunk
                yield "code_chunk", chunk
            else:
                yield "error", chunk
                return
        
        current_code = debug_code_buffer
        yield "code_final", current_code