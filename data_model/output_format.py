import json


class OutputFormatEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, OutputFormat):  # YourClass에는 실제 클래스 이름을 사용합니다.
            return {
                "question_number": obj.question_number,
                "question": obj.question,
                "gt_number": obj.gt_number,
                "predict_number": obj.predict_number,
                "predict_solution": obj.predict_solution,
                "rag_confidence": obj.rag_confidence,
                "rag_content": obj.rag_content,
            }
        return super(OutputFormatEncoder, self).default(obj)


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
