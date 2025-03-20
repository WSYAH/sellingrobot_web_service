import os
import time
#time.sleep(1000)

import uvicorn
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.docs import (
    get_redoc_html,
    get_swagger_ui_html,
    get_swagger_ui_oauth2_redirect_html,
)
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.responses import RedirectResponse

from app import app
from exceptions import CustomHTTPException

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

root = os.path.abspath(os.path.join(os.path.basename(__file__), "../"))
app.mount("/static", StaticFiles(directory=root + "/static"), name="static")


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="/static/swagger-ui-bundle.js",
        swagger_css_url="/static/swagger-ui.css",
    )


@app.get(app.swagger_ui_oauth2_redirect_url, include_in_schema=False)
async def swagger_ui_redirect():
    return get_swagger_ui_oauth2_redirect_html()


@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    return get_redoc_html(
        openapi_url=app.openapi_url,
        title=app.title + " - ReDoc",
        redoc_js_url="/static/redoc.standalone.js",
    )


@app.get("/")
async def index_html():
    url = app.url_path_for("custom_swagger_ui_html")
    response = RedirectResponse(url=url)
    return response


@app.exception_handler(CustomHTTPException)
async def custom_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.custom_resp,
    )




if __name__ == '__main__':
    # 终端启
    # uvicorn.run(app="main:app",reload=True,debug=True)
    # pycharm直接启
    uvicorn.run(app="main:app", host="0.0.0.0", port=9528, reload=True)
    # uvicorn.run(app="main:app", host="0.0.0.0", port=8040, workers=3)
