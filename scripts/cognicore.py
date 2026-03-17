#!/usr/bin/env python3

import os
import sys
import json
import subprocess
from datetime import datetime

class CogniCore:
    """Complete CogniCore Implementation"""
    
    def __init__(self, workspace_path=None):
        if workspace_path is None:
            # Use environment variable if set
            workspace_path = os.environ.get('COGNICORE_WORKSPACE')
            if workspace_path is None:
                # Default to current working directory
                workspace_path = os.getcwd()
        
        self.workspace = os.path.expanduser(workspace_path)
        self.scripts_dir = os.path.join(self.workspace, "scripts")
        self.memory_dir = os.path.join(self.workspace, "memory")
        self.learnings_dir = os.path.join(self.workspace, ".learnings")
        
        # Ensure directories exist
        os.makedirs(self.memory_dir, exist_ok=True)
        os.makedirs(self.learnings_dir, exist_ok=True)
    
    def write_memory(self, content: str, priority: str = "low") -> bool:
        """Write memory entry with FTS indexing"""
        try:
            date_str = datetime.now().strftime("%Y-%m-%d")
            time_str = datetime.now().strftime("%H:%M")
            
            # Write to daily memory file
            memory_file = os.path.join(self.memory_dir, f"{date_str}.md")
            with open(memory_file, "a", encoding="utf-8") as f:
                f.write(f"[{time_str}] [PRIORITY: {priority}] {content}\n")
            
            # Update FTS index
            memory_db_dir = os.path.expanduser("~/.openclaw/memory")
            memory_db = os.path.join(memory_db_dir, "xiaozhang.sqlite")
            
            if os.path.exists(memory_db):
                subprocess.run([
                    os.path.join(self.scripts_dir, "write-memory.sh"),
                    content, priority
                ], cwd=self.workspace, check=True)
            
            return True
        except Exception as e:
            print(f"Error writing memory: {e}")
            return False
    
    def search_memory(self, query: str) -> list:
        """Search memory using FTS"""
        try:
            result = subprocess.run([
                os.path.join(self.scripts_dir, "search-memory.sh"),
                query
            ], cwd=self.workspace, capture_output=True, text=True, check=True)
            
            # Parse results (simplified)
            lines = result.stdout.split('\n')
            results = []
            in_results = False
            
            for line in lines:
                if line.startswith("Results:"):
                    in_results = True
                    continue
                if in_results and line.strip() and not line.startswith("===="):
                    results.append(line.strip())
            
            return results
        except Exception as e:
            print(f"Error searching memory: {e}")
            return []
    
    def detect_learning(self, user_message: str) -> str:
        """Detect learning opportunities"""
        try:
            result = subprocess.run([
                os.path.join(self.scripts_dir, "learning-detector.sh"),
                user_message
            ], cwd=self.workspace, capture_output=True, text=True, check=True)
            
            return result.stdout.strip()
        except Exception as e:
            print(f"Error detecting learning: {e}")
            return "none"
    
    def collaborate(self, task_description: str) -> dict:
        """Multi-agent collaboration"""
        try:
            result = subprocess.run([
                sys.executable,
                os.path.join(self.scripts_dir, "agent-collaborator.py"),
                task_description
            ], cwd=self.workspace, capture_output=True, text=True, check=True)
            
            return json.loads(result.stdout)
        except Exception as e:
            print(f"Error in collaboration: {e}")
            return {"error": str(e)}
    
    def process_input(self, user_input: str) -> dict:
        """Process user input through CogniCore pipeline"""
        result = {
            "input": user_input,
            "learning_detected": None,
            "memory_searched": [],
            "collaboration_plan": None,
            "actions_taken": []
        }
        
        # 1. Detect learning opportunities
        learning_type = self.detect_learning(user_input)
        if learning_type != "none":
            result["learning_detected"] = learning_type
            result["actions_taken"].append(f"Detected {learning_type} opportunity")
        
        # 2. Search relevant memories
        if len(user_input) > 10:  # Only search for substantial queries
            memories = self.search_memory(user_input[:50])  # Use first 50 chars
            if memories:
                result["memory_searched"] = memories
                result["actions_taken"].append("Retrieved relevant memories")
        
        # 3. Plan collaboration if needed
        if len(user_input) > 20:  # Complex tasks
            collaboration = self.collaborate(user_input)
            if "error" not in collaboration:
                result["collaboration_plan"] = collaboration
                result["actions_taken"].append("Planned multi-agent collaboration")
        
        return result

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 cognicore.py '<user_input>'")
        sys.exit(1)
    
    user_input = sys.argv[1]
    core = CogniCore()
    result = core.process_input(user_input)
    
    print(json.dumps(result, indent=2, ensure_ascii=False))
