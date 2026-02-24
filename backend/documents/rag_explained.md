# Retrieval-Augmented Generation (RAG)

## What is RAG?

Retrieval-Augmented Generation (RAG) is an AI architecture that enhances large language model (LLM) responses by retrieving relevant information from an external knowledge base before generating an answer. It was introduced in a 2020 paper by Lewis et al. from Facebook AI Research.

RAG addresses key limitations of LLMs:
- **Knowledge cutoff**: LLMs have a fixed training date and cannot access new information
- **Hallucination**: LLMs can generate plausible-sounding but factually incorrect information
- **Domain-specific knowledge**: LLMs lack proprietary or specialized knowledge
- **Source attribution**: LLMs cannot easily cite specific sources

## RAG Architecture

### Phase 1: Indexing (Offline)

1. **Document Loading**: Load documents from various sources (PDF, web pages, databases)
2. **Text Splitting**: Break documents into manageable chunks (typically 500-1000 tokens with overlap)
3. **Embedding**: Convert chunks into vector representations using an embedding model
4. **Vector Storage**: Store vectors in a vector database with metadata

### Phase 2: Retrieval and Generation (Online)

1. **Query Embedding**: Convert the user's question into a vector
2. **Similarity Search**: Find the most similar document chunks in the vector store
3. **Context Formation**: Combine retrieved chunks into a context
4. **Prompt Construction**: Create a prompt with the question and context
5. **LLM Generation**: Generate an answer using the LLM with the context
6. **Response**: Return the answer with source citations

## Types of RAG

### Naive RAG
The basic RAG pipeline as described above:
- Simple embedding and retrieval
- Single-stage retrieval
- Direct prompt stuffing

### Advanced RAG
Improvements to the basic pipeline:
- **Query Rewriting**: Rewrite queries for better retrieval
- **HyDE (Hypothetical Document Embeddings)**: Generate a hypothetical answer, embed it, then retrieve
- **Multi-Query Retrieval**: Generate multiple query variations
- **Contextual Compression**: Compress retrieved documents to relevant parts

### Modular RAG
Even more flexible architecture:
- Searchable modules that can be combined
- Routing to different retrievers
- Adaptive retrieval

## Chunking Strategies

### Fixed-Size Chunking
Split by character or token count:
- Simple and predictable
- May break semantic units

### Recursive Text Splitting
Split by paragraph, then sentence, then word:
- Better preserves semantic meaning
- LangChain's `RecursiveCharacterTextSplitter`

### Semantic Chunking
Split based on semantic similarity between sentences:
- Groups semantically related content
- More expensive to compute

### Document-Specific Splitting
- Markdown: Split by headers
- Code: Split by function/class
- HTML: Split by tag structure

## Retrieval Strategies

### Dense Retrieval
- Uses embedding similarity
- Semantic search
- Captures meaning beyond keywords

### Sparse Retrieval
- BM25 / TF-IDF
- Keyword-based
- Exact match retrieval

### Hybrid Retrieval
- Combines dense and sparse
- Uses reciprocal rank fusion (RRF) to merge results
- Often achieves better results than either alone

### MMR (Maximum Marginal Relevance)
- Balances relevance and diversity
- Reduces redundancy in retrieved documents

## Evaluation of RAG Systems

### Retrieval Metrics
- **Recall@K**: What fraction of relevant documents appear in top K
- **Precision@K**: What fraction of top K results are relevant
- **MRR (Mean Reciprocal Rank)**: Rank of the first relevant document

### Generation Metrics
- **Faithfulness**: Is the answer grounded in the retrieved context?
- **Answer Relevancy**: Is the answer relevant to the question?
- **Context Precision**: Are the retrieved chunks relevant?
- **Context Recall**: Does the context contain the needed information?

### Frameworks
- **RAGAS**: Framework specifically for RAG evaluation
- **TruLens**: Evaluation and tracing for LLM apps

## Common Challenges and Solutions

### Challenge: Poor Retrieval Quality
- Solution: Better chunking, embedding models, hybrid search

### Challenge: Lost in the Middle
- Solution: LLMs perform better with relevant content at the start or end of context; use reranking

### Challenge: Context Window Limits
- Solution: Contextual compression, map-reduce patterns

### Challenge: Outdated Knowledge Base
- Solution: Implement update pipelines to re-index new documents

## RAG with LangChain

```python
from langchain_community.document_loaders import DirectoryLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.chains import RetrievalQA

# Load and split documents
loader = DirectoryLoader("./documents", glob="**/*.md")
docs = loader.load()
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_documents(docs)

# Create vector store
embeddings = OpenAIEmbeddings()
vectorstore = FAISS.from_documents(chunks, embeddings)

# Create RAG chain
llm = ChatOpenAI(model="gpt-4o-mini")
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=vectorstore.as_retriever(search_kwargs={"k": 4}),
    return_source_documents=True
)

# Query
result = qa_chain.invoke({"query": "What is RAG?"})
print(result["result"])
```
