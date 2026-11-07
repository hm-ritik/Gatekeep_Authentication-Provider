class AppError(Exception):
    """Base class for all domain errors."""


class TenantAlreadyExistsError(AppError):
    def __init__(self, slug: str):
        super().__init__(f"Tenant with slug '{slug}' already exists")
        self.slug = slug


class TenantNotFoundError(AppError):
    def __init__(self, slug: str) -> None:
        super().__init__(f"Tenant '{slug}' not found")   


class ClientAlreadyExistsError(AppError):
    def __init__(self, client_id: str):
            super().__init__(f"Tenant with slug '{client_id}' already exists")
            self.slug = client_id




class UserAlreadyExistsError(AppError):
    def __init__(self, email: str) -> None:
        super().__init__(f"User '{email}' already exists in this tenant")


class UserNotFoundError(AppError):
    def __init__(self, user: str) -> None:
        super().__init__(f"User '{user}' not found")