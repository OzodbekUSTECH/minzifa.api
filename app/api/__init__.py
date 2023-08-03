from api.routers.users import router as router_users
from api.routers.categories import router as router_categories
all_routers = [
    router_users,
    router_categories
]