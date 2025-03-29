import threading
import time
import os
import json
import logging
import httpx
from typing import Dict, List, Optional, Any
from unstructured.partition.auto import partition
from dotenv import load_dotenv

from task_manager import TaskManager, TaskStatus

# Load environment variables
load_dotenv()

# Configure logging with custom formatter
class TaskLogFormatter(logging.Formatter):
    """
    Custom formatter for standardized task logging across all data cleanse modules.
    
    This formatter ensures consistent logging format for all task operations:
    LEVEL    - SOURCE  - TASK ID                         - STAGE      - MESSAGE
    
    Use this formatter in all data cleanse related modules to maintain consistency.
    """
    def format(self, record):
        # Default placeholder values
        task_id = getattr(record, 'task_id', ' ' * 36)
        stage = getattr(record, 'stage', ' ' * 10)
        source = getattr(record, 'source', 'core')
        
        # Create the formatted message
        return f"{record.levelname:7s} - {source:7s} - TASK {task_id:36s} - {stage:10s} - {record.msg}"

# Set up the formatter and handler for this module
formatter = TaskLogFormatter()
console_handler = logging.StreamHandler()
console_handler.setFormatter(formatter)

# Configure root logger
logging.basicConfig(level=logging.INFO, handlers=[console_handler])

# Disable some INFO logs
logging.getLogger("pypandoc").setLevel(logging.WARNING)
logging.getLogger("httpx").setLevel(logging.WARNING)

# Setup our logger
logger = logging.getLogger("data_cleanse.core")

class DataCleanseCore:
    def __init__(self, 
                 num_workers: int = 3, 
                 persistence_dir: str = "data",
                 poll_interval: float = 0.1):  # Reduced polling interval to improve responsiveness
        """
        Initialize the Data Cleanse Core
        
        The data cleansing process uses an integrated design that combines data cleansing 
        and forwarding to Elasticsearch into a single process, avoiding state management issues
        in multi-threaded/asynchronous environments. The process follows the state transitions:
        
        WAITING -> PROCESSING -> FORWARDING -> COMPLETED
        
        Args:
            num_workers: Number of worker threads for parallel processing
            persistence_dir: Directory to persist task information
            poll_interval: Interval in seconds to poll for new tasks
        """
        # Create persistence directory if it doesn't exist
        os.makedirs(persistence_dir, exist_ok=True)
        
        # Initialize task manager
        persistence_file = os.path.join(persistence_dir, "tasks.json")
        self.task_manager = TaskManager(max_workers=num_workers, 
                                        persistence_file=persistence_file)
        
        # Initialize worker threads
        self.poll_interval = poll_interval
        self.workers = []
        self.running = False
        
        # Get Elasticsearch service URL
        self.es_service_url = os.environ.get("ELASTICSEARCH_SERVICE", "http://localhost:8000")
        self.default_embedding_dim = 1024  # Default embedding dimension
        self.default_index_name = "knowledge_base"  # Default index name
    
    def start(self) -> None:
        """Start the data cleanse core"""
        if self.running:
            return
        
        logger.info("Starting Data Cleanse Core", 
                   extra={'task_id': ' ' * 36, 'stage': 'STARTUP', 'source': 'core'})
        self.running = True
        
        # Start worker threads
        for i in range(self.task_manager.executor._max_workers):
            worker = threading.Thread(
                target=self._worker_loop,
                name=f"Worker-{i+1}",
                daemon=True
            )
            worker.start()
            self.workers.append(worker)
            logger.info(f"Started worker thread: {worker.name}", 
                       extra={'task_id': ' ' * 36, 'stage': 'STARTUP', 'source': 'core'})
    
    def stop(self) -> None:
        """Stop the data cleanse core"""
        if not self.running:
            return
        
        logger.info("Stopping Data Cleanse Core", 
                   extra={'task_id': ' ' * 36, 'stage': 'SHUTDOWN', 'source': 'core'})
        self.running = False
        
        # Wait for worker threads to terminate
        for worker in self.workers:
            if worker.is_alive():
                worker.join(timeout=3.0)
        
        self.workers = []
        self.task_manager.shutdown()
        logger.info("Data Cleanse Core stopped", 
                   extra={'task_id': ' ' * 36, 'stage': 'SHUTDOWN', 'source': 'core'})
    
    def create_task(self, source: str, source_type: str = "file", 
                   chunking_strategy: Optional[str] = None, 
                   **kwargs) -> str:
        """
        Create a new data cleansing task
        
        Args:
            source: Source data (file path, URL, or text)
            source_type: Type of source ("file", "url", or "text")
            chunking_strategy: Strategy for chunking the document
            **kwargs: Additional parameters for cleanse_data
            
        Returns:
            Task ID
        """
        # Create task data
        task_data = {
            "source": source,
            "source_type": source_type,
            "chunking_strategy": chunking_strategy
        }
        
        # Add additional parameters
        task_data.update(kwargs)
        
        # Create task in task manager
        task_id = self.task_manager.create_task(task_data)
        logger.info(f"Created new task for source: {source}", 
                   extra={'task_id': task_id, 'stage': 'CREATED', 'source': 'core'})
        return task_id

    def create_batch_tasks(self, sources: List[Dict[str, Any]]) -> List[str]:
        """
        Create multiple data cleansing tasks in batch
        
        Args:
            sources: List of source dictionaries, each containing:
                    - source: Source data (file path, URL, or text)
                    - source_type: Type of source ("file", "url", or "text")
                    - chunking_strategy: Strategy for chunking the document
                    - Additional parameters for cleanse_data
                    
        Returns:
            List of task IDs
        """
        # Use the same async processing approach for all batch tasks, regardless of size
        task_ids = []
        batch_id = f"batch-{int(time.time())}"
        
        logger.info(f"Creating batch with {len(sources)} tasks", 
                   extra={'task_id': batch_id, 'stage': 'BATCH', 'source': 'core'})
        
        # Create a separate task for each source
        for source_data in sources:
            source = source_data.get("source")
            source_type = source_data.get("source_type", "file")
            chunking_strategy = source_data.get("chunking_strategy")
            
            # Extract additional kwargs
            kwargs = {k: v for k, v in source_data.items() 
                    if k not in ["source", "source_type", "chunking_strategy"]}
            
            task_id = self.create_task(
                source=source,
                source_type=source_type,
                chunking_strategy=chunking_strategy,
                **kwargs
            )
            task_ids.append(task_id)
        
        logger.info(f"Batch creation completed with {len(task_ids)} tasks", 
                   extra={'task_id': batch_id, 'stage': 'BATCH', 'source': 'core'})
        return task_ids
    
    def get_task(self, task_id: str) -> Optional[Dict[str, Any]]:
        """
        Get task information
        
        Args:
            task_id: Task ID
            
        Returns:
            Task information or None if not found
        """
        return self.task_manager.get_task(task_id)
    
    def get_all_tasks(self) -> List[Dict[str, Any]]:
        """
        Get all tasks
        
        Returns:
            List of all tasks
        """
        return self.task_manager.get_all_tasks()
    
    def _worker_loop(self) -> None:
        """Worker thread loop to process tasks"""
        thread_name = threading.current_thread().name
        logger.info(f"Worker {thread_name} started", 
                   extra={'task_id': ' ' * 36, 'stage': 'WORKER', 'source': 'core'})
        
        while self.running:
            # Get next waiting task
            task = self.task_manager.get_next_waiting_task()
            
            if task:
                task_id = task['id']
                logger.info(f"Worker {thread_name} processing task", 
                           extra={'task_id': task_id, 'stage': 'WAITING', 'source': 'core'})
                self._process_task(task)
            else:
                # Sleep if no tasks - using shorter polling interval
                time.sleep(self.poll_interval)
        
        logger.info(f"Worker {thread_name} stopped", 
                   extra={'task_id': ' ' * 36, 'stage': 'WORKER', 'source': 'core'})
    
    def _process_task(self, task: Dict[str, Any]) -> None:
        """
        Process a single task
        
        Args:
            task: Task to process
        """
        task_id = task["id"]
        task_data = task["data"]
        
        try:
            # Extract task parameters
            source = task_data.get("source")
            source_type = task_data.get("source_type", "file")
            chunking_strategy = task_data.get("chunking_strategy")
            
            # Extract additional parameters - excluding specific key names
            kwargs = {k: v for k, v in task_data.items()
                    if k not in ["source", "source_type", "chunking_strategy", "is_batch", "sources"]}
            
            # Process data - using the integrated method
            logger.info(f"Processing source: {source} ({source_type})", 
                      extra={'task_id': task_id, 'stage': 'PROCESSING', 'source': 'core'})
            try:
                # Complete data cleansing and forwarding in one step
                self.cleanse_and_forward_data(
                    task_id=task_id,
                    source=source,
                    source_type=source_type,
                    chunking_strategy=chunking_strategy,
                    **kwargs
                )
                
                # If execution reaches here, the entire process completed successfully
                logger.info("Task completed successfully", 
                          extra={'task_id': task_id, 'stage': 'COMPLETED', 'source': 'core'})
                
            except Exception as e:
                # Handle errors in data cleansing and forwarding process
                error_msg = str(e)
                logger.error(f"Processing failed with error: {error_msg}", 
                           extra={'task_id': task_id, 'stage': 'FAILED', 'source': 'core'})
                
                # Update task status to failed
                self.task_manager.update_task_status(
                    task_id=task_id,
                    status=TaskStatus.FAILED,
                    error=error_msg
                )
            
        except Exception as e:
            # Handle uncaught errors in overall task process
            error_msg = str(e)
            logger.error(f"Failed with unexpected error: {error_msg}", 
                       extra={'task_id': task_id, 'stage': 'FAILED', 'source': 'core'})
            
            self.task_manager.update_task_status(
                task_id=task_id,
                status=TaskStatus.FAILED,
                error=error_msg
            )

    def cleanse_data(
        self,
        source: str,
        source_type: str = "file",
        chunking_strategy: Optional[str] = "basic",
        **kwargs
    ) -> List[Dict[str, Any]]:
        """
        Cleanses data from various sources using unstructured library.
        
        Args:
            source: Path to file, URL, or text content to process
            source_type: Type of source - "file", "url", or "text"
            chunking_strategy: Strategy to chunk the document (e.g., "by_title")
            **kwargs: Additional arguments to pass to partition function
            
        Returns:
            List of dictionaries containing cleansed text and metadata
        """
        # Validate source_type
        if source_type not in ["file", "url", "text"]:
            raise ValueError("source_type must be one of: 'file', 'url', 'text'")
        
        # Set up partition parameters based on source_type
        partition_kwargs = kwargs.copy()
        
        if chunking_strategy:
            partition_kwargs["chunking_strategy"] = chunking_strategy
        
        # Track file size and creation time
        file_size = 0
        creation_date = None
        file_name = ""
        
        # Process based on source type
        try:
            if source_type == "file":
                # Convert to absolute path if it's a relative path
                if not os.path.isabs(source):
                    source = os.path.abspath(source)
                
                # Get file metadata before processing
                if os.path.exists(source):
                    file_stats = os.stat(source)
                    file_size = file_stats.st_size // 1024  # Convert to KB
                    creation_date = file_stats.st_ctime
                    file_name = os.path.basename(source)
                
                elements = partition(filename=source, max_characters=5000, **partition_kwargs)
            elif source_type == "url":
                try:
                    # For URLs, try to get content size from headers
                    import requests
                    file_name = source.split("/")[-1]
                    headers = requests.head(source, allow_redirects=True).headers
                    if 'content-length' in headers:
                        file_size = int(headers['content-length']) // 1024  # Convert to KB
                    creation_date = time.time()  # Use current time as creation date for URLs
                except Exception as e:
                    logger.warning(f"Could not get URL metadata: {str(e)}")
                
                elements = partition(url=source, max_characters=5000, **partition_kwargs)
            else:  # text
                # For text type, we need a different processing approach
                # Try to write text content to a temporary file, then process
                import tempfile
                
                # Calculate size of text in KB
                file_size = len(source.encode('utf-8')) // 1024
                creation_date = time.time()  # Use current time
                file_name = "text_input.txt"
                
                with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as temp_file:
                    temp_file.write(source)
                    temp_path = temp_file.name
                
                try:
                    # Process using temporary file
                    elements = partition(filename=temp_path, max_characters=5000, **partition_kwargs)
                    
                    # Create a simple result list
                    result = []
                    for element in elements:
                        # Get element metadata
                        metadata = element.metadata.to_dict()
                        
                        # Add file metadata if not present
                        if 'file_size' not in metadata:
                            metadata['file_size'] = file_size
                        if 'creation_date' not in metadata and creation_date:
                            metadata['creation_date'] = creation_date
                        if 'filename' not in metadata:
                            metadata['filename'] = file_name
                            
                        # Add title if not present (use first line or filename)
                        if 'title' not in metadata:
                            title = file_name
                            # Use first line as title if it's not too long
                            first_line = element.text.strip().split('\n')[0] if element.text else ""
                            if first_line and len(first_line) < 100:
                                title = first_line
                            metadata['title'] = title
                        
                        result.append({
                            "text": element.text,
                            "metadata": metadata,
                            "source": source,
                            "source_type": source_type
                        })
                    
                    return result
                finally:
                    # Ensure temporary file is deleted
                    if os.path.exists(temp_path):
                        os.unlink(temp_path)
            
            # Processing for file and url types
            # Extract text and metadata
            result = []
            for element in elements:
                # Get element metadata
                metadata = element.metadata.to_dict()
                
                # Add file metadata if not present
                if 'file_size' not in metadata:
                    metadata['file_size'] = file_size
                if 'creation_date' not in metadata and creation_date:
                    metadata['creation_date'] = creation_date
                if 'filename' not in metadata:
                    metadata['filename'] = file_name
                    
                # Add title if not present (use first line or filename)
                if 'title' not in metadata:
                    title = file_name
                    # Use first line as title if it's not too long
                    first_line = element.text.strip().split('\n')[0] if element.text else ""
                    if first_line and len(first_line) < 100:
                        title = first_line
                    metadata['title'] = title
                
                result.append({
                    "text": element.text,
                    "metadata": metadata,
                    "source": source,
                    "source_type": source_type
                })
            
            return result
        except Exception as e:
            # Rewrap exception, preserving original error message
            raise ValueError(f"Error processing document: {str(e)}")

    def cleanse_and_forward_data(
        self,
        task_id: str,
        source: str,
        source_type: str = "file",
        chunking_strategy: Optional[str] = "basic",
        **kwargs
    ) -> List[Dict[str, Any]]:
        """
        Cleanse data and forward it to Elasticsearch
        
        This method integrates the entire processing workflow to avoid state management issues
        in asynchronous processing. The workflow follows the state transitions:
        WAITING -> PROCESSING -> FORWARDING -> COMPLETED
        
        Args:
            task_id: Task ID
            source: Source data (file path, URL, or text content)
            source_type: Type of source ("file", "url", or "text")
            chunking_strategy: Strategy for chunking the document 
            **kwargs: Additional parameters for partition function
            
        Returns:
            List of processed data items
        """
        # Phase 1: Data cleansing
        logger.info(f"Starting data cleansing phase for {source} ({source_type})", 
                  extra={'task_id': task_id, 'stage': 'CLEANSING', 'source': 'core'})
        
        # Cleanse data
        result = self.cleanse_data(
            source=source,
            source_type=source_type,
            chunking_strategy=chunking_strategy,
            **kwargs
        )
        
        if not result:
            logger.error("No results generated during data cleansing", 
                       extra={'task_id': task_id, 'stage': 'CLEANSING', 'source': 'core'})
            raise ValueError("No results generated during data cleansing")
        
        # Update task status to forwarding
        self.task_manager.update_task_status(
            task_id=task_id,
            status=TaskStatus.FORWARDING,
            result=result
        )
        logger.info("Data cleansing completed, state changed to forwarding", 
                  extra={'task_id': task_id, 'stage': 'FORWARDING', 'source': 'core'})
        
        # Phase 2: Forward to Elasticsearch
        # Get index name from task data
        task = self.get_task(task_id)
        if not task:
            logger.error("Task not found for forwarding phase", 
                       extra={'task_id': task_id, 'stage': 'FORWARDING', 'source': 'core'})
            raise ValueError(f"Task {task_id} not found for forwarding phase")
            
        index_name = task.get("data", {}).get("index_name", self.default_index_name)
        
        # Prepare content for forwarding
        payload = {
            "task_id": task_id,
            "index_name": index_name,
            "results": result
        }
        
        # Call Elasticsearch service synchronously
        logger.info(f"Beginning transfer to Elasticsearch index '{index_name}'", 
                  extra={'task_id': task_id, 'stage': 'FORWARDING', 'source': 'core'})
        
        # Use httpx synchronous client instead of async client
        with httpx.Client(timeout=600.0) as client:
            try:
                # Send request to Elasticsearch service
                response = client.post(
                    f"{self.es_service_url}/indices/{index_name}/documents",
                    json=payload,
                    timeout=500.0  # 增加批量请求的超时时间
                )
                response.raise_for_status()
                response_data = response.json()
                
                # Update task status to completed
                self.task_manager.update_task_status(
                    task_id=task_id,
                    status=TaskStatus.COMPLETED,
                    result=result,
                    error=None
                )
                
                logger.info(f"Successfully indexed {response_data.get('total_indexed', 0)} documents to Elasticsearch", 
                          extra={'task_id': task_id, 'stage': 'COMPLETED', 'source': 'core'})
            except httpx.HTTPStatusError as e:
                error_msg = f"HTTP error during Elasticsearch indexing ({e.response.status_code}): {e.response.text}"
                logger.error(error_msg, extra={'task_id': task_id, 'stage': 'FAILED', 'source': 'core'})
                raise ValueError(error_msg)
            except httpx.TimeoutException:
                error_msg = "Timeout during Elasticsearch indexing"
                logger.error(error_msg, extra={'task_id': task_id, 'stage': 'FAILED', 'source': 'core'})
                raise ValueError(error_msg)
            except Exception as e:
                error_msg = f"Unexpected error during Elasticsearch indexing: {str(e)}"
                logger.error(error_msg, extra={'task_id': task_id, 'stage': 'FAILED', 'source': 'core'})
                raise ValueError(error_msg)
        
        return result 