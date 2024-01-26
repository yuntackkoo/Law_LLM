import json


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


def convert_to_dict(obj):
    if isinstance(obj, OutputFormat):
        return obj.__dict__
    return obj


class OutputFormat:
    def __init__(
        self,
        question_number: str,
        question: str,
        gt_number: list[int],
        predict_number: list[int],
        predict_solution: str,
        rag_confidence: float,
        rag_content: str,
    ) -> None:
        self.question_number = question_number
        self.question = question
        self.gt_number = gt_number
        self.predict_number = predict_number
        self.predict_solution = predict_solution
        self.rag_confidence = rag_confidence
        self.rag_content = rag_content
