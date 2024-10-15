from flask import Flask, request, jsonify
import json
from langchain.prompts import PromptTemplate
from langchain.llms import OpenAI
import google.generativeai as genai
import os
from api import gemApi

os.environ["GOOGLE_API_KEY"] = gemApi
genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
app = Flask(__name__)

# LangChain setup
model = genai.GenerativeModel(model_name = "gemini-pro")

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

    # if file.content_type != 'application/json':
    #     return jsonify({"error": "Uploaded file must be a JSON"}), 400

    try:
        
        # Instead of treating file like a dictionary, use file.read() to get its contents
        file_contents = file.read()
            
        
        # Read and parse the JSON file content
        # json_data = jsonify(file)

        # Create a prompt with LangChain's prompt template
        # prompt = prompt_template.format(data=json.dumps(json_data, indent=2))

        # Generate a response using LangChain’s LLM
        # response =  model.generate_content(json_data["question"]).text

        return jsonify({"response": type(file)})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
