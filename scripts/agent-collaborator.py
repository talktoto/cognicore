#!/usr/bin/env python3

import json
import subprocess
import sys
from typing import Dict, List, Optional

class AgentCollaborator:
    """CogniCore Multi-Agent Collaboration Framework"""
    
    def __init__(self):
        self.agents = {
            'techlead': {'complexity_threshold': 0.7, 'expertise': ['coding', 'architecture', 'debugging']},
            'pm': {'complexity_threshold': 0.5, 'expertise': ['planning', 'coordination', 'management']},
            'accountant': {'complexity_threshold': 0.3, 'expertise': ['finance', 'accounting', 'budgeting']},
            'chief_officer': {'complexity_threshold': 0.8, 'expertise': ['strategy', 'leadership', 'decision']}
        }
    
    def analyze_task(self, task_description: str) -> Dict:
        """Analyze task complexity and type"""
        # Simple keyword-based analysis for now
        complexity = 0.5  # Default medium complexity
        
        # Increase complexity for technical terms
        tech_keywords = ['code', 'debug', 'implement', 'develop', 'build', 'api', 'database']
        if any(keyword in task_description.lower() for keyword in tech_keywords):
            complexity = max(complexity, 0.7)
        
        # Determine task type
        if any(keyword in task_description.lower() for keyword in ['plan', 'schedule', 'manage']):
            task_type = 'planning'
        elif any(keyword in task_description.lower() for keyword in ['money', 'cost', 'budget', 'finance']):
            task_type = 'financial'
        elif any(keyword in task_description.lower() for keyword in ['code', 'program', 'develop', 'build']):
            task_type = 'technical'
        else:
            task_type = 'general'
            
        return {'complexity': complexity, 'type': task_type}
    
    def delegate_task(self, task_description: str) -> str:
        """Delegate task to appropriate agent"""
        analysis = self.analyze_task(task_description)
        complexity = analysis['complexity']
        task_type = analysis['type']
        
        # Find best agent based on expertise and complexity
        best_agent = 'xiaozhang'  # Default to main agent
        
        for agent_name, agent_info in self.agents.items():
            if complexity >= agent_info['complexity_threshold']:
                if task_type in [expertise.split('_')[0] if '_' in expertise else expertise 
                               for expertise in agent_info['expertise']]:
                    best_agent = agent_name
                    break
        
        return best_agent
    
    def execute_collaboration(self, task_description: str) -> Dict:
        """Execute multi-agent collaboration"""
        primary_agent = self.delegate_task(task_description)
        
        result = {
            'primary_agent': primary_agent,
            'task_analysis': self.analyze_task(task_description),
            'collaboration_plan': []
        }
        
        # Add collaboration steps if needed
        if primary_agent != 'xiaozhang':
            result['collaboration_plan'].append(f"Primary: {primary_agent}")
            result['collaboration_plan'].append("Review: xiaozhang")
        
        return result

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 agent-collaborator.py '<task_description>'")
        sys.exit(1)
    
    task = sys.argv[1]
    collaborator = AgentCollaborator()
    result = collaborator.execute_collaboration(task)
    
    print(json.dumps(result, indent=2, ensure_ascii=False))
