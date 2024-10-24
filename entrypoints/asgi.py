import uvicorn

from settings import get_settings
from web.application import create_application

settings = get_settings()
application = create_application(settings)

if __name__ == '__main__':
    uvicorn.run(
        app="entrypoints.asgi:application",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.API_DEBUG
    )
