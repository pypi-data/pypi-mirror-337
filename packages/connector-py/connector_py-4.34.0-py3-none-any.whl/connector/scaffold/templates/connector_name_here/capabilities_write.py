from connector.generated import (
    AssignEntitlementRequest,
    AssignEntitlementResponse,
    ActivateAccountRequest,
    ActivateAccountResponse,
    CreateAccountRequest,
    CreateAccountResponse,
    DeactivateAccountRequest,
    DeactivateAccountResponse,
    DeleteAccountRequest,
    DeleteAccountResponse,
    UnassignEntitlementRequest,
    UnassignEntitlementResponse,
)


async def assign_entitlement(args: AssignEntitlementRequest) -> AssignEntitlementResponse:
    raise NotImplementedError


async def unassign_entitlement(
    args: UnassignEntitlementRequest,
) -> UnassignEntitlementResponse:
    raise NotImplementedError


async def create_account(
    args: CreateAccountRequest,
) -> CreateAccountResponse:
    raise NotImplementedError


async def delete_account(
    args: DeleteAccountRequest,
) -> DeleteAccountResponse:
    raise NotImplementedError


async def activate_account(
    args: ActivateAccountRequest,
) -> ActivateAccountResponse:
    raise NotImplementedError


async def deactivate_account(
    args: DeactivateAccountRequest,
) -> DeactivateAccountResponse:
    raise NotImplementedError
