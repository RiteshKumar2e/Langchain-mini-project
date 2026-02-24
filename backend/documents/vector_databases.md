# Vector Databases

## What is a Vector Database?

A vector database is a type of database that stores data as high-dimensional vectors (also called embeddings). These vectors are mathematical representations of data (text, images, audio, etc.) in a multi-dimensional space where similar items are located close to each other.

Vector databases are essential components in modern AI applications, particularly for:
- Semantic search
- Recommendation systems
- Retrieval-Augmented Generation (RAG)
- Anomaly detection
- Image and audio similarity search

## How Vector Databases Work

### 1. Embedding Generation
Data is first converted into embeddings using embedding models:
- Text → OpenAI `text-embedding-ada-002`, Sentence Transformers
- Images → CLIP, ResNet
- Audio → wav2vec

### 2. Indexing
Vectors are indexed using Approximate Nearest Neighbor (ANN) algorithms:
- **HNSW (Hierarchical Navigable Small World)**: Graph-based, fast query time
- **IVF (Inverted File Index)**: Cluster-based
- **LSH (Locality Sensitive Hashing)**: Hash-based

### 3. Querying
A query vector is compared to stored vectors using distance metrics:
- **Cosine Similarity**: Measures the angle between vectors (most common for text)
- **Euclidean Distance**: Straight-line distance between points
- **Dot Product**: Measures the projection of one vector onto another

## Popular Vector Databases

### FAISS (Facebook AI Similarity Search)
- Open source library by Facebook/Meta
- Optimized for billion-scale similarity search
- In-memory or on-disk storage
- Used as the backbone for many vector stores
- **Best for**: Local development, research, when you control the infrastructure

### Chroma
- Open source embedding database
- Easy to use with LangChain
- Persistent storage out of the box
- **Best for**: Development, prototyping, small to medium scale

### Pinecone
- Fully managed, cloud-native vector database
- Automatic scaling and high availability
- **Best for**: Production applications requiring managed infrastructure

### Weaviate
- Open source vector search engine
- Supports GraphQL queries
- Multi-modal support (text + images)
- **Best for**: Complex schemas and hybrid search

### Qdrant
- Open source vector search engine written in Rust
- High performance and low memory footprint
- **Best for**: Self-hosted production deployments

### Milvus
- Open source vector database
- Highly scalable and cloud-native
- **Best for**: Large-scale enterprise deployments

## FAISS Deep Dive

FAISS (Facebook AI Similarity Search) is particularly important for LangChain applications:

### Index Types
- **IndexFlatL2**: Exact search using L2 distance
- **IndexFlatIP**: Exact search using inner product
- **IndexIVFFlat**: Approximate search with inverted file
- **IndexHNSWFlat**: Graph-based approximate search

### Usage with LangChain
```python
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(documents, embeddings)

# Save and load
vectorstore.save_local("faiss_index")
vectorstore = FAISS.load_local("faiss_index", embeddings)
```

## Hybrid Search

Modern vector databases support hybrid search combining:
- **Dense retrieval**: Vector similarity search
- **Sparse retrieval**: Keyword/BM25 search
- **Reranking**: Cross-encoder models to rerank results

## Key Concepts

### Metadata Filtering
Filter results based on metadata before or after vector search:
- Date ranges
- Categories
- Author names
- Document types

### Namespaces/Collections
Partition data into separate logical groups for multi-tenant applications.

### Upsert Operations
Insert or update vectors while maintaining the index.
