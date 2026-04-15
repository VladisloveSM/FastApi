from fastapi import HTTPException, status
from functools import wraps
from typing import Callable, Optional

class PermissionChecker:
    def __init__(self, roles: list[str]):
        self.roles = roles 

    def __call__(self, func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            user = kwargs.get("current_user")
            if not user:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Authentication required")

            if "admin" in user.roles: 
                return await func(*args, **kwargs)

            if not any(role in user.roles for role in self.roles):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Insufficient permissions for access"
                )
            return await func(*args, **kwargs)
        return wrapper

class OwnershipChecker:
    """
    Декоратор для проверки владения ресурсом.
    
    Проверяет, что пользователь может получить доступ к ресурсу только если:
    1. Он является владельцем ресурса (username совпадает)
    2. Он является администратором
    3. Ресурс является публичным (опционально)
    """
    def __init__(
        self,
        allow_public: bool = False,
        check_existence: bool = True,
        allow_admin_override: bool = True
    ):
        """
        Args:
            allow_public: Разрешить доступ к публичным ресурсам
            check_existence: Проверять существование ресурса (для GET/PUT/DELETE)
            allow_admin_override: Админы имеют доступ к любым ресурсам
        """
        self.allow_public = allow_public
        self.check_existence = check_existence
        self.allow_admin_override = allow_admin_override
    
    def __call__(self, func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            # Получаем текущего пользователя
            current_user = kwargs.get("current_user")
            if not current_user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Authentication required"
                )
            
            # Получаем username из параметров пути
            username = kwargs.get("username")
            if not username:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username parameter is required"
                )
            
            # Админы имеют доступ ко всем ресурсам
            if self.allow_admin_override and "admin" in current_user.roles:
                return await func(*args, **kwargs)
            
            # Импортируем RESOURCE здесь, чтобы избежать циклических импортов
            from app.db import RESOURCE
            
            # Проверка существования ресурса (для GET/PUT/DELETE)
            if self.check_existence:
                if username not in RESOURCE:
                    raise HTTPException(
                        status_code=status.HTTP_404_NOT_FOUND,
                        detail=f"Resource for user '{username}' not found"
                    )
                
                resource = RESOURCE[username]
                
                # Проверка публичности ресурса (если разрешено)
                if self.allow_public and hasattr(resource, 'is_public') and resource.is_public:
                    return await func(*args, **kwargs)
            
            # Проверка владения: username из пути должен совпадать с текущим пользователем
            if current_user.username != username:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Access denied. You can only access your own resources."
                )
            
            # Все проверки пройдены
            return await func(*args, **kwargs)
        
        return wrapper


class CreateOwnershipChecker:
    """
    Специальный декоратор для проверки создания ресурса.
    
    Пользователь может создать ресурс только под своим username.
    Админы могут создавать ресурсы для любого пользователя.
    """
    def __init__(self, allow_admin_override: bool = True):
        """
        Args:
            allow_admin_override: Админы могут создавать ресурсы для других пользователей
        """
        self.allow_admin_override = allow_admin_override
    
    def __call__(self, func: Callable):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            current_user = kwargs.get("current_user")
            if not current_user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Authentication required"
                )
            
            username = kwargs.get("username")
            if not username:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Username parameter is required"
                )
            
            # Админы могут создавать ресурсы для любого пользователя
            if self.allow_admin_override and "admin" in current_user.roles:
                return await func(*args, **kwargs)
            
            # Обычные пользователи могут создавать ресурсы только под своим username
            if current_user.username != username:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"You can only create resources under your own username ('{current_user.username}'). Cannot create for '{username}'."
                )
            
            # Проверяем, что ресурс еще не существует
            from app.db import RESOURCE
            if username in RESOURCE:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Resource for user '{username}' already exists"
                )
            
            return await func(*args, **kwargs)
        
        return wrapper