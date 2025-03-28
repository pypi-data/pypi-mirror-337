import time
import os
from typing import List, Dict, Any, Optional
from fastapi import FastAPI, HTTPException, Query, Body, Path, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from dotenv import load_dotenv

from AgentEngine.vector_database.elasticsearch_core import ElasticSearchCore

# Load environment variables
load_dotenv()

# Get ES configuration from environment
ES_HOST = os.getenv("ELASTICSEARCH_HOST", "https://localhost:9200")
ES_API_KEY = os.getenv("ELASTICSEARCH_API_KEY")
CREATE_TEST_KB = os.getenv("CREATE_TEST_KB", "False").lower() == "true"

# Initialize FastAPI app
app = FastAPI(
    title="Elasticsearch Vector Database API",
    description="API for managing vector search with Elasticsearch",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize ElasticSearchCore instance with HTTPS support
es_core = ElasticSearchCore(
    init_test_kb=CREATE_TEST_KB,
    host=ES_HOST,
    api_key=ES_API_KEY,
    verify_certs=False,
    ssl_show_warn=False,
)

# --- Pydantic Models ---

class FileInfo(BaseModel):
    path_or_url: str = Field(..., description="Document source path or URL")
    file: str = Field(..., description="File name or identifier")
    file_size: Optional[int] = Field(None, description="Size of the file in bytes")
    create_time: Optional[str] = Field(None, description="Creation time of the file")

class IndexInfo(BaseModel):
    base_info: Dict[str, Any]
    search_performance: Dict[str, Any]
    fields: List[str]
    unique_sources_count: int
    cleanse_source: str
    embedding_model: Optional[str] = Field(None, description="Embedding model used")
    files: Optional[List[FileInfo]] = Field(None, description="List of files in the index")

class IndexingRequest(BaseModel):
    task_id: str
    index_name: str
    results: List[Dict[str, Any]]
    embedding_dim: Optional[int] = None

class IndexingResponse(BaseModel):
    success: bool
    message: str
    total_indexed: int
    total_submitted: int

class DocumentResponse(BaseModel):
    id: str
    title: str
    file: str
    path_or_url: str
    language: Optional[str] = None
    author: Optional[str] = None
    date: Optional[str] = None
    content: str
    cleanse_source: str
    embedding_model_name: Optional[str] = None
    file_size: Optional[int] = None
    create_time: Optional[str] = None
    score: Optional[float] = None

class SearchResponse(BaseModel):
    results: List[DocumentResponse]
    total: int
    query_time_ms: Optional[float] = None

# --- Dependency Injection ---

def get_es_core():
    return es_core

# Index Management

@app.delete("/indices/{index_name}")
def delete_index(
    index_name: str = Path(..., description="Name of the index to delete"),
    es_core: ElasticSearchCore = Depends(get_es_core)
):
    """Delete an index"""
    success = es_core.delete_index(index_name)
    if not success:
        raise HTTPException(status_code=404, detail=f"Index {index_name} not found or could not be deleted")
    return {"status": "success", "message": f"Index {index_name} deleted successfully"}

@app.get("/indices")
def list_indices(
    pattern: str = Query("*", description="Pattern to match index names"),
    include_stats: bool = Query(False, description="Whether to include index stats"),
    es_core: ElasticSearchCore = Depends(get_es_core)
):
    """List all user indices with optional stats"""
    indices = es_core.get_user_indices(pattern)
    
    if include_stats:
        # Get stats for all indices
        all_stats = es_core.get_all_indices_stats(pattern)
        
        # Build richer index information
        indices_info = []
        for index_name in indices:
            index_info = {
                "name": index_name,
                "stats": all_stats.get(index_name, {})
            }
            indices_info.append(index_info)
        
        return {
            "indices": indices,
            "count": len(indices),
            "indices_info": indices_info
        }
    else:
        return {"indices": indices, "count": len(indices)}

@app.get("/indices/{index_name}/info")
def get_index_info(
    index_name: str = Path(..., description="Name of the index"),
    include_files: bool = Query(True, description="Whether to include file list"),
    es_core: ElasticSearchCore = Depends(get_es_core)
):
    """Get comprehensive information about an index including stats, fields, sources and cleanse info"""
    try:
        # Get all the info in one combined response
        stats = es_core.get_index_stats(index_name)
        fields = es_core.get_index_mapping(index_name)
        unique_sources_count = es_core.get_unique_sources_count(index_name)
        
        # Get file list if requested
        files = []
        if include_files:
            files = es_core.get_file_list_with_details(index_name)
        
        # Ensure base info includes unique source count
        if "base_info" not in stats:
            stats["base_info"] = {}
        stats["base_info"]["unique_sources_count"] = unique_sources_count
        
        return {
            "base_info": stats["base_info"],
            "search_performance": stats["search_performance"],
            "fields": fields,
            "files": files
        }
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Error getting info for index {index_name}: {str(e)}")

# Document Operations

@app.post("/indices/{index_name}/documents", response_model=IndexingResponse)
def index_documents(
    index_name: str = Path(..., description="Name of the index"),
    data: IndexingRequest = Body(..., description="Indexing request to process"),
    embedding_model_name: Optional[str] = Query(None, description="Name of the embedding model to use"),
    es_core: ElasticSearchCore = Depends(get_es_core)
):
    """
    Index documents with embeddings, creating the index if it doesn't exist.
    Accepts an IndexingRequest object from data processing.
    """
    try:
        print(f"Received request for index {index_name}")
        
        # Extract index_name from IndexingRequest if present
        if data.index_name:
            # Override path parameter with value from the data itself
            print(f"Using index name from request: {data.index_name}")
            index_name = data.index_name
            
        if not index_name:
            raise HTTPException(status_code=400, detail="Index name is required")
        
        # Check if index exists, create if it doesn't
        indices = es_core.get_user_indices()
        
        # Create index if needed (ElasticSearchCore will handle embedding_dim automatically)
        if index_name not in indices:
            print(f"Creating new index: {index_name}")
            success = es_core.create_vector_index(index_name)
            if not success:
                raise HTTPException(status_code=500, detail=f"Failed to auto-create index {index_name}")
        
        # Handle indexing request format
        task_id = data.task_id
        results = data.results
        
        print(f"Processing {len(results)} documents for task {task_id}")
        
        # Transform indexing request results to documents
        documents = []
        
        for idx, item in enumerate(results):
            # All items should be dictionaries
            if not isinstance(item, dict):
                print(f"Skipping item {idx} - not a dictionary")
                continue
                
            # Extract metadata
            metadata = item.get("metadata", {})
            source = item.get("source", "")
            text = item.get("text", "")
            
            file_name = metadata.get("filename", os.path.basename(source) if source else "unknown")
            
            # Get title from metadata, or use filename
            title = metadata.get("title", file_name)
            
            # Get other metadata
            language = metadata.get("language", "null")
            author = metadata.get("author", "null")
            date = metadata.get("date", time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime()))
            file_size = metadata.get("file_size", 0)
            
            # Get create_time from metadata or current time
            create_time = metadata.get("creation_date", time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime()))
            if isinstance(create_time, (int, float)):
                import datetime
                create_time = datetime.datetime.fromtimestamp(create_time).isoformat()
            
            # Create document
            document = {
                "id": f"{task_id}_{idx}",
                "title": title,
                "file": file_name,
                "path_or_url": source,
                "language": language,
                "author": author,
                "date": date,
                "content": text,
                "cleanse_source": "Unstructured",
                "file_size": file_size,
                "create_time": create_time
            }
            
            documents.append(document)
        
        # Ensure all documents have required fields
        current_time = time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime())
        for doc in documents:
            # Set embedding model name if provided or use the default from the embedding model
            if embedding_model_name:
                doc["embedding_model_name"] = embedding_model_name
            elif not doc.get("embedding_model_name"):
                doc["embedding_model_name"] = es_core.embedding_model.embedding_model_name
            
            # Set create_time if not present
            if not doc.get("create_time"):
                doc["create_time"] = current_time
            
            # Ensure file_size is present (default to 0 if not provided)
            if not doc.get("file_size"):
                doc["file_size"] = 0
                
            # Ensure cleanse_source is present
            if not doc.get("cleanse_source"):
                doc["cleanse_source"] = "Unstructured"
        
        total_submitted = len(documents)
        if total_submitted == 0:
            return {
                "success": True,
                "message": "No documents to index",
                "total_indexed": 0,
                "total_submitted": 0
            }
            
        print(f"Submitting {total_submitted} documents to Elasticsearch")
        
        # Index documents (use default batch_size and content_field)
        try:
            total_indexed = es_core.index_documents(
                index_name=index_name,
                documents=documents
            )
            
            print(f"Successfully indexed {total_indexed} documents")
            
            return {
                "success": True,
                "message": f"Successfully indexed {total_indexed} documents",
                "total_indexed": total_indexed,
                "total_submitted": total_submitted
            }
        except Exception as e:
            error_msg = str(e)
            print(f"Error during indexing: {error_msg}")
            raise HTTPException(status_code=500, detail=f"Error during indexing: {error_msg}")
        
    except Exception as e:
        error_msg = str(e)
        print(f"Error indexing documents: {error_msg}")
        raise HTTPException(status_code=500, detail=f"Error indexing documents: {error_msg}")

@app.delete("/indices/{index_name}/documents")
def delete_documents(
    index_name: str = Path(..., description="Name of the index"),
    path_or_url: str = Query(..., description="Path or URL of documents to delete"),
    es_core: ElasticSearchCore = Depends(get_es_core)
):
    """Delete documents by path or URL"""
    deleted_count = es_core.delete_documents_by_path_or_url(index_name, path_or_url)
    return {"status": "success", "deleted_count": deleted_count}

# Search Operations

@app.get("/indices/{index_name}/search/accurate")
def accurate_search(
    index_name: str = Path(..., description="Name of the index to search in"),
    query: str = Query(..., description="Text query to search for"),
    top_k: int = Query(5, description="Number of results to return"),
    es_core: ElasticSearchCore = Depends(get_es_core)
):
    """Search for documents using fuzzy text matching"""
    try:
        # Validate query is not empty
        if not query.strip():
            raise HTTPException(status_code=400, detail="Search query cannot be empty")
            
        start_time = time.time()
        results = es_core.accurate_search(index_name, query, top_k)
        query_time = (time.time() - start_time) * 1000  # Convert to milliseconds
        
        # Format results
        formatted_results = []
        for result in results:
            doc = result["document"]
            doc["score"] = result["score"]
            formatted_results.append(doc)
        
        return {
            "results": formatted_results,
            "total": len(formatted_results),
            "query_time_ms": query_time
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during search: {str(e)}")

@app.get("/indices/{index_name}/search/semantic")
def semantic_search(
    index_name: str = Path(..., description="Name of the index to search in"),
    query: str = Query(..., description="Text query to search for"),
    top_k: int = Query(5, description="Number of results to return"),
    es_core: ElasticSearchCore = Depends(get_es_core)
):
    """Search for similar documents using vector similarity"""
    try:
        # Validate query is not empty
        if not query.strip():
            raise HTTPException(status_code=400, detail="Search query cannot be empty")
            
        start_time = time.time()
        results = es_core.semantic_search(index_name, query, top_k)
        query_time = (time.time() - start_time) * 1000  # Convert to milliseconds
        
        # Format results
        formatted_results = []
        for result in results:
            doc = result["document"]
            doc["score"] = result["score"]
            formatted_results.append(doc)
        
        return {
            "results": formatted_results,
            "total": len(formatted_results),
            "query_time_ms": query_time
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error during search: {str(e)}")

# Health check
@app.get("/health")
def health_check(es_core: ElasticSearchCore = Depends(get_es_core)):
    """Check API and Elasticsearch health"""
    try:
        # Try to list indices as a health check
        indices = es_core.get_user_indices()
        return {
            "status": "healthy",
            "elasticsearch": "connected",
            "indices_count": len(indices)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Health check failed: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 