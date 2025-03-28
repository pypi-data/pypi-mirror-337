import fastapi.requests
from fastapi import APIRouter

from project.api.authorize import APIAuthorizeData, api_authorize, require_api_key_dbm_api_authorize_middleware, \
    require_user_token_dbm_api_authorize_middleware
from project.api.schema.common import BaseRouteSO
from project.api.schema.out.common.error import ErrorCommonSO
from project.sqlalchemy_db_.sqlalchemy_model import OperationDBM, UserDBM


class GetOperationAllowedStatusesAdminRouteSO(BaseRouteSO):
    allowed_statuses: list[str]


api_router = APIRouter()


@api_router.get(
    "",
    name="Get operation allowed statuses",
    status_code=fastapi.status.HTTP_200_OK,
    response_model=GetOperationAllowedStatusesAdminRouteSO | ErrorCommonSO,
)
async def _(
        *,
        request: fastapi.requests.Request,
        response: fastapi.responses.Response,
        api_auth_data: APIAuthorizeData = fastapi.Depends(api_authorize(middlewares=[
            require_api_key_dbm_api_authorize_middleware(
                require_active=True
            ),
            require_user_token_dbm_api_authorize_middleware(
                require_active_user_token=True,
                require_user_roles=[UserDBM.Roles.admin]
            )
        ]))
):
    return GetOperationAllowedStatusesAdminRouteSO(
        allowed_statuses=OperationDBM.Statuses.values_list()
    )
