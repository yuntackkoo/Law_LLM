from langchain.chat_models import ChatOpenAI
import langchain.prompts as prompts
import vector_db_helper.vector_db as db

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


llm = ChatOpenAI(
        model_name="gpt-3.5-turbo",
        streaming=True,
        callbacks=[FinalStreamingStdOutCallbackHandler()],
        temperature=0,
    )

prompt = prompts.PromptTemplate.from_template(template='''template''')
question = '''query'''

rag, relevance = database.query(question)
input = prompt.format(rag=rag, question=question)
result = llm.predict(input)
