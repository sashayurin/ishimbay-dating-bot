from .user import router as user_router
from .admin import router as admin_router

def register_user_handlers(dp):
    dp.include_router(user_router)

def register_admin_handlers(dp):
    dp.include_router(admin_router)
