from fastapi import HTTPException


class ItemNotExist(Exception):
    pass


class ActivityNotFoundException(HTTPException):
    def __init__(self, activity_id: int):
        super().__init__(
            status_code=404, detail=f"Вид деятельности с ID {activity_id} не найден"
        )


class InvalidActivityDataException(HTTPException):
    def __init__(self, message: str):
        super().__init__(
            status_code=400, detail=f"Некорректные данные вида деятельности: {message}"
        )


class DuplicateActivityNameException(HTTPException):
    def __init__(self, name: str):
        super().__init__(
            status_code=400,
            detail=f"Вид деятельности с названием '{name}' уже существует",
        )


class ParentActivityNotFoundException(HTTPException):
    def __init__(self, parent_id: int):
        super().__init__(
            status_code=400,
            detail=f"Родительский вид деятельности с ID {parent_id} не найден",
        )


class CircularDependencyException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=400,
            detail="Обнаружена циклическая зависимость в иерархии видов деятельности",
        )


class BuildingNotFoundException(HTTPException):
    def __init__(self, building_id: int):
        super().__init__(
            status_code=404, detail=f"Здание с ID {building_id} не найдено"
        )


class InvalidBuildingDataException(HTTPException):
    def __init__(self, message: str):
        super().__init__(
            status_code=400, detail=f"Некорректные данные здания: {message}"
        )


class DuplicateBuildingAddressException(HTTPException):
    def __init__(self, address: str):
        super().__init__(
            status_code=400, detail=f"Здание с адресом '{address}' уже существует"
        )


class InvalidCoordinatesException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=400,
            detail="Некорректные координаты. Широта должна быть от -90 до 90, долгота от -180 до 180",
        )


class InvalidAddressException(HTTPException):
    def __init__(self, message: str):
        super().__init__(status_code=400, detail=f"Некорректный адрес: {message}")


class OrganizationNotFoundException(HTTPException):
    def __init__(self, org_id: int):
        super().__init__(
            status_code=404, detail=f"Организация с ID {org_id} не найдена"
        )


class BuildingNotFoundException(HTTPException):
    def __init__(self, building_id: int):
        super().__init__(
            status_code=404, detail=f"Здание с ID {building_id} не найдено"
        )


class ActivityNotFoundException(HTTPException):
    def __init__(self, activity_id: int):
        super().__init__(
            status_code=404, detail=f"Вид деятельности с ID {activity_id} не найден"
        )


class InvalidCoordinatesException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=400,
            detail="Некорректные координаты. Широта должна быть от -90 до 90, долгота от -180 до 180",
        )


class InvalidRadiusException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=400,
            detail="Некорректный радиус. Радиус должен быть положительным числом",
        )


class InvalidBoundingBoxException(HTTPException):
    def __init__(self):
        super().__init__(
            status_code=400,
            detail="Некорректные границы области. Минимальные значения должны быть меньше максимальных",
        )


class DuplicateOrganizationNameException(HTTPException):
    def __init__(self, name: str):
        super().__init__(
            status_code=400, detail=f"Организация с названием '{name}' уже существует"
        )


class InvalidPhoneNumberException(HTTPException):
    def __init__(self, phone: str):
        super().__init__(
            status_code=400, detail=f"Некорректный формат номера телефона: {phone}"
        )
