from haystack.document_stores import InMemoryDocumentStore
from haystack.nodes import DensePassageRetriever, FARMReader, PDFToTextConverter, PreProcessor
from haystack.pipelines import ExtractiveQAPipeline
from haystack.utils import convert_files_to_docs
from haystack.schema import Document

# Initialize the Document Store
document_store = InMemoryDocumentStore()

# Initialize the Retriever
retriever = DensePassageRetriever(
    document_store=document_store,
    query_embedding_model="facebook/dpr-question_encoder-single-nq-base",
    passage_embedding_model="facebook/dpr-ctx_encoder-single-nq-base"
)

# Initialize the Pipeline without the Reader
pipeline = ExtractiveQAPipeline(retriever=retriever)

# Convert PDFs to Documents
converter = PDFToTextConverter()
preprocessor = PreProcessor(
    clean_empty_lines=True,
    clean_whitespace=True,
    split_by="word",
    split_length=200,
    split_respect_sentence_boundary=True
)

# Path to your PDFs
pdf_dir = "./cancer_docs"

# Convert and Preprocess PDFs
docs = convert_files_to_docs(dir_path=pdf_dir, converter=converter, preprocessor=preprocessor)
document_store.write_documents(docs)

# Update Embeddings
document_store.update_embeddings(retriever)

if __name__ == "__main__":
    print("running test")
