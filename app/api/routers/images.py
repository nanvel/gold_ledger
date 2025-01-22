from dataclasses import replace
from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, UploadFile

from app.container import Container
from app.models import Image, User
from app.repos.uow import UnitOfFork
from app.services.images import ImagesService
from .auth import get_active_user

router = APIRouter()


@router.post("/images/upload")
@inject
async def upload_image(
    file: UploadFile,
    user: User = Depends(get_active_user),
    uow: UnitOfFork = Depends(Provide[Container.uow]),
    images_service: ImagesService = Depends(Provide[Container.images_service]),
) -> Image:
    image = images_service.upload(file.file, file_name=file.filename)

    image = replace(
        image,
        uploaded_by=user.id,
        supplier_id=user.supplier_id,
        retailer_id=user.retailer_id,
    )

    with uow:
        image_id = uow.images.create(image)

    image = replace(image, id=image_id)

    return image
