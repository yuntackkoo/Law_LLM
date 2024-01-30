import json
import dataclasses
import output_format as outformat


def test_output_format_serialize():
  test_json = ('{'
               '"question_number": "1",'
               '"question": "question",'
               '"gt_number": [1, 2],'
               '"predict_number": [1, 2],'
               '"predict_solution": "solution",'
               '"rag_confidence": 0.75,'
               '"rag_content": "rag"'
               '}'
               )
  obj = outformat.OutputFormat('1', 'question', [1, 2], [
                               1, 2], 'solution', 0.75, 'rag')
  result_str = json.dumps(obj, default=dataclasses.asdict,
                          ensure_ascii=False)

  assert json.loads(test_json) == json.loads(result_str)


def test_output_format_deserialize():
  test_json = ('{'
               '"question_number": "1",'
               '"question": "question",'
               '"gt_number": [1, 2],'
               '"predict_number": [1, 2],'
               '"predict_solution": "solution",'
               '"rag_confidence": 0.75,'
               '"rag_content": "rag"'
               '}'
               )
  obj = outformat.OutputFormat('1', 'question', [1, 2], [
                               1, 2], 'solution', 0.75, 'rag')
  result_obj = json.loads(
    test_json, object_hook=lambda d: outformat.OutputFormat(**d))

  assert obj == result_obj
