from typing import Annotated, Any, Dict
import os

from fastapi import FastAPI, Depends, Header, Request, Response, Cookie
from fastapi.exceptions import HTTPException
from fastapi.requests import Request
from fastapi.responses import (
    JSONResponse,
    FileResponse,
    Response
)
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from jose import jwt

from src.routers.movies import movie_router
from src.utils.http_error_handler import HTTPErrorHandler

def dependecy1():
    print("Global dependency 1")

def dependecy2():
    print("Global dependency 2")

app = FastAPI(dependencies=[Depends(dependecy1), Depends(dependecy2)])
app.add_middleware(HTTPErrorHandler)
oauth2_schema = OAuth2PasswordBearer(tokenUrl="token")

users: Dict = {
    "ale": {"username": "ale", "email": "ale@mail.com", "password": "password"},
    "pablo": {"username": "pablo", "email": "pablo@mail.com", "password": "password"}
}

def encode_token(payload: Dict) -> str:
    return jwt.encode(payload, "MY_SECRET", algorithm="HS256")

def decode_token(token: Annotated[str, Depends(oauth2_schema)]) -> Dict:
    return users.get(
        jwt.decode(token, "MY_SECRET", algorithms=["HS256"])["username"]
    )


def get_headers(
    access_token: Annotated[str | None, Header()] = None,
    user_role: Annotated[str | None, Header()] = None
) -> Dict:
    return {"access_token": access_token, "user_role": user_role}

@app.post("/token")
def login(formdata: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Dict:
    user = users.get(formdata.username)

    if not user or formdata.password != user.get("password"):
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    token = encode_token({"username": user.get("username"), "email": user.get("email")})
    return {"access_token": token}


@app.get("/users/profile")
def profile(my_user: Annotated[dict, Depends(decode_token)]):
    return my_user


@app.get("/dashboard")
def dashboard(
    headers: Annotated[Dict, Depends(get_headers)],
    request: Request,
    response: Response,
):
    print("Request", request.headers)
    response.headers["user_status"] = "enabled"
    return {"access_token": headers.get("access_token"), "user_role": headers.get("user_role")}


@app.get("/root")
def get_root():
    response: Dict = JSONResponse(content={"msg": "holox"})
    response.set_cookie(key="username", value="alejandro", expires=10)
    return response


@app.get("/root-cookie")
def get_root_cookie(username: Annotated[str, Cookie()]):
    return username


@app.middleware("http")
async def http_error_handler(request: Request, call_next: Any) -> Response | JSONResponse:
    print("Middleware is running...")
    return await call_next(request)


app.title = "My first app using FastAPI"
app.version = "v0.0.1"
static_path = os.path.join(os.path.dirname(__file__), "static/")
templates_path = os.path.join(os.path.dirname(__file__), "templates/")
app.mount("/static", StaticFiles(directory=static_path), "static")
templates = Jinja2Templates(directory=templates_path)


@app.get("/", tags=("Home Main",))
def home(request: Request):
    return templates.TemplateResponse("index.html", {"message": "Welcome", "request": request})
    # return PlainTextResponse("Home")
    # return HTMLResponse("<h1>Hola desde FastAPI...</h1>")


#def common_params(start_date: str, end_date: str) -> Dict:
#    return {"start_date": start_date, "end_date": end_date}
# CommonDep = Annotated[Dict, Depends(common_params)]

class CommonDep:
    def __init__(self, start_date: str, end_date: str):
        self.start_date = start_date
        self.end_date = end_date




@app.get("/users")
def get_users(commons: CommonDep = Depends()):
    return f"User created between {commons.start_date} and {commons.end_date}"


@app.get("/customers")
def get_customers(commons: CommonDep = Depends()):
    return f"Customers created between {commons.start_date} and {commons.end_date}"


@app.get("/get-file")
def get_file():
    return FileResponse("out.txt")


app.include_router(prefix="/movies", router=movie_router)
