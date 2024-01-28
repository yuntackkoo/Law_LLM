import vector_db_helper.vector_db as db
from langchain.embeddings import OpenAIEmbeddings

def tiktoken_len(text: str) -> int:
    tokenizer = tiktoken.get_encoding("cl100k_base")
    tokens = tokenizer.encode(text)
    return len(tokens)

#vector db 경로
DB_PATH = "./db/hugging"

embed_model = OpenAIEmbeddings(model="text-embedding-ada-002")
spliter = RecursiveCharacterTextSplitter(chunk_size=1024, length_function=tiktoken_len)

#설정된 db 경로에 db가 있으면 로드 아니면 빈 db를 생성
database = db.VectorDB(DB_PATH, embed_model, spliter)

#pdf 추가
database.append_pdf("pdf 경로")

#문자열 추가
database.append_pages("텍스트")

#설정된 db 경로에 저장
database.save()

#입력 문자열의 반환으로 rag와 신뢰도를 반환
database.query("querys...")
