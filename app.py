import os
import re
import pandas as pd
from flask import Flask, request, render_template, jsonify
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables
load_dotenv()  # reads .env
api_key = os.getenv('OPENAI_API_KEY')

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

# System prompt for LLM
SYSTEM_PROMPT = """
You are a data analyst assistant. You are working with a pandas dataframe called df.
Write clean pandas code to answer the user's question.
NEVER use 'eval' or unsafe functions. Only use pandas and matplotlib.
Return ONLY the code between ```python ... ```.
"""

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    # 1. Read uploaded CSV
    file = request.files.get('file')
    if not file:
        return jsonify({'answer': 'Error: No file uploaded'}), 400
    df = pd.read_csv(file, parse_dates=['date'])

    # 2. User question
    question = request.form.get('question', '')
    if not question:
        return jsonify({'answer': 'Error: No question provided'}), 400

    # 3. Build messages
    messages = [
        {'role': 'system', 'content': SYSTEM_PROMPT},
        {'role': 'user', 'content': f"My question: {question}"}
    ]

    # 4. Query LLM for pandas code
    resp = client.chat.completions.create(
        model='gpt-4o',
        messages=messages,
        temperature=0
    )
    reply = resp.choices[0].message.content

    # 5. Extract code block
    match = re.search(r"```python(.*?)```", reply, re.DOTALL)
    if match:
        code = match.group(1).strip()
    else:
        return jsonify({'answer': 'Could not parse code from LLM.'}), 500

    # 6. Execute code safely
    local_vars = {'df': df.copy()}
    try:
        exec(code, {}, local_vars)
        result = local_vars.get('result', 'Code executed.')
    except Exception as e:
        result = f"Error running code: {e}"

    return jsonify({'answer': str(result)})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)