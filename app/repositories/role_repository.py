from sqlalchemy import select, delete
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from app.models.role import Role, Permission, UserRole, RolePermission

class RoleRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    
    async def create_role(self, role: Role) -> Role:
        """Create a new role"""
        self.db.add(role)
        await self.db.commit()
        await self.db.refresh(role)
        return role

    async def get_role_by_name(self, name: str) -> Optional[Role]:
        """Get role by name"""
        result = await self.db.execute(
            select(Role).where(Role.name == name)
        )
        return result.scalar_one_or_none()

    async def get_role_by_id(self, role_id: int) -> Optional[Role]:
        """Get role by ID"""
        result = await self.db.execute(
            select(Role).where(Role.id == role_id)
        )
        return result.scalar_one_or_none()

    async def get_all_roles(self) -> List[Role]:
        """Get all roles"""
        result = await self.db.execute(select(Role))
        return result.scalars().all()

    async def update_role(self, role: Role) -> Role:
        """Update role"""
        await self.db.commit()
        await self.db.refresh(role)
        return role

    async def delete_role(self, role: Role) -> None:
        """Delete role"""
        await self.db.delete(role)
        await self.db.commit()

  
    async def create_permission(self, permission: Permission) -> Permission:
        """Create a new permission"""
        self.db.add(permission)
        await self.db.commit()
        await self.db.refresh(permission)
        return permission

    async def get_permission_by_id(self, permission_id: int) -> Optional[Permission]:
        """Get permission by ID"""
        result = await self.db.execute(
            select(Permission).where(Permission.id == permission_id)
        )
        return result.scalar_one_or_none()

    async def get_permission_by_resource_action(self, resource: str, action: str) -> Optional[Permission]:
        """Get permission by resource:action"""
        result = await self.db.execute(
            select(Permission).where(
                Permission.resource == resource,
                Permission.action == action
            )
        )
        return result.scalar_one_or_none()

    async def get_all_permissions(self) -> List[Permission]:
        """Get all permissions"""
        result = await self.db.execute(select(Permission))
        return result.scalars().all()

   
    async def create_user_role(self, user_role: UserRole) -> UserRole:
        """Assign a role to a user"""
        self.db.add(user_role)
        await self.db.commit()
        await self.db.refresh(user_role)
        return user_role

    async def delete_user_role(self, user_role: UserRole) -> None:
        """Remove a role from a user"""
        await self.db.delete(user_role)
        await self.db.commit()

    async def get_user_roles(self, user_id: int, client_id: Optional[str] = None) -> List[UserRole]:
        """Get user's role assignments"""
        query = select(UserRole).where(UserRole.user_id == user_id)
        if client_id:
            query = query.where(UserRole.client_id == client_id)
        result = await self.db.execute(query)
        return result.scalars().all()

   
    async def create_role_permission(self, role_permission: RolePermission) -> RolePermission:
        """Add a permission to a role"""
        self.db.add(role_permission)
        await self.db.commit()
        await self.db.refresh(role_permission)
        return role_permission

    async def delete_role_permission(self, role_permission: RolePermission) -> None:
        """Remove a permission from a role"""
        await self.db.delete(role_permission)
        await self.db.commit()

    async def get_role_permissions(self, role_id: int) -> List[RolePermission]:
        """Get all permission assignments for a role"""
        result = await self.db.execute(
            select(RolePermission).where(RolePermission.role_id == role_id)
        )
        return result.scalars().all()