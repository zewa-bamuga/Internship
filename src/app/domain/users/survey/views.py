from typing import List

from a8t_tools.db import pagination, sorting
from dependency_injector import wiring
from fastapi import APIRouter, Depends, Header, HTTPException

from app.api import deps
from app.containers import Container
from app.domain.users.core import schemas
from app.domain.users.core.schemas import UserСhoiceSurvey
from app.domain.users.profile.views import user_token
# from app.domain.users.survey.command import SurveyCategoryUserAddCommand
from app.domain.users.survey.queries import SurveyManagementListQuery

router = APIRouter()


@router.get(
    "/categories",
    response_model=pagination.CountPaginationResults[schemas.Survey],
)
@wiring.inject
async def get(
        token: str = Header(...),
        query: SurveyManagementListQuery = Depends(wiring.Provide[Container.user.management_survey_list_query]),
        pagination: pagination.PaginationCallable[schemas.Survey] = Depends(
            deps.get_skip_limit_pagination_dep(schemas.Survey)),
        sorting: sorting.SortingData[schemas.SurveySorts] = Depends(
            deps.get_sort_order_sorting_dep(
                schemas.SurveySorts,
                schemas.SurveySorts.id,
                sorting.SortOrders.desc,
            )
        ),
) -> pagination.Paginated[schemas.Survey]:
    async with user_token(token):
        surveys = await query(schemas.SurveyListRequestSchema(pagination=pagination, sorting=sorting))
        return surveys


@router.post(
    "/categories",
    response_model=UserСhoiceSurvey,
)
@wiring.inject
async def choose(
        token: str,
        payload: UserСhoiceSurvey,
        # command: SurveyCategoryUserAddCommand = Depends(wiring.Provide[Container.user.user_choose_survey_query]),
) -> UserСhoiceSurvey:
    return