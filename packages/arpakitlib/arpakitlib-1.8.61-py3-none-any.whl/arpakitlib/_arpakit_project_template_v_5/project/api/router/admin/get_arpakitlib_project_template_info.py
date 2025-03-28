import fastapi
from fastapi import APIRouter

from project.api.authorize import require_user_token_dbm_api_authorize_middleware, APIAuthorizeData, \
    api_authorize, require_api_key_dbm_api_authorize_middleware
from project.api.schema.common import BaseRouteSO
from project.api.schema.out.common.error import ErrorCommonSO
from project.api.schema.out.common.raw_data import RawDataCommonSO
from project.sqlalchemy_db_.sqlalchemy_model import UserDBM
from project.util.arpakitlib_project_template import get_arpakitlib_project_template_info


class GetArpakitlibProjectTemplateInfoAdminRouteSO(BaseRouteSO, RawDataCommonSO):
    pass


api_router = APIRouter()


@api_router.get(
    "",
    name="Get arpakitlib project template info",
    status_code=fastapi.status.HTTP_200_OK,
    response_model=GetArpakitlibProjectTemplateInfoAdminRouteSO | ErrorCommonSO
)
async def _(
        *,
        request: fastapi.requests.Request,
        response: fastapi.responses.Response,
        api_auth_data: APIAuthorizeData = fastapi.Depends(api_authorize(middlewares=[
            require_api_key_dbm_api_authorize_middleware(
                require_active=True
            ), require_user_token_dbm_api_authorize_middleware(
                require_active_user_token=True,
                require_user_roles=[UserDBM.Roles.admin]
            )
        ]))
):
    arpakitlib_project_template_data = get_arpakitlib_project_template_info()
    return GetArpakitlibProjectTemplateInfoAdminRouteSO(raw_data=arpakitlib_project_template_data)
