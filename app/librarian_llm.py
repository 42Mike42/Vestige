# librarian_llm.py
import subprocess
import json

def query_librarian(fragment: str):
    prompt = f"""You are Vestige, a reflective AI librarian. 
Evaluate this memory fragment and respond in JSON with the following fields:
- "score" (float between 0 and 1): likelihood this memory should be retained.
- "tags" (list of short strings): semantic or emotional categories (e.g. "nostalgia", "robotics", "speculation").
- "reason" (string): a brief explanation of why this memory is meaningful.

Memory fragment:
\"\"\"
{fragment}
\"\"\"
"""

    result = subprocess.run(
        ["ollama", "run", "llama3.2:3b", "--format", "json"],
        input=prompt.encode(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )

    try:
        output = result.stdout.decode()
        return json.loads(output)
    except Exception as e:
        return {"score": 0.5, "tags": ["uncategorized"], "reason": "Defaulted due to parsing error."}
