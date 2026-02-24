# LangChain Overview

## What is LangChain?

LangChain is an open-source framework designed to simplify the creation of applications using large language models (LLMs). It provides a set of tools, components, and interfaces that make it easier to build LLM-powered applications, including chatbots, question-answering systems, agents, and more.

LangChain was created by Harrison Chase and first released in October 2022. It has since become one of the most popular frameworks for building LLM applications.

## Core Components of LangChain

### 1. Models

LangChain supports multiple types of models:
- **LLMs**: Large language models that take text input and produce text output
- **Chat Models**: Models that take a list of messages as input
- **Embeddings**: Models that generate vector representations of text

### 2. Prompts

Prompts are the instructions given to the language model:
- **PromptTemplate**: Templates for creating prompts
- **ChatPromptTemplate**: Templates for chat models
- **FewShotPromptTemplate**: Templates with few-shot examples

### 3. Chains

Chains combine multiple components into a pipeline:
- **LLMChain**: Combines a prompt with an LLM
- **SequentialChain**: Chains multiple chains sequentially
- **RouterChain**: Routes inputs to different chains based on conditions

### 4. Retrievers and Vector Stores

For RAG (Retrieval-Augmented Generation):
- **Document Loaders**: Load documents from various sources (PDF, HTML, text, etc.)
- **Text Splitters**: Split documents into manageable chunks
- **Vector Stores**: Store and retrieve document embeddings (FAISS, Chroma, Pinecone)
- **Retrievers**: Retrieve relevant documents based on a query

### 5. Memory

Memory allows chains to remember previous interactions:
- **ConversationBufferMemory**: Stores the entire conversation history
- **ConversationSummaryMemory**: Stores a summary of the conversation
- **VectorStoreRetrieverMemory**: Uses vector store to retrieve relevant past interactions

### 6. Agents

Agents use LLMs to decide which actions to take:
- **ReAct Agents**: Reason and Act based on observations
- **Plan-and-Execute Agents**: Plan a sequence of steps then execute
- **Custom Agents**: Define your own agent logic

## RAG (Retrieval-Augmented Generation) with LangChain

RAG is a technique that combines retrieval with generation:

1. **Indexing Phase**:
   - Load documents using Document Loaders
   - Split documents into chunks using Text Splitters
   - Embed chunks using Embeddings
   - Store in a Vector Store

2. **Retrieval Phase**:
   - User submits a query
   - Query is embedded using the same Embeddings model
   - Similar chunks are retrieved from the Vector Store

3. **Generation Phase**:
   - Retrieved chunks are used as context
   - LLM generates a response based on the context and query

## LangChain Expression Language (LCEL)

LCEL is a declarative way to compose chains using the pipe operator (`|`):

```python
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import ChatOpenAI

prompt = ChatPromptTemplate.from_template("Tell me about {topic}")
model = ChatOpenAI()
chain = prompt | model
result = chain.invoke({"topic": "Python"})
```

## Supported Integrations

LangChain integrates with numerous services:
- **LLM Providers**: OpenAI, Anthropic, Google, Hugging Face, Groq, Ollama
- **Vector Stores**: FAISS, Chroma, Pinecone, Weaviate, Milvus
- **Document Loaders**: PDF, Word, HTML, CSV, JSON, Notion, Google Drive
- **Databases**: SQLite, PostgreSQL, MongoDB
- **Tools**: Google Search, Wikipedia, Calculator, Python REPL
