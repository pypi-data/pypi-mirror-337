import os
import json
import requests
from typing import List, Dict, Any
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class JinaEmbedding:
    def __init__(self):
        """Initialize JinaEmbedding with configuration from environment variables."""
        self.api_key = os.getenv('JINA_API_KEY')
        self.api_url = os.getenv('JINA_API_URL')
        self.model = os.getenv('JINA_MODEL')
        self.embedding_model_name = "Jina Embedding"
        self.embedding_dim = os.getenv('JINA_EMBEDDING_DIM', 1024)
        
        if not all([self.api_key, self.api_url, self.model]):
            raise ValueError("Missing required environment variables. Please check your .env file.")
        
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }

    def _prepare_input(self, inputs: List[Dict[str, str]]) -> Dict[str, Any]:
        """Prepare the input data for the API request."""
        return {
            "model": self.model,
            "input": inputs
        }

    def _make_request(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Make the API request and return the response."""
        response = requests.post(
            self.api_url,
            headers=self.headers,
            json=data
        )
        response.raise_for_status()
        return response.json()

    def get_embeddings(self, inputs: List[Dict[str, str]]) -> List[List[float]]:
        """
        Get embeddings for a list of inputs (text or image URLs).
        
        Args:
            inputs: List of dictionaries containing either 'text' or 'image' keys
            
        Returns:
            List of embedding vectors
            
        Example:
            >>> jina = JinaEmbedding()
            >>> inputs = [
            ...     {"text": "A beautiful sunset over the beach"},
            ...     {"image": "https://example.com/image.jpg"}
            ... ]
            >>> embeddings = jina.get_embeddings(inputs)
        """
        data = self._prepare_input(inputs)
        response = self._make_request(data)
        
        # Extract embeddings from response
        embeddings = [item["embedding"] for item in response["data"]]
        return embeddings

    def get_embeddings_with_metadata(self, inputs: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Get embeddings along with metadata from the API response.
        
        Args:
            inputs: List of dictionaries containing either 'text' or 'image' keys
            
        Returns:
            Dictionary containing embeddings and metadata
        """
        data = self._prepare_input(inputs)
        response = self._make_request(data)
        return response

def main():
    """Example usage of the JinaEmbedding class."""
    # Example inputs
    inputs = [
        {"text": "A beautiful sunset over the beach"},
        {"text": "Un beau coucher de soleil sur la plage"},
        {"text": "海滩上美丽的日落"},
        {"text": "浜辺に沈む美しい夕日"},
        {"image": "https://i.ibb.co/nQNGqL0/beach1.jpg"},
        {"image": "https://i.ibb.co/r5w8hG8/beach2.jpg"},
        {"image": "R0lGODlhEAAQAMQAAORHHOVSKudfOulrSOp3WOyDZu6QdvCchPGolfO0o/XBs/fNwfjZ0frl3/zy7////wAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACH5BAkAABAALAAAAAAQABAAAAVVICSOZGlCQAosJ6mu7fiyZeKqNKToQGDsM8hBADgUXoGAiqhSvp5QAnQKGIgUhwFUYLCVDFCrKUE1lBavAViFIDlTImbKC5Gm2hB0SlBCBMQiB0UjIQA7"}
    ]
    
    try:
        # Initialize the embedding model
        jina = JinaEmbedding()
        
        # Get embeddings
        embeddings = jina.get_embeddings(inputs)
        print(f"Successfully generated {len(embeddings)} embeddings")
        
        # Get embeddings with metadata
        response = jina.get_embeddings_with_metadata(inputs)
        print(f"Total tokens used: {response['usage']['total_tokens']}")
        
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    main() 