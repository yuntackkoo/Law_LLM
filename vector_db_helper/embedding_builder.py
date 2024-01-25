import langchain.embeddings as embed
from langchain_core.embeddings import Embeddings

def load_embeddings(model_name:str) -> Embeddings:
    model_kwargs = {"device": "cpu"}
    encode_kwargs ={'normalize_embeddings': True}
    hf = embed.HuggingFaceEmbeddings(model_name=model_name,
                                model_kwargs=model_kwargs,
                                encode_kwargs=encode_kwargs)
    return hf
