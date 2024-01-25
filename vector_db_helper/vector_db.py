import langchain_core as core
import langchain.vectorstores as store
import langchain.document_loaders as loaders
import langchain.text_splitter as spliter
from typing import Any


def load_pdf_from_path(path) -> list[core.documents.Document]:
    loader = loaders.PyPDFLoader(path)
    pages = loader.load()
    return pages


class VectorDB:
    def __init__(
        self,
        db_path: str,
        embed_function: core.embeddings.Embeddings,
        split_stregy: Any,
    ) -> None:
        self.store = store.Chroma(
            persist_directory=db_path, embedding_function=embed_function
        )
        self.splitter = split_stregy

    def append_pages(self, pages):
        splited_doc = self.splitter.split_documents(pages)
        input_metas = [doc.metadata for doc in splited_doc]
        input_texts = [doc.page_content for doc in splited_doc]
        self.store.add_texts(texts=input_texts, metadatas=input_metas)

    def append_pdf(self, pdf_path: str):
        pages = load_pdf_from_path(pdf_path)
        self.append_pages(pages)

    def query(self, query: str) -> tuple:
        result = self.store.similarity_search_with_relevance_scores(query, k=1)[0]
        return result[0].page_content, result[1]

    def save(self):
        self.store.persist()
