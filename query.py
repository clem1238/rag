import requests
import json


def query_model(query: str):
    data = {"query": query}
    r = requests.post(
        "http://localhost:3030/ai",
        data=json.dumps(data),
        headers={"Content-Type": "application/json"},
    )
    return r


def upload_files():
    file_path = "/home/user/Téléchargements/dormeur_du_val.pdf"
    with open(file_path, "rb") as f:
        response = requests.post("http://localhost:3030/pdf", files={"file": f})
    print(response)


def query_pdf(query: str):
    data = {"query": query}
    r = requests.post(
        "http://localhost:3030/ask_pdf",
        data=json.dumps(data),
        headers={"Content-Type": "application/json"},
    )
    return r


def run():
    # upload_files()
    queries = [
        "Récite moi 'le dormeur du val' de arthur rimbaud",
        "j'ai bien compris le contexte historique mais peux-tu me préciser les procédés littéraires utilisés dans la première strophe par exemple ?",
    ]
    for query in queries:
        r = query_pdf(query)
        # r = query_model(input(">>>>> "))
        print(r.json()["answer"])


if __name__ == "__main__":
    run()


# from flask import Flask, request, send_file
# import os

# app = Flask(__name__)

# @app.route('/upload', methods=['POST'])
# def upload_file():
#     if request.method == 'POST':
#         file = request.files['file']
#         filename = file.filename
#         file.save(os.path.join('uploads', filename))
#         return 'File uploaded successfully!'

# @app.route('/download/<filename>', methods=['GET'])
# def download_file(filename):
#     return send_file(os.path.join('uploads', filename), as_attachment=True)

# if __name__ == '__main__':
#     app.run(debug=True)
# # This code sets up a Flask web server that listens for POST requests to the `/upload` endpoint. When a
# # file is uploaded, it saves the file to a directory called `uploads`. It also sets up a GET route for
# # downloading files at the `/download/<filename>` endpoint.

# # You can then use the `requests` library to send an HTTP request to your local host and upload the PDF
# # file:

# import requests

# with open('path/to/your/pdf/file.pdf', 'rb') as f:
#     response = requests.post('http://localhost:5000/upload', files={'file': f})

# if response.status_code == 200:
#     print('File uploaded successfully!')
# else:
#     print('Error uploading file:', response.text)
