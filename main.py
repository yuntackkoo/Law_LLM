import os
import json
import tiktoken

import vector_db_helper.vector_db as db
import vector_db_helper.embedding_builder as embed

from langchain_community.chat_models import ChatOpenAI
from langchain_community.embeddings import OpenAIEmbeddings

import langchain.prompts as prompts

from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.callbacks.streaming_stdout_final_only import (
    FinalStreamingStdOutCallbackHandler,
)

import data_model.input_model as inmodel
import data_model.output_format as outmodel
import utils.util as utils

root_path = os.path.dirname(__file__) + "/"


def tiktoken_len(text: str) -> int:
    tokenizer = tiktoken.get_encoding("cl100k_base")
    tokens = tokenizer.encode(text)
    return len(tokens)


def load_template() -> str:
    template_path = root_path + "template/base.txt"
    return open(template_path, encoding="utf-8").read()


def load_vector_db() -> db.VectorDB:
    embed_model = embed.load_embeddings("jhgan/ko-sroberta-multitask")
    # embed_model = OpenAIEmbeddings(model="text-embedding-ada-002")
    database = db.VectorDB("./db/hugging", embed_model, load_spliter())
    return database


def load_openai_db(path: str) -> db.VectorDB:
    embed_model = OpenAIEmbeddings(model="text-embedding-ada-002")
    database = db.VectorDB(path, embed_model, load_spliter())
    return database


def load_llm():
    return ChatOpenAI(
        model_name="gpt-3.5-turbo",
        streaming=True,
        callbacks=[FinalStreamingStdOutCallbackHandler()],
        temperature=0,
    )


def load_spliter():
    return RecursiveCharacterTextSplitter(chunk_size=1024, length_function=tiktoken_len)


def get_absolute_paths(folder_path):
    absolute_paths = []
    if os.path.exists(folder_path):
        entries = os.listdir(folder_path)

        for entry in entries:
            entry_path = os.path.join(folder_path, entry)
            absolute_path = os.path.abspath(entry_path)

            if os.path.isfile(absolute_path):
                absolute_paths.append(absolute_path)

    return absolute_paths


def load_prompt():
    template = load_template()
    return prompts.PromptTemplate.from_template(template=template)


def append_pdf(pdf_path: str, store: db.VectorDB):
    data_list = get_absolute_paths(pdf_path)
    for data in data_list:
        store.append_pdf(data)


def create_vector_db():
    vector_db = load_vector_db()
    append_pdf(root_path + "data_set/", store=vector_db)
    vector_db.save()


def load_question() -> list:
    loader = inmodel.LocalLoader(root_path + "data_set/quest.csv")
    model = inmodel.InputModel(loader)
    return model.load_get_questions()


def save_result(path: str, results: list[outmodel.OutputFormat]):
    with open(path, "w", encoding="utf-8") as fd:
        json.dump(results, fd, cls=outmodel.OutputFormatEncoder)


def run():
    llm = load_llm()
    prompt = load_prompt()
    questions = load_question()
    results = []
    vector_db = load_openai_db(root_path + "example/db")

    for question in questions:
        try:
            result, rag, relevance = chain(
                store=vector_db, llm=llm, prompt=prompt, question=question["문제"]
            )
            gt_number, predict_solution = utils.parse_answer(result)
            if gt_number is None:
                gt_number = [0]
            if predict_solution is None:
                predict_solution = result
            output = outmodel.OutputFormat(
                question["문제번호"],
                question["문제"],
                question["정답번호"],
                gt_number,
                predict_solution,
                relevance,
                rag,
            )

            results.append(output)
        except Exception as e:
            print(e)

    with open(root_path + "result.json", "w", encoding="utf-8") as f:
        json.dump(results, default=outmodel.convert_to_dict,
                  fp=f, ensure_ascii=False)


def chain(store: db.VectorDB, llm, prompt, question: str):
    rag, relevance = store.query(question)
    input_prompt = prompt.format(rag=rag, question=question)
    result = llm.predict(input_prompt)
    return result, rag, relevance


run()
