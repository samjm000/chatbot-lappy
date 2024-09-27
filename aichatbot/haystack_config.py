from haystack.document_stores import InMemoryDocumentStore
from haystack.nodes import DensePassageRetriever, FARMReader
from haystack.pipelines import ExtractiveQAPipeline

document_store = InMemoryDocumentStore()
retriever = DensePassageRetriever(document_store=document_store)
reader = FARMReader(model_name_or_path="deepset/roberta-base-squad2")

pipeline = ExtractiveQAPipeline(reader, retriever)
