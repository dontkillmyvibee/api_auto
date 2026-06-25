from pydantic import HttpUrl

from tools.schema.schema_helpers import CamelCaseModel


class TariffSchema(CamelCaseModel):
    url: HttpUrl
    document: str


class ContractSchema(CamelCaseModel):
    url: HttpUrl
    document: str


class GetTariffDocumentResponseSchema(CamelCaseModel):
    tariff: TariffSchema


class GetContractDocumentResponseSchema(CamelCaseModel):
    contract: ContractSchema
