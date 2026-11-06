class AppError(Exception):
    """Base class for all domain errors."""


class TenantAlreadyExistsError(AppError):
    def __init__(self, slug: str) 
        super().__init__(f"Tenant with slug '{slug}' already exists")
        self.slug = slug