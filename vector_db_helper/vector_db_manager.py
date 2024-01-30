import json


class VectorDBMetadata:
  def __init__(
      self,
      name: str,
      remote_path: str,
      local_path: str,
      model_name: str,
      model_type: str,
      describe: str,
  ) -> None:
    self.name = name
    self.remote_path = remote_path
    self.local_path = local_path
    self.model_name = model_name
    self.model_type = model_type
    self.describe = describe

  def __eq__(self, other):
    if isinstance(other, VectorDBMetadata):
      return (
          self.name == other.name
          and self.remote_path == other.remote_path
          and self.local_path == other.local_path
          and self.model_name == other.model_name
          and self.model_type == other.model_type
          and self.describe == other.describe
      )
    return False


class VectorDBManager:
  def __init__(self) -> None:
    self._dbs = set()

  def load_db(self, name: str, path: str):
    json.loads(path)


def get_meta_from_json(obj: dict) -> VectorDBMetadata:
  return VectorDBMetadata(
      obj["name"],
      obj["remote_path"],
      obj["local_path"],
      obj["model_name"],
      obj["model_type"],
      obj["describe"],
  )
