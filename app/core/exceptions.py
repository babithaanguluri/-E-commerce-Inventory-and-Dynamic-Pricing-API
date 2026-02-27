from fastapi import HTTPException, status

class APIException(HTTPException):
    def __init__(self, status_code: int, detail: str, error_code: str = None):
        super().__init__(status_code=status_code, detail=detail)
        self.error_code = error_code

class EntityNotFoundException(APIException):
    def __init__(self, entity_name: str, entity_id: any):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{entity_name} with id {entity_id} not found",
            error_code="ENTITY_NOT_FOUND"
        )

class InsufficientStockException(APIException):
    def __init__(self, sku: str, requested: int, available: int):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Insufficient stock for {sku}. Requested: {requested}, Available: {available}",
            error_code="INSUFFICIENT_STOCK"
        )
