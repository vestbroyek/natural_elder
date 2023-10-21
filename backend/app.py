from flask import abort, Flask, jsonify
from langchain.chains import RetrievalQA
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.llms import OpenAI
from langchain.vectorstores import FAISS
from utils import get_risk_data

app = Flask(__name__)


@app.route("/")
def health_check():
    return jsonify({"success": True}, 200)


@app.route("/query/<prompt>")
def answer_query(prompt):
    embeddings = OpenAIEmbeddings()
    db = FAISS.load_local("arizona", embeddings)

    # Create a retrieval-based QA system
    qa = RetrievalQA.from_chain_type(
        llm=OpenAI(), chain_type="stuff", retriever=db.as_retriever()
    )

    # Run the query and print the result
    try:
        res = qa.run(prompt)
        return jsonify({"success": True, "prompt": prompt, "response": res}, 200)
    except:
        abort(500)


@app.route("/risk/<location>")
def return_risk(location):
    try:
        risk_data = get_risk_data(location)
        return jsonify({"success": True, "location": location, "data": risk_data}, 200)
    except:
        abort(500)


if __name__ == "__main__":
    app.run(debug=True)
