from src.repository.business_repository import BusinessRepository
from src.usecase.base_usecase import BaseUsecase


class BusinessUsecase(BaseUsecase):
    def __init__(self, business_repository: BusinessRepository):
        self.business_repository = business_repository
        super().__init__(business_repository)
