## Main.py - test case for Neoadjuvant HR +'ve , HER 2 -ve patient - EC-D

## Imports
import os
from haystack.document_stores import FAISSDocumentStore
from haystack.utils import convert_files_to_docs
from haystack.nodes import DensePassageRetriever, PDFToTextConverter
from haystack.pipelines import DocumentSearchPipeline
from haystack_integrations.components.generators.llama_cpp import LlamaCppChatGenerator

# Model setup with LlamaCppChatGenerator
generator = LlamaCppChatGenerator(
    model="/LLM/Meta-Llama-3.1-8B-Instruct-Q4_K_M-take2.gguf",
    n_ctx=512,
    n_batch=128,
    model_kwargs={"n_gpu_layers": -1},
    generation_kwargs={"max_tokens": 128, "temperature": 0.9},
)

# Set up document store
document_store = FAISSDocumentStore(faiss_index_factory_str="Flat")

# Initialize PDF converter
pdf_converter = PDFToTextConverter(remove_numeric_tables=True, valid_languages=["en"])

# Directory containing PDF files
pdf_dir = "cancer_docs"

# Fetch and process PDF files
documents = []
for filename in os.listdir(pdf_dir):
    if filename.endswith(".pdf"):
        file_path = os.path.join(pdf_dir, filename)
        docs = pdf_converter.convert(file_path=file_path, meta=None)
        documents.extend(docs)

# Write documents to the document store
document_store.write_documents(documents)

# Set up retriever
retriever = DensePassageRetriever(
    document_store=document_store,
    query_embedding_model="facebook/dpr-question_encoder-single-nq-base",
    passage_embedding_model="facebook/dpr-ctx_encoder-single-nq-base",
)

# Update embeddings
document_store.update_embeddings(retriever)

# Initialize search pipeline
pipeline = DocumentSearchPipeline(retriever)

# Test setup
query = "What are the side effects of paclitaxel?"
result = pipeline.run(query=query, params={"Retriever": {"top_k": 10}})

print(result)
