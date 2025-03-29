import os
import sys
import argparse
import logging
import uvicorn
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Dict, List, Optional, Any
import time

from AgentEngine.data_cleanse.unstructured_core import DataCleanseCore, TaskLogFormatter
from AgentEngine.data_cleanse.task_manager import TaskStatus  # Import TaskStatus enum

# Configure logging using the formatter from unstructured_core
formatter = TaskLogFormatter()
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

# Configure root logger (if not already configured)
if not logging.root.handlers:
    logging.basicConfig(level=logging.INFO, handlers=[console_handler])
else:
    # If handlers exist, just set the level
    logging.root.setLevel(logging.INFO)
    # Add our handler if different from existing handlers
    if console_handler not in logging.root.handlers:
        logging.root.addHandler(console_handler)

logger = logging.getLogger("data_cleanse.service")

# Pydantic models for API
class TaskRequest(BaseModel):
    source: str
    source_type: str = "file"
    chunking_strategy: Optional[str] = None
    additional_params: Dict[str, Any] = Field(default_factory=dict)


class BatchTaskRequest(BaseModel):
    sources: List[Dict[str, Any]] = Field(..., description="List of source objects to process")


class TaskResponse(BaseModel):
    task_id: str


class BatchTaskResponse(BaseModel):
    task_ids: List[str]


class SimpleTaskStatusResponse(BaseModel):
    id: str
    status: str
    created_at: float
    updated_at: float
    error: Optional[str] = None


class SimpleTasksListResponse(BaseModel):
    tasks: List[SimpleTaskStatusResponse]


class TaskStatusUtil:
    """Utility class: Unified task status conversion handling"""
    
    @staticmethod
    def format_status_for_api(status_value) -> str:
        """
        Convert any status format to lowercase string format for API use
        
        Args:
            status_value: Any status value (enum or string)
            
        Returns:
            Lowercase status string for API response
        """
        # If enum, directly get value (already lowercase)
        if isinstance(status_value, TaskStatus):
            return status_value.value
            
        # If string, ensure lowercase
        return str(status_value).lower()
    
    @staticmethod
    def has_result(task: Dict[str, Any]) -> bool:
        """
        Check if a task should contain result data
        
        Args:
            task: Task information dictionary
            
        Returns:
            True if task result should be returned
        """
        status = task.get("status")
        result_exists = "result" in task and task["result"]
        
        # Only return True if status is completed or forwarding, and result exists
        if isinstance(status, TaskStatus):
            return (status in [TaskStatus.COMPLETED, TaskStatus.FORWARDING]) and result_exists
        
        # String status handling
        status_str = str(status).lower()
        return status_str in ["completed", "forwarding"] and result_exists
    
    @staticmethod
    def get_status_display(task: Dict[str, Any]) -> Dict[str, Any]:
        """
        Get task status information for frontend display
        
        Args:
            task: Task information dictionary
            
        Returns:
            Dictionary containing status information suitable for frontend display
        """
        # Get API format status (lowercase)
        status = TaskStatusUtil.format_status_for_api(task["status"])
        
        # Build basic response
        response = {
            "task_id": task["id"],
            "status": status,
            "created_at": task["created_at"],
            "updated_at": task["updated_at"]
        }
        
        # Add result (if exists and status allows)
        if TaskStatusUtil.has_result(task):
            response["result"] = task.get("result")
        
        # Add error message (if exists)
        if task.get("error"):
            response["error"] = task["error"]
        
        return response


class DataCleanseService:
    def __init__(self, host: str = "0.0.0.0", port: int = 8001, 
                 num_workers: int = 3, persistence_dir: str = "data"):
        """
        Initialize the Data Cleanse Service
        
        Args:
            host: Host to bind to
            port: Port to bind to
            num_workers: Number of worker threads for parallel processing
            persistence_dir: Directory to persist task information
        """
        self.host = host
        self.port = port
        self.persistence_dir = persistence_dir
        
        # Initialize core
        self.core = DataCleanseCore(
            num_workers=num_workers,
            persistence_dir=persistence_dir
        )
        
        # Create FastAPI app
        self.app = self._create_app()
    
    def _create_app(self) -> FastAPI:
        """Create FastAPI application"""
        app = FastAPI(
            title="Data Cleanse API",
            description="API for data cleansing using Unstructured partitioning",
            version="0.1.0"
        )
        
        # Start service on application startup
        @app.on_event("startup")
        async def startup_event():
            self.core.start()
        
        # Shutdown service on application shutdown
        @app.on_event("shutdown")
        async def shutdown_event():
            self.core.stop()
        
        # API Endpoints
        @app.post("/tasks", response_model=TaskResponse, status_code=201)
        async def create_task(request: TaskRequest):
            """
            Create a new data cleansing task
            
            Creates a data cleansing task and immediately returns the task ID. 
            The task will be processed asynchronously in the background,
            and will be forwarded to Elasticsearch service upon completion.
            
            After processing, the task status will change to forwarding, then 
            automatically forwarded to Elasticsearch, and finally the status 
            will become completed or failed.
            """
            # Extract parameters
            params = {}
            if request.additional_params:
                params.update(request.additional_params)
            
            # Create task directly - no need to wait for processing
            start_time = time.time()
            task_id = self.core.create_task(
                source=request.source,
                source_type=request.source_type,
                chunking_strategy=request.chunking_strategy,
                **params
            )
            logger.info(f"Task creation took {(time.time() - start_time)*1000:.2f}ms", 
                       extra={'task_id': task_id, 'stage': 'API-CREATE', 'source': 'service'})
            
            return TaskResponse(task_id=task_id)
        
        @app.post("/tasks/batch", response_model=BatchTaskResponse, status_code=201)
        async def create_batch_tasks(request: BatchTaskRequest):
            """
            Create a batch of data cleansing tasks
            
            Creates multiple data cleansing tasks and immediately returns the task ID list.
            Tasks will be processed asynchronously in the background,
            and will be forwarded to Elasticsearch service upon completion.
            
            After processing, each task status will change to forwarding, then 
            automatically forwarded to Elasticsearch, and finally the status 
            will become completed or failed.
            """
            # Create batch tasks directly - no need to wait for processing
            start_time = time.time()
            batch_id = f"batch-{int(time.time())}"
            
            logger.info(f"Processing batch request with {len(request.sources)} sources", 
                       extra={'task_id': batch_id, 'stage': 'API-BATCH', 'source': 'service'})
            
            task_ids = self.core.create_batch_tasks(request.sources)
            
            elapsed_ms = (time.time() - start_time) * 1000
            logger.info(f"Batch task creation took {elapsed_ms:.2f}ms for {len(task_ids)} tasks", 
                       extra={'task_id': batch_id, 'stage': 'API-BATCH', 'source': 'service'})
            
            return BatchTaskResponse(task_ids=task_ids)
        
        @app.get("/tasks/{task_id}", response_model=SimpleTaskStatusResponse)
        async def get_task(task_id: str):
            """Get task status (without results and metadata)"""
            task = self.core.get_task(task_id)
            
            if not task:
                raise HTTPException(status_code=404, detail=f"Task with ID {task_id} not found")
            
            # Get status and convert to lowercase - using utility class
            status = TaskStatusUtil.format_status_for_api(task["status"])
            
            return SimpleTaskStatusResponse(
                id=task["id"],
                status=status,
                created_at=task["created_at"],
                updated_at=task["updated_at"],
                error=task.get("error")
            )
        
        @app.get("/tasks", response_model=SimpleTasksListResponse)
        async def list_tasks():
            """List all tasks (without results and metadata)"""
            tasks = self.core.get_all_tasks()
            
            task_responses = []
            for task in tasks:
                # Use unified status conversion method
                status = TaskStatusUtil.format_status_for_api(task["status"])
                
                task_responses.append(
                    SimpleTaskStatusResponse(
                        id=task["id"],
                        status=status,
                        created_at=task["created_at"],
                        updated_at=task["updated_at"],
                        error=task.get("error")
                    )
                )
            
            return SimpleTasksListResponse(tasks=task_responses)
        
        @app.get("/healthcheck")
        async def healthcheck():
            """Health check endpoint to verify if the service is running."""
            return {"status": "ok", "message": "Data cleanse service is running"}
        
        @app.get("/tasks/{task_id}/details")
        async def get_task_details(task_id: str):
            """Get task status and results."""
            task = self.core.get_task(task_id)
            
            if not task:
                raise HTTPException(status_code=404, detail="Task not found")
            
            # Use utility method to get formatted task status information
            return TaskStatusUtil.get_status_display(task)
        
        return app
    
    def start(self):
        """Start the service"""
        service_id = f"service-{int(time.time())}"
        logger.info(f"Starting Data Cleanse Service - Host: {self.host}:{self.port} - Workers: {self.core.task_manager.executor._max_workers}", 
                   extra={'task_id': service_id, 'stage': 'STARTUP', 'source': 'service'})
        logger.info(f"Task data will be stored in: '{self.persistence_dir}'", 
                   extra={'task_id': service_id, 'stage': 'STARTUP', 'source': 'service'})
        
        try:
            # Start the uvicorn server
            uvicorn.run(self.app, host=self.host, port=self.port)
        except KeyboardInterrupt:
            logger.info("Service terminated by user", 
                       extra={'task_id': service_id, 'stage': 'SHUTDOWN', 'source': 'service'})
        except Exception as e:
            logger.error(f"Error starting service: {e}", 
                        extra={'task_id': service_id, 'stage': 'ERROR', 'source': 'service'})
            sys.exit(1)
        finally:
            self.core.stop()


def main():
    """Main entry point for the data cleansing service"""
    # Check if no arguments are provided and use defaults
    if len(sys.argv) == 1:
        # Start with default parameters
        service = DataCleanseService()
        return service.start()
    
    # Parse arguments
    parser = argparse.ArgumentParser(description="Data Cleanse Service")
    
    # Add command line arguments
    parser.add_argument("--host", default="0.0.0.0", help="Host address to bind to")
    parser.add_argument("--port", type=int, default=8001, help="Port to bind to")
    parser.add_argument("--workers", type=int, default=3, help="Number of worker threads")
    parser.add_argument("--data-dir", default="task_data", help="Directory to store task data")
    
    # Parse arguments
    args = parser.parse_args()
    
    # Start the server with parsed arguments
    service = DataCleanseService(
        host=args.host,
        port=args.port,
        num_workers=args.workers,
        persistence_dir=args.data_dir
    )
    service.start()


if __name__ == "__main__":
    main() 