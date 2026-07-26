from typing import Protocol

import pytest
from pydantic import UUID4, BaseModel

from clients.http.gateway.accounts.client import AccountsGatewayHTTPClient, build_accounts_gateway_http_client
from clients.http.gateway.accounts.schema import (
    AccountType,
    AccountViewSchema,
    OpenCreditCardAccountRequestSchema,
    OpenDebitCardAccountRequestSchema,
    OpenDepositAccountRequestSchema,
    OpenSavingsAccountRequestSchema,
)
from fixtures.users import UserFixture


class AccountFixture(BaseModel):
    user: UserFixture
    account: AccountViewSchema

    @property
    def account_id(self) -> UUID4:
        return self.account.id


class AccountFactory(Protocol):
    def __call__(
        self,
        account_type: AccountType,
        user: UserFixture | None = None,
    ) -> AccountFixture: ...


@pytest.fixture
def http_gateway_account_client() -> AccountsGatewayHTTPClient:
    return build_accounts_gateway_http_client()


@pytest.fixture
def account_factory(
    http_gateway_account_client: AccountsGatewayHTTPClient, function_user: UserFixture
) -> AccountFactory:
    def create(account_type: AccountType, user: UserFixture | None = None) -> AccountFixture:
        user = user or function_user
        user_id = user.user_id

        match account_type:
            case AccountType.DEPOSIT:
                return AccountFixture(
                    user=user,
                    account=http_gateway_account_client.open_deposit_account(
                        OpenDepositAccountRequestSchema(
                            user_id=user_id,
                        )
                    ).account,
                )

            case AccountType.SAVINGS:
                return AccountFixture(
                    user=user,
                    account=http_gateway_account_client.open_savings_account(
                        OpenSavingsAccountRequestSchema(
                            user_id=user_id,
                        )
                    ).account,
                )

            case AccountType.DEBIT_CARD:
                return AccountFixture(
                    user=user,
                    account=http_gateway_account_client.open_debit_card_account(
                        OpenDebitCardAccountRequestSchema(
                            user_id=user_id,
                        )
                    ).account,
                )

            case AccountType.CREDIT_CARD:
                return AccountFixture(
                    user=user,
                    account=http_gateway_account_client.open_credit_card_account(
                        OpenCreditCardAccountRequestSchema(
                            user_id=user_id,
                        )
                    ).account,
                )

            case _:
                raise ValueError(f"Unsupported account type: {account_type}")

    return create
