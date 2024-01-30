import re
import ast


def parse_answer(answer: str) -> tuple:
  numbers = [0]
  explain = answer
  try:
    pattern = re.compile(r"\[([\d,\s]+)\],\s*<([^>]+)>")
    mat = pattern.match(answer)

    if mat:
      numbers = list(map(ast.literal_eval, mat.group(1).split(",")))
      explain = mat.group(2)
  except (ValueError, SyntaxError) as e:
    print(f"Error: {e}")
  finally:
    return numbers, explain
