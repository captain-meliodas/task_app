from src.app import main_app
from src.config.config import Settings
import uvicorn

def run_server():
    settings = Settings.get_settings()
    app = main_app()

    if settings.ssl_cert and settings.ssl_key:
        uvicorn.run(app,host=settings.bind_ip,port=settings.port,ssl_keyfile=settings.ssl_key,ssl_certfile=settings.ssl_cert)
    else:
        uvicorn.run(app,host=settings.bind_ip,port=settings.port)

if __name__ =="__main__":
    run_server()