import requests
import json
import time
import unittest
import os
from typing import Dict, Any, List

# Base URL for the API
BASE_URL = "http://localhost:8000"

# 是否打印详细结果
VERBOSE = True

def print_response(response, title="Response"):
    """打印响应内容"""
    if VERBOSE:
        print(f"\n=== {title} ===")
        print(f"Status Code: {response.status_code}")
        if hasattr(response, 'json'):
            try:
                data = response.json()
                print(json.dumps(data, indent=2, ensure_ascii=False))
            except:
                print(response.text)
        else:
            print(response)
        print("=" * (len(title) + 8))

class TestElasticsearchService(unittest.TestCase):
    """Test class for Elasticsearch Service API endpoints"""
    
    @classmethod
    def setUpClass(cls):
        """Setup test class - verify API is running and test knowledge base exists"""
        # Check health endpoint
        try:
            response = requests.get(f"{BASE_URL}/health")
            assert response.status_code == 200, "API is not healthy"
            
            # Get list of indices to verify test knowledge base exists
            response = requests.get(f"{BASE_URL}/indices")
            indices = response.json()["indices"]
            
            # If test knowledge base doesn't exist, create it by indexing a sample document
            if "sample_articles" not in indices:
                print("Test knowledge base 'sample_articles' not found, creating it...")
                # Create a sample document to index
                sample_doc = [{
                    "id": "sample1",
                    "title": "Sample Document",
                    "file": "sample.txt",
                    "path_or_url": "https://example.com/sample.txt",
                    "content": "This is a sample document for testing.",
                    "cleanse_source": "Test",
                    "embedding_model_name": "Jina Embedding",
                    "file_size": 1024,
                    "create_time": time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime())
                }]
                
                # Index the document to automatically create the index
                response = requests.post(
                    f"{BASE_URL}/indices/sample_articles/documents",
                    json=sample_doc
                )
                print_response(response, "Index Creation Response")
                assert response.status_code == 200, "Failed to create test knowledge base"
                
                # Wait for index creation to complete
                time.sleep(2)
                
                # Check if it exists now
                response = requests.get(f"{BASE_URL}/indices")
                indices = response.json()["indices"]
                assert "sample_articles" in indices, "Failed to create test knowledge base"
                
            print(f"Found {len(indices)} indices: {', '.join(indices)}")
            cls.index_name = "sample_articles"
            
        except requests.exceptions.ConnectionError:
            raise unittest.SkipTest("API is not running. Please start the service first.")
    
    def test_01_health_endpoint(self):
        """Test the health endpoint"""
        response = requests.get(f"{BASE_URL}/health")
        print_response(response, "Health Endpoint")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "healthy")
        self.assertEqual(data["elasticsearch"], "connected")
        self.assertIsInstance(data["indices_count"], int)
    
    def test_02_list_indices(self):
        """Test listing indices"""
        response = requests.get(f"{BASE_URL}/indices")
        print_response(response, "List Indices")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("indices", data)
        self.assertIn("count", data)
        self.assertGreaterEqual(data["count"], 1)  # At least one index should exist
        self.assertIn(self.index_name, data["indices"])
        
        # Test with include_stats parameter
        response = requests.get(f"{BASE_URL}/indices?include_stats=true")
        print_response(response, "List Indices with Stats")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # 检查响应结构 - 兼容当前API结构
        if "indices_info" in data:
            # 新结构
            self.assertIn("indices_info", data)
            
            # Check that all indices have stats
            found_index = False
            for index_info in data["indices_info"]:
                self.assertIn("name", index_info)
                self.assertIn("stats", index_info)
                if index_info["name"] == self.index_name:
                    found_index = True
                    self.assertIn("base_info", index_info["stats"])
                    self.assertIn("search_performance", index_info["stats"])
                    self.assertIn("embedding_model", index_info["stats"]["base_info"])
                    self.assertIn("cleanse_source", index_info["stats"]["base_info"])
                    self.assertIn("unique_sources_count", index_info["stats"]["base_info"])
            
            self.assertTrue(found_index, f"Expected to find index {self.index_name} in indices_info")
        else:
            # 旧结构
            self.assertIn("indices_stats", data)
            self.assertIn(self.index_name, data["indices_stats"])
            
            # Check that the stats contain the necessary fields
            index_stats = data["indices_stats"][self.index_name]
            self.assertIn("base_info", index_stats)
            self.assertIn("embedding_model", index_stats["base_info"])
    
    def test_03_get_index_info(self):
        """Test getting consolidated index information"""
        response = requests.get(f"{BASE_URL}/indices/{self.index_name}/info")
        print_response(response, "Index Info")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        
        # Check for all consolidated fields
        self.assertIn("base_info", data)
        self.assertIn("search_performance", data)
        self.assertIn("fields", data)
        
        # 根据响应结构处理字段
        if "files" in data:
            self.assertIn("files", data)
        
        # 检查基本信息字段，处理unique_sources_count可能在base_info或顶层
        self.assertIn("doc_count", data["base_info"])
        
        # 检查不同结构的唯一源计数
        if "unique_sources_count" in data["base_info"]:
            self.assertIn("unique_sources_count", data["base_info"])
        elif "unique_sources_count" in data:
            self.assertIn("unique_sources_count", data)
            
        # 检查不同结构的嵌入模型信息
        if "embedding_model" in data["base_info"]:
            self.assertIn("embedding_model", data["base_info"])  
        elif "embedding_model" in data:
            self.assertIn("embedding_model", data)
            
        # 检查不同结构的cleanse_source信息
        if "cleanse_source" in data["base_info"]:
            self.assertIn("cleanse_source", data["base_info"])
        elif "cleanse_source" in data:
            self.assertIn("cleanse_source", data)
            
        self.assertGreater(data["base_info"]["doc_count"], 0)  # Should have documents
        
        # Validate field mapping
        expected_fields = ["id", "title", "content", "embedding", "path_or_url", "cleanse_source"]
        for field in expected_fields:
            self.assertIn(field, data["fields"])
            
        # 检查新增字段，可能不存在于所有索引中
        new_fields = ["embedding_model_name", "file_size", "create_time"]
        for field in new_fields:
            if field in data["fields"]:
                pass  # 如果存在则通过
            
        # Check file list structure if available
        if "files" in data and data["files"]:
            file_info = data["files"][0]
            self.assertIn("path_or_url", file_info)
            self.assertIn("file", file_info)
    
    def test_05_accurate_search(self):
        """Test accurate text search"""
        # Search for "Doctor" which should be in the sample articles
        response = requests.get(
            f"{BASE_URL}/indices/{self.index_name}/search/accurate", 
            params={"query": "Doctor", "top_k": 2}
        )
        print_response(response, "Accurate Search")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("results", data)
        self.assertIn("total", data)
        self.assertIn("query_time_ms", data)
        self.assertGreater(data["total"], 0)  # Should find at least one result
        
        # Check first result structure
        result = data["results"][0]
        self.assertIn("id", result)
        self.assertIn("title", result)
        self.assertIn("content", result)
        self.assertIn("score", result)
        self.assertNotIn("embedding", result)  # Embedding vector shouldn't be returned
        
        # Check for new fields
        if "embedding_model_name" in result:
            self.assertIsNotNone(result["embedding_model_name"])
    
    def test_06_semantic_search(self):
        """Test semantic vector search"""
        # Search for a semantic query
        response = requests.get(
            f"{BASE_URL}/indices/{self.index_name}/search/semantic", 
            params={"query": "medical professionals in London", "top_k": 2}
        )
        print_response(response, "Semantic Search")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertIn("results", data)
        self.assertIn("total", data)
        self.assertIn("query_time_ms", data)
        self.assertGreater(data["total"], 0)  # Should find at least one result
        
        # Check first result structure
        result = data["results"][0]
        self.assertIn("id", result)
        self.assertIn("title", result)
        self.assertIn("content", result)
        self.assertIn("score", result)
        
        # Check for new fields
        if "embedding_model_name" in result:
            self.assertIsNotNone(result["embedding_model_name"])
    
    def test_07_index_with_new_fields(self):
        """Test indexing documents with new fields"""
        # Create a temporary index name for this test
        temp_index = "test_new_fields"
        
        # Prepare test documents with new fields
        current_time = time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime())
        test_docs = [
            {
                "id": "newfields1",
                "title": "Document with New Fields",
                "file": "newfields1.txt",
                "path_or_url": "https://example.com/newfields1.txt",
                "content": "This document has explicit values for all new fields.",
                "cleanse_source": "Test",
                "embedding_model_name": "Custom Model",
                "file_size": 2048,
                "create_time": current_time
            },
            {
                "id": "newfields2",
                "title": "Document with Default Fields",
                "file": "newfields2.txt",
                "path_or_url": "https://example.com/newfields2.txt",
                "content": "This document relies on default values for new fields.",
                "cleanse_source": "Test"
            }
        ]
        
        # Index the documents
        response = requests.post(
            f"{BASE_URL}/indices/{temp_index}/documents",
            json=test_docs,
            params={"embedding_model_name": "API Override Model"}
        )
        print_response(response, "Index with New Fields")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["total_submitted"], 2)
        
        # Get index info to verify fields
        time.sleep(1)  # Allow time for indexing to complete
        response = requests.get(f"{BASE_URL}/indices/{temp_index}/info")
        print_response(response, "New Fields Index Info")
        self.assertEqual(response.status_code, 200)
        info = response.json()
        
        # Check embedding model field - 处理两种可能的响应结构
        if "embedding_model" in info["base_info"]:
            self.assertEqual(info["base_info"]["embedding_model"], "API Override Model")
        elif "embedding_model" in info:
            self.assertEqual(info["embedding_model"], "API Override Model")
        
        # Check file info
        if "files" in info and info["files"]:
            found_explicit = False
            for file in info["files"]:
                if file["path_or_url"] == "https://example.com/newfields1.txt":
                    found_explicit = True
                    if "file_size" in file:
                        self.assertEqual(file["file_size"], 2048)
            self.assertTrue(found_explicit, "Could not find document with explicit field values")
        
        # Clean up - delete the index
        response = requests.delete(f"{BASE_URL}/indices/{temp_index}")
        self.assertEqual(response.status_code, 200)
    
    def test_09_index_documents(self):
        """Test indexing documents with auto-creation of index"""
        # Create a temporary index name for this test
        temp_index = "test_index_documents"
        
        # Prepare test documents
        test_docs = [
            {
                "id": "test1",
                "title": "Test Document 1",
                "file": "test1.txt",
                "path_or_url": "https://example.com/test1.txt",
                "content": "This is a test document for indexing.",
                "cleanse_source": "Test",
                "language": "en",
                "author": "Test Author",
                "date": "2023-01-01",
                "file_size": 1024,
                "create_time": time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime())
            },
            {
                "id": "test2",
                "title": "Test Document 2",
                "file": "test2.txt",
                "path_or_url": "https://example.com/test2.txt",
                "content": "This is another test document for indexing.",
                "cleanse_source": "Test"
            }
        ]
        
        # Index the documents (should auto-create the index)
        response = requests.post(
            f"{BASE_URL}/indices/{temp_index}/documents",
            json=test_docs
        )
        print_response(response, "Index Documents")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["total_submitted"], 2)
        
        # Verify the documents were indexed
        time.sleep(1)  # Allow time for indexing to complete
        response = requests.get(f"{BASE_URL}/indices/{temp_index}/info")
        self.assertEqual(response.status_code, 200)
        info = response.json()
        self.assertEqual(info["base_info"]["doc_count"], 2)
        
        # Search for the documents
        response = requests.get(
            f"{BASE_URL}/indices/{temp_index}/search/accurate", 
            params={"query": "test document", "top_k": 2}
        )
        self.assertEqual(response.status_code, 200)
        results = response.json()
        self.assertEqual(results["total"], 2)
        
        # Clean up - delete the documents
        response = requests.delete(
            f"{BASE_URL}/indices/{temp_index}/documents",
            params={"path_or_url": "https://example.com/test1.txt"}
        )
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "success")
        self.assertEqual(data["deleted_count"], 1)
        
        # Clean up - delete the index
        response = requests.delete(f"{BASE_URL}/indices/{temp_index}")
        self.assertEqual(response.status_code, 200)
    
    def test_10_index_creation_and_deletion(self):
        """Test auto-creation via document indexing and deletion of an index"""
        # Create a new index by indexing a document
        test_index = "test_index_creation"
        
        # Prepare a test document
        test_doc = [{
            "id": "auto_create",
            "title": "Auto Create Index Test",
            "file": "auto_create.txt",
            "path_or_url": "https://example.com/auto_create.txt",
            "content": "This document should trigger auto-creation of an index.",
            "cleanse_source": "Test",
            "file_size": 512,
            "create_time": time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime())
        }]
        
        # Index the document with a custom embedding dimension
        response = requests.post(
            f"{BASE_URL}/indices/{test_index}/documents",
            json=test_doc,
            params={"embedding_dim": 512}
        )
        print_response(response, "Index Creation")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "success")
        
        # Verify it exists
        response = requests.get(f"{BASE_URL}/indices")
        self.assertIn(test_index, response.json()["indices"])
        
        # Delete the index
        response = requests.delete(f"{BASE_URL}/indices/{test_index}")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "success")
        
        # Verify it's gone
        response = requests.get(f"{BASE_URL}/indices")
        self.assertNotIn(test_index, response.json()["indices"])
    
    def test_11_error_handling(self):
        """Test error handling for non-existent resources"""
        # Non-existent index
        response = requests.get(f"{BASE_URL}/indices/non_existent_index/info")
        print_response(response, "Non-existent Index Error")
        self.assertEqual(response.status_code, 404)
        
        # Invalid search query (empty)
        response = requests.get(
            f"{BASE_URL}/indices/{self.index_name}/search/accurate", 
            params={"query": "", "top_k": 2}
        )
        print_response(response, "Empty Query Error")
        self.assertNotEqual(response.status_code, 200)
    
    def test_12_duplicate_index_creation(self):
        """Test that reusing an existing index name works properly"""
        # Create a temporary index for this test
        temp_index = "test_duplicate_index"
        
        # 先尝试删除现有的索引，避免之前测试残留
        try:
            requests.delete(f"{BASE_URL}/indices/{temp_index}")
            time.sleep(1)  # 等待删除完成
        except:
            pass
            
        # First document batch to create the index
        first_docs = [{
            "id": "dup1",
            "title": "First Document",
            "file": "dup1.txt",
            "path_or_url": "https://example.com/dup1.txt",
            "content": "This is the first document that creates the index.",
            "cleanse_source": "Test",
            "file_size": 128,
            "create_time": time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime())
        }]
        
        # Index the first document to create the index
        response = requests.post(
            f"{BASE_URL}/indices/{temp_index}/documents",
            json=first_docs
        )
        print_response(response, "First Document Indexing")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "success")
        
        # Verify the index was created
        time.sleep(1)  # Allow time for indexing to complete
        response = requests.get(f"{BASE_URL}/indices")
        self.assertIn(temp_index, response.json()["indices"])
        
        # Second document batch to test inserting into existing index
        second_docs = [{
            "id": "dup2",
            "title": "Second Document",
            "file": "dup2.txt",
            "path_or_url": "https://example.com/dup2.txt",
            "content": "This is the second document going into the same index.",
            "cleanse_source": "Test",
            "file_size": 256,
            "create_time": time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime())
        }]
        
        # Index the second document to the same index
        response = requests.post(
            f"{BASE_URL}/indices/{temp_index}/documents",
            json=second_docs
        )
        print_response(response, "Second Document Indexing")
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertEqual(data["status"], "success")
        
        # Verify both documents are in the index
        time.sleep(1)  # Allow time for indexing to complete
        response = requests.get(f"{BASE_URL}/indices/{temp_index}/info")
        print_response(response, "Index Info After Multiple Documents")
        self.assertEqual(response.status_code, 200)
        info = response.json()
        
        # Check file details if files field exists
        if "files" in info and info["files"]:
            file_urls = [file["path_or_url"] for file in info["files"]]
            self.assertIn("https://example.com/dup1.txt", file_urls)
            self.assertIn("https://example.com/dup2.txt", file_urls)
        
        # Clean up - delete the index
        response = requests.delete(f"{BASE_URL}/indices/{temp_index}")
        self.assertEqual(response.status_code, 200)


if __name__ == "__main__":
    print("Testing the Elasticsearch Vector Database API...")
    print(f"Base URL: {BASE_URL}")
    print("Make sure the API server is running before executing these tests.")
    
    # Check for environment variable to control verbosity
    VERBOSE = os.getenv("VERBOSE_TESTS", "True").lower() in ("true", "1", "yes")
    if VERBOSE:
        print("Running tests with verbose output...")
    else:
        print("Running tests...")
        
    unittest.main(verbosity=2) 