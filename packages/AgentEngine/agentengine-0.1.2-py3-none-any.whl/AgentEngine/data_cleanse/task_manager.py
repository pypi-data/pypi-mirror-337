import threading
import uuid
import json
import os
import time
import logging
from enum import Enum
from typing import Dict, List, Optional, Any
from concurrent.futures import ThreadPoolExecutor

# Task status enum
class TaskStatus(str, Enum):
    WAITING = "WAITING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FORWARDING = "FORWARDING"
    FAILED = "FAILED"

# Get logger for task manager
logger = logging.getLogger("data_cleanse.task_manager")

class TaskManager:
    def __init__(self, max_workers: int = 3, persistence_file: str = "tasks.json"):
        """
        Initialize the Task Manager
        
        Args:
            max_workers: Number of worker threads for parallel processing
            persistence_file: File path to persist task information
        """
        self.tasks = {}
        self.task_lock = threading.Lock()
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.persistence_file = persistence_file
        self.shutdown_flag = False
        
        # Load existing tasks if persistence file exists
        self._load_tasks()
        
        logger.info(f"Task Manager initialized with {max_workers} workers", 
                  extra={'task_id': ' ' * 36, 'stage': 'STARTUP', 'source': 'tmgr'})
    
    def create_task(self, task_data: Dict[str, Any]) -> str:
        """
        Create a new task and add it to the queue
        
        Args:
            task_data: Dictionary containing task parameters
            
        Returns:
            task_id: Unique identifier for the task
        """
        # Generate unique task ID
        task_id = str(uuid.uuid4())
        
        # Create task record
        task = {
            "id": task_id,
            "status": TaskStatus.WAITING,
            "created_at": time.time(),
            "updated_at": time.time(),
            "data": task_data,
            "result": None,
            "error": None,
            "sources": task_data.get("sources") if task_data.get("is_batch", False) else None
        }
        
        # Add task to tasks dictionary
        with self.task_lock:
            self.tasks[task_id] = task
            self._persist_tasks()
        
        logger.info(f"Created new task with data source: {task_data.get('source', 'batch')}", 
                  extra={'task_id': task_id, 'stage': 'CREATED', 'source': 'tmgr'})
        return task_id
    
    def get_task(self, task_id: str) -> Optional[Dict[str, Any]]:
        """
        Get task information by ID
        
        Args:
            task_id: Unique identifier for the task
            
        Returns:
            Task information or None if not found
        """
        with self.task_lock:
            task = self.tasks.get(task_id)
            if task:
                # Return a copy to prevent modification
                return task.copy()
            return None
    
    def get_all_tasks(self) -> List[Dict[str, Any]]:
        """
        Get all tasks
        
        Returns:
            List of all tasks
        """
        with self.task_lock:
            # Return a copy of tasks list
            return [task.copy() for task in self.tasks.values()]
    
    def update_task_status(self, task_id: str, status: TaskStatus, 
                          result: Any = None, error: str = None,
                          sources: List[Dict[str, Any]] = None) -> bool:
        """
        Update the status of a task
        
        Args:
            task_id: Unique identifier for the task
            status: New status of the task
            result: Result data if task is completed
            error: Error message if task failed
            sources: Source information for batch tasks
            
        Returns:
            True if task was updated, False otherwise
        """
        with self.task_lock:
            if task_id not in self.tasks:
                logger.warning(f"Attempted to update non-existent task", 
                             extra={'task_id': task_id, 'stage': 'UPDATE', 'source': 'tmgr'})
                return False
            
            old_status = self.tasks[task_id]["status"]
            self.tasks[task_id]["status"] = status
            self.tasks[task_id]["updated_at"] = time.time()
            
            if result is not None:
                self.tasks[task_id]["result"] = result
            
            if error is not None:
                self.tasks[task_id]["error"] = error
                
            if sources is not None:
                self.tasks[task_id]["sources"] = sources
            
            self._persist_tasks()
            
            logger.info(f"Updated task status from {old_status} to {status}", 
                      extra={'task_id': task_id, 'stage': str(status), 'source': 'tmgr'})
            return True
    
    def get_next_waiting_task(self) -> Optional[Dict[str, Any]]:
        """
        Get the next waiting task
        
        Returns:
            Next waiting task or None if no waiting tasks
        """
        with self.task_lock:
            for task_id, task in self.tasks.items():
                if task["status"] == TaskStatus.WAITING:
                    # Mark task as processing
                    self.tasks[task_id]["status"] = TaskStatus.PROCESSING
                    self.tasks[task_id]["updated_at"] = time.time()
                    self._persist_tasks()
                    
                    logger.info(f"Task assigned for processing", 
                              extra={'task_id': task_id, 'stage': 'PROCESSING', 'source': 'tmgr'})
                    return task.copy()
            return None
    
    def _persist_tasks(self) -> None:
        """Persist tasks to file"""
        try:
            # Make sure directory exists
            os.makedirs(os.path.dirname(os.path.abspath(self.persistence_file)), exist_ok=True)
            
            with open(self.persistence_file, 'w') as f:
                # Convert tasks to serializable format (enums to strings)
                serializable_tasks = {}
                for task_id, task in self.tasks.items():
                    serializable_task = task.copy()
                    if isinstance(serializable_task["status"], TaskStatus):
                        serializable_task["status"] = serializable_task["status"].value
                    serializable_tasks[task_id] = serializable_task
                
                json.dump(serializable_tasks, f)
        except Exception as e:
            logger.error(f"Error persisting tasks: {e}", 
                       extra={'task_id': ' ' * 36, 'stage': 'PERSIST', 'source': 'tmgr'})
    
    def _load_tasks(self) -> None:
        """Load tasks from file"""
        if not os.path.exists(self.persistence_file):
            return
        
        try:
            with open(self.persistence_file, 'r') as f:
                tasks_data = json.load(f)
                
                for task_id, task in tasks_data.items():
                    # Convert string status back to enum
                    if "status" in task and isinstance(task["status"], str):
                        task["status"] = TaskStatus(task["status"])
                    
                    self.tasks[task_id] = task
                
                logger.info(f"Loaded {len(tasks_data)} tasks from persistence file", 
                          extra={'task_id': ' ' * 36, 'stage': 'STARTUP', 'source': 'tmgr'})
        except Exception as e:
            logger.error(f"Error loading tasks: {e}", 
                       extra={'task_id': ' ' * 36, 'stage': 'STARTUP', 'source': 'tmgr'})
    
    def shutdown(self) -> None:
        """Shutdown the task manager"""
        self.shutdown_flag = True
        self.executor.shutdown()
        logger.info(f"Task Manager shutdown complete", 
                  extra={'task_id': ' ' * 36, 'stage': 'SHUTDOWN', 'source': 'tmgr'}) 