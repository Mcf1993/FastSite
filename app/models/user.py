from app.db.postgresql import engine
from datetime import datetime
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects import postgresql
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base(engine)


class User(Base):
    __tablename__ = 'user'
    id = Column(postgresql.INTEGER(), primary_key=True, index=True)
    username = Column(
        postgresql.VARCHAR(length=48),
        primary_key=False,
        index=True,
        unique=True,
        nullable=False,
        doc="用户名"
    )
    password = Column(
        postgresql.VARCHAR(length=256),
        primary_key=False,
        unique=False,
        nullable=False,
        doc="密码"
    )
    email = Column(
        postgresql.VARCHAR(length=256),
        primary_key=False,
        unique=True,
        nullable=True,
        doc="邮箱"
    )
    is_active = Column(
        postgresql.BOOLEAN(),
        default=True,
        doc="是否有效"
    )
    full_name = Column(
        postgresql.VARCHAR(length=64),
        primary_key=False,
        unique=False,
        nullable=True,
        doc="完整名称"
    )
    create_at = Column(
        postgresql.TIMESTAMP(),
        primary_key=False,
        default=datetime.now(),
        doc="创建日期"
    )
    last_login = Column(
        postgresql.TIMESTAMP(),
        primary_key=False,
        nullable=True,
        doc="上次登录"
    )
    is_manager = Column(
        postgresql.BOOLEAN(),
        default=False,
        doc="是否是管理者"
    )


class Permission(Base):
    __tablename__ = 'permission'
    id = Column(postgresql.INTEGER(), primary_key=True, index=True)
    code = Column(postgresql.VARCHAR(length=64), primary_key=False, index=True, nullable=False, doc="权限代码")
    display_name = Column(postgresql.VARCHAR(length=128), primary_key=False, index=True, nullable=False, doc="显示名称")


class PermissionGroup(Base):
    __tablename__ = 'permission_group'
    id = Column(postgresql.INTEGER(), primary_key=True, index=True)
    name = Column(postgresql.VARCHAR(length=128), primary_key=False, index=True, nullable=False, doc="分组名称")
    permission_id = Column(ForeignKey('permission.id'), index=True)

    permission = relationship('Permission')


class UserPermission(Base):
    __tablename__ = 'user_permission'
    id = Column(postgresql.INTEGER(), primary_key=True, index=True)
    permission_id = Column(ForeignKey('permission.id'), nullable=True, index=False)
    user_id = Column(ForeignKey('user.id'), nullable=True, index=False)

    permission = relationship('Permission')
    user = relationship('User')


class UserPermissionGroup(Base):
    __tablename__ = 'user_permission_group'
    id = Column(postgresql.INTEGER(), primary_key=True, index=True)
    user_id = Column(ForeignKey('user.id'), nullable=True, index=False)
    permission_group_id = Column(ForeignKey('permission_group.id'), nullable=True, index=False)

    user = relationship('User')
    permission_group = relationship('PermissionGroup')


