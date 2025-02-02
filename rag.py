# from langchain.document_loaders import DirectyLoader
# from langchain.text_splitter import RecursiveCharacterTextSplitter
# data_path="my_chroma_data/books/"

# def load_documents():
#     loader=DirectyLoader(data_path, glob="*.md")
#     documents=loader.load()
#     return documents

# def text_spliiter(documents):
#     text_splitter=RecursiveCharacterTextSplitter(
#         chunk_size=1000,
#         chunk_overlap=500,
#         length_function=len,
#         add_start_index=True
#     )


from pathlib import Path
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from langchain_community.llms import Ollama
import ollama
from langchain_community.vectorstores import Chroma
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings.fastembed import FastEmbedEmbeddings
from langchain_community.document_loaders import PDFPlumberLoader
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.chains import create_retrieval_chain
from langchain.prompts import PromptTemplate


app = Flask(__name__)

# def set_locale():
#     babel.locale_set('en_US')  # Set English (US) as the default language

folder_path = "db"

cached_llm = Ollama(model="llama3")
embedding = FastEmbedEmbeddings()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1024, chunk_overlap=80, length_function=len, is_separator_regex=False
)

raw_prompt = PromptTemplate.from_template(
    """
    <s>[INST] Tu es un assistant pédagogique qui aide les élèves à rédiger leur devoir. [/INST] </s>
    [INST] {input}
           Context: {context}
           Answer:
    [/INST]
"""
)

chat_history = [
    {
        "role": "system",
        "content": "Tu es un assistant pédagogique qui aide les élèves à rédiger leur devoir.",
    }
]


@app.route("/delete-document/<int:document_id>", methods=["DELETE"])
def delete_document(document_id):
    query = db.session.query(db.Model).filter_by(id=document_id)
    document = query.first()
    if document is None:
        return
    try:
        db.session.delete(document)
        db.session.commit()
    except Exception as e:
        return

    return jsonify({"message": "Document deleted successfully"}), 200


@app.route("/ai", methods=["POST"])
def aiPost():
    print("Post /ai called")
    json_content = request.json
    query = json_content.get("query")

    print(f"query: {query}")

    response = cached_llm.invoke(query)

    print(response)

    response_answer = {"answer": response}
    return response_answer


@app.route("/ask_pdf", methods=["POST"])
def askPDFPost():
    print("Post /ask_pdf called")
    json_content = request.json
    query = json_content.get("query")
    context=json_content.get("context", [])

    print(f"query: {query}")

    

    print("Loading vector store")
    vector_store = Chroma(persist_directory=folder_path, embedding_function=embedding)

    print("Creating chain")
    retriever = vector_store.as_retriever(
        search_type="similarity_score_threshold",
        search_kwargs={
            "k": 20,
            "score_threshold": 0.1,
        },
    )

    document_chain = create_stuff_documents_chain(cached_llm, raw_prompt)
    chain = create_retrieval_chain(retriever, document_chain)

    result = chain.invoke({"input": query})

    print(result)


    # print(result["answer"]["content"])

    # sources = []
    # for doc in result["context"]:
    #     sources.append(
    #         {"source": doc.metadata["source"], "page_content": doc.page_content}
    #     )

    # response_answer = {"answer": result["answer"], "sources": sources}
    # return response_answer


@app.route("/pdf", methods=["POST"])
def pdfPost():
    print("/pdf: got files:", request.files)
    file = request.files[
        "file"
    ]  # request => objet passé par flask et on récupère le fichier
    save_dir = Path(
        "~/.cache/rag/pdf"
    ).expanduser()  # directory de stockage(destination)
    save_dir.mkdir(parents=True, exist_ok=True)  # crée le directory si il n'existe pas
    save_file = save_dir.joinpath(file.filename)  # sauve le fichier dans le directory
    file.save(save_file)
    print(f"filename: {file.filename}")

    loader = PDFPlumberLoader(save_file)  # lit le pdf
    docs = loader.load_and_split()  # fais les chunks
    print(f"docs len={len(docs)}")

    chunks = text_splitter.split_documents(docs)
    print(f"chunks len={len(chunks)}")

    vector_store = Chroma.from_documents(
        documents=chunks, embedding=embedding, persist_directory=folder_path
    )

    vector_store.persist()

    response = {
        "status": "Successfully Uploaded",
        "filename": file.filename,
        "doc_len": len(docs),
        "chunks": len(chunks),
    }

    print(response)
    return response


def start_app():
    app.run(host="0.0.0.0", port=3030, debug=True)


if __name__ == "__main__":
    start_app()
