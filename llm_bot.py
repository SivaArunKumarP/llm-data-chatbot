import os
import pandas as pd
from openai import OpenAI

# Set your API key
client = OpenAI(api_key="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")  # Replace with your real key

# Load dataset
df = pd.read_csv('sales.csv', parse_dates=['date'])

# System prompt
SYSTEM_PROMPT = """
You are a data analyst assistant. You are working with a pandas dataframe called df.
Write clean pandas code to answer the user's question.
NEVER use 'eval' or unsafe functions. Only use pandas and matplotlib.
Return ONLY the code between ```python ... ```.
"""

def query_llm(user_question):
    """Ask OpenAI to generate pandas code"""
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"My question: {user_question}"}
    ]
    response = client.chat.completions.create(
        model="gpt-4o",  # Use GPT-4o for faster and cheaper calls
        messages=messages,
        temperature=0
    )
    reply = response.choices[0].message.content

    # Extract python code from response
    import re
    code_match = re.search(r"```python(.*?)```", reply, re.DOTALL)
    if code_match:
        return code_match.group(1).strip()
    else:
        return None

def execute_code(code):
    """Run generated code on df and capture the output"""
    local_vars = {'df': df.copy()}
    try:
        exec(code, {}, local_vars)
        if 'result' in local_vars:
            print("✅ Result:\n", local_vars['result'])
        else:
            print("✅ Code executed successfully.")
    except Exception as e:
        print("❌ Error while running code:", e)

def main():
    print("🤖 Sales Insights Bot (LLM-powered). Ask questions about your dataset!")
    print("Type 'exit' to quit.\n")
    while True:
        user_question = input("You: ")
        if user_question.strip().lower() in ['exit', 'quit']:
            print("Bot: Goodbye!")
            break
        print("🔍 Generating code...")
        code = query_llm(user_question)
        if code:
            print("📜 Generated code:\n", code)
            execute_code(code)
        else:
            print("❌ Could not parse LLM response.")

if __name__ == "__main__":
    main()
