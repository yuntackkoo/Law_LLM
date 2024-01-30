import vector_db_manager as manager
import json
single_object_json_test_str = '''
[
  {
    "name": "Object1",
    "remote_path": "/remote/path1",
    "local_path": "/local/path1",
    "model_name": "Model1",
    "model_type": "Type1",
    "describe": "Description for Object1"
  }
]
'''


def test_get_meta_from_json():
  origin = manager.VectorDBMetadata("Object1", "/remote/path1",
                                    "/local/path1",
                                    "Model1",
                                    "Type1", "Description for Object1")
  json_data = json.loads(single_object_json_test_str)[0]
  obj = manager.get_meta_from_json(json_data)
  assert origin == obj
