class BaseUsecase:
    def __init__(self, repository) -> None:
        self._repository = repository

    def get_list(self, schema, context):
        return self._repository.read_by_options(schema, context)

    def get_by_id(self, id: int, context):
        return self._repository.read_by_id(id, context)

    def add(self, schema, context):
        return self._repository.create(schema, context)

    def patch(self, id: int, schema, context):
        return self._repository.update(id, schema, context)

    def patch_attr(self, id: int, attr: str, value, context):
        return self._repository.update_attr(id, attr, value, context)

    def put_update(self, id: int, schema, context):
        return self._repository.whole_update(id, schema, context)

    def remove_by_id(self, id, context):
        return self._repository.delete_by_id(id, context)
