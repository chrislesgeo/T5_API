from flask import Flask, request, jsonify
import json
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI

app = Flask(__name__)

# LangChain setup
llm = OpenAI(temperature=0.9)

# Define a simple PromptTemplate
template = """
You are an AI assistant. Based on the provided JSON data, generate a helpful response:
{data}
"""

prompt_template = PromptTemplate(template=template, input_variables=["data"])

@app.route('/process-json', methods=['POST'])
def process_json():
    # Ensure the request has a file and it's JSON
    if 'file' not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files['file']

    if file.filename == '':
        return jsonify({"error": "No file selected for uploading"}), 400

    if file.content_type != 'application/json':
        return jsonify({"error": "Uploaded file must be a JSON"}), 400

    try:
        # Read and parse the JSON file
        json_data = json.load(file)

        # Create a prompt with LangChain's prompt template
        prompt = prompt_template.format(data=json.dumps(json_data, indent=2))

        # Generate a response using LangChain’s LLM
        response = llm(prompt)

        return jsonify({"response": response})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
