import json
from dataclasses import dataclass


class OutputFormatEncoder(json.JSONEncoder):
  def default(self, o):
    if isinstance(o, OutputFormat):  # YourClass에는 실제 클래스 이름을 사용합니다.
      return {
          "question_number": o.question_number,
          "question": o.question,
          "gt_number": o.gt_number,
          "predict_number": o.predict_number,
          "predict_solution": o.predict_solution,
          "rag_confidence": o.rag_confidence,
          "rag_content": o.rag_content,
      }
    return super(OutputFormatEncoder, self).default(o)


@dataclass
class OutputFormat:
  question_number: str
  question: str
  gt_number: list[int]
  predict_number: list[int]
  predict_solution: str
  rag_confidence: float
  rag_content: str
