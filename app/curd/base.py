from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from typing import TypeVar, Generic, Type, Union, Dict, Any, List
from sqlalchemy.orm import Session
from sqlalchemy.sql import func


Model = TypeVar('Model', bound=BaseModel)
CreateModel = TypeVar('CreateModel', bound=BaseModel)
UpdateModel = TypeVar('UpdateModel', bound=BaseModel)


class CURDBase(Generic[Model, CreateModel, UpdateModel]):
    def __init__(self, model: Type[Model]):
        self.model = model

    def get(self, db: Session, pk: int) -> Model:
        return db.query(self.model).filter(self.model.id == pk).first()

    def get_all(self, db: Session) -> List[Model]:
        return db.query(self.model).all()

    def filter_all(self, db: Session, filter_params: List[Any]) -> List[Model]:
        return db.query(self.model).filter(*filter_params).all()

    def filter_pagination(self, db: Session, filter_params: Union[List[Any]],
                          page: Union[int], page_size: Union[int] = 20) -> Dict[str, Any]:
        db_query = db.query(self.model)
        instance_count = db.query(func.count(self.model.id)).filter(
            *filter_params
        ).scalar()
        if filter_params is not None:
            db_query = db_query.filter(**filter_params)
        if page is not None and isinstance(page, int) and page > 1:
            db_query = db_query.offset((page - 1) * page_size)
        if page_size is not None and isinstance(page_size, int):
            db_query = db_query.limit(page_size)
        return {
            'count': instance_count,
            'results': db_query.all()
        }

    def create(self, db: Session, create_dict: CreateModel) -> Model:
        db_model = jsonable_encoder(create_dict)
        create_obj = self.model(**db_model)
        db.add(create_obj)
        db.commit()
        db.refresh(create_obj)
        return create_obj

    def delete(self, db: Session, pk: int) -> None:
        instance_obj = self.get(db, pk)
        if instance_obj:
            db.delete(instance_obj)
            db.commit()

    def update(self, db: Session, instance: Model, data_dict: Union[UpdateModel, Dict[str, Any]]) -> Model:
        instance_obj = jsonable_encoder(instance)
        update_data = data_dict
        if not isinstance(data_dict, dict):
            update_data = data_dict.dict(exclude_unset=True)
        for field in instance_obj:
            if field in update_data:
                setattr(instance, field, update_data[field])
        db.add(instance)
        db.commit()
        db.refresh(instance)
        return instance
