from enum import StrEnum


class HTTPRoutes(StrEnum):
    USERS = "/api/v1/users"
    CARDS = "/api/v1/cards"
    ACCOUNTS = "/api/v1/accounts"
    OPERATIONS = "/api/v1/operations"
    DOCUMENTS = "/api/v1/documents"
