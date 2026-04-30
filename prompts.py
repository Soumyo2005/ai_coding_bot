def generate_code(language, problem, level):
    return f"""
You are an expert {language} developer.

Write {level} level {language} code for the following problem:

PROBLEM:
{problem}

REQUIREMENTS:
- Write clean and readable code
- Add comments where needed
- Follow best practices
- Handle errors properly

Provide ONLY the code.
"""


def explain_code(code):
    return f"""
Explain the following code in detail:

{code}
"""


def explain_code_simple(code):
    return f"""
Explain this code in a beginner-friendly way:

{code}
"""


def debug_code(code, error):
    return f"""
Debug this code.

CODE:
{code}

ERROR:
{error}

Find the issue and provide corrected code.
"""


def explain_concept(concept):
    return f"""
Explain this programming concept in simple terms with examples:

{concept}
"""