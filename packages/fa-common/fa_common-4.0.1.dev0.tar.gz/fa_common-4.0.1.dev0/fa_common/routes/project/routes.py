from typing import Annotated, Optional

from bson import ObjectId
from fastapi import APIRouter, Depends, Query

from fa_common.auth.utils import get_admin_scope
from fa_common.exceptions import NotFoundError, UnauthorizedError
from fa_common.models import Message, PaginationListResponse
from fa_common.routes.user.models import UserDB
from fa_common.routes.user.service import get_current_app_user

from . import service
from .models import CreateProject, ProjectDB, UpdateProject

router = APIRouter()


@router.get("", response_model=PaginationListResponse[ProjectDB])
async def list_projects(
    only_mine: bool = True,
    offset: int = 0,
    limit: int = 10,
    search: Optional[str] = None,
    sort: Annotated[
        list[str], Query(description="The list of fields to sort the projects by using the syntax `['+fieldName', '-secondField']`.")
    ] = [],
    current_user: UserDB = Depends(get_current_app_user),
) -> PaginationListResponse[ProjectDB]:
    """
    List projects based on the provided filters.

    Parameters
    ----------
    only_mine : bool, optional
        If True, only return projects owned by the current user. If False, return all projects the user has access to. Default is True.
    offset : int, optional
        The number of projects to skip before starting to return results. Default is 0.
    limit : int, optional
        The maximum number of projects to return. Default is 10.
    search : str, optional
        Search string to filter projects by name or tags. Default is None.
    sort : list[str], optional
        The list of fields to sort the projects by using the syntax `['+fieldName', '-secondField']`.
        See https://beanie-odm.dev/tutorial/finding-documents/
        Default is an empty list.
    current_user : UserDB, optional
        The current authenticated user. Default is obtained using the `get_current_app_user` dependency.

    Returns
    -------
    PaginationListResponse[ProjectDB]
        A paginated list of projects that match the provided filters.
    """
    projects, total = await service.get_projects_for_user(
        user=current_user, owner_only=only_mine, offset=offset, limit=limit, sort=sort, search=search
    )

    return PaginationListResponse[ProjectDB](total=total, values=projects, limit=limit, offset=offset)


@router.put("", response_model=ProjectDB, response_model_exclude=ProjectDB._api_out_exclude())
async def create_project(
    project: CreateProject,
    current_user: UserDB = Depends(get_current_app_user),
) -> ProjectDB:
    new_project = await service.create_project(current_user, project.model_dump())

    return new_project


@router.patch("/{project_id}", response_model=ProjectDB, response_model_exclude=ProjectDB._api_out_exclude())
async def update_project(
    project_id: str,
    project_update: UpdateProject,
    current_user: UserDB = Depends(get_current_app_user),
) -> ProjectDB:
    project = await ProjectDB.find_one(ProjectDB.id == ObjectId(project_id))

    if project is None:
        raise NotFoundError(f"Project {project_id} not found.")

    if project.user_id != current_user.sub and current_user.sub not in project.project_users:
        raise UnauthorizedError("You do not have access to this project.")

    updated_project = await service.update_project(project, project_update)

    return updated_project


@router.get("/{project_id}", response_model=ProjectDB, response_model_exclude=ProjectDB._api_out_exclude())  # type: ignore
async def get_project(
    project_id: str,
    current_user: UserDB = Depends(get_current_app_user),
) -> ProjectDB:
    """Gets a project given the project_name."""
    project = await ProjectDB.find_one(ProjectDB.id == ObjectId(project_id))

    if project is None:
        raise NotFoundError(f"Project {project_id} not found.")

    if get_admin_scope() in current_user.roles:
        return project

    if project.user_id != current_user.sub and current_user.sub not in project.project_users:
        raise UnauthorizedError("You do not have access to this project.")

    return project


@router.delete("/{project_id}", response_model=Message)
async def delete_project(
    project_id: str,
    current_user: UserDB = Depends(get_current_app_user),
) -> Message:
    """Deletes a project given the project_name."""
    proj_id = ObjectId(project_id)
    user_sub = None
    if get_admin_scope() not in current_user.scopes:
        user_sub = current_user.sub

    delete_outcome = await service.delete(project_id=proj_id, user_sub=user_sub)

    if delete_outcome is False:
        raise NotFoundError()

    return Message(message=f"Deleted project {project_id}.")
