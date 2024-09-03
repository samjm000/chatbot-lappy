## Main.py - test case for Neoadjuvant HR +'ve , HER 2 -ve patient - EC-D
## start code

##Imports
import os
from transformers import AutoModelForCausalLM, AutoTokenizer

model_name = "meta-llama/Llama-3.1-8B"
model = AutoModelForCausalLM.from_pretrained(model_name)
tokenizer = AutoTokenizer.from_pretrained(model_name)

#Set up document store
from haystack.document_stores import FAISSDocumentStore
document_store = FAISSDocumentStore(faiss_index_factory_str="Flat")

from haystack.nodes import Seq2SeqGenerator

#Set up generator 
generator = Seq2SeqGenerator(model_name="meta-llama/Llama-3.1-8B")

#Add PDF documents to Document Store
from haystack.utils import convert_files_to_docs
from haystack.nodes import DensePassageRetriever, PDFToTextConverter


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

# Set up retreiver
from haystack.nodes import DensePassageRetriever

retriever = DensePassageRetriever(
    document_store=document_store,
    query_embedding_model="facebook/dpr-question_encoder-single-nq-base",
    passage_embedding_model="facebook/dpr-ctx_encoder-single-nq-base"
)

#update embeddings
document_store.update_embeddings(retriever)

from haystack.pipelines import DocumentSearchPipeline
#initialize search pipeline
pipeline = DocumentSearchPipeline(retriever)

#test setup 
query = "What are the side effects of paclitaxel?"
result = pipeline.run(query = query, params ={"Retriever":{"top_k":10}})

print(result)