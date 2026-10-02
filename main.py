"""brettberger.me — content-managed link-hub site."""
from fastapi import FastAPI, Request, Form, HTTPException, Depends, Cookie
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pathlib import Path
import json, os, secrets, hashlib, hmac, time

APP_DIR = Path(__file__).parent
CONTENT_FILE = APP_DIR / "content.json"
SEED_FILE = APP_DIR / "content_seed.json"

ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "change-me-now")
SECRET_KEY = os.environ.get("SECRET_KEY", secrets.token_hex(32))
SESSION_COOKIE = "bb_session"
SESSION_HOURS = 24

app = FastAPI(title="brettberger.me")
app.mount("/static", StaticFiles(directory=str(APP_DIR / "static")), name="static")
templates = Jinja2Templates(directory=str(APP_DIR / "templates"))


def load_content() -> dict:
    if not CONTENT_FILE.exists():
        with open(SEED_FILE) as f:
            seed = json.load(f)
        save_content(seed)
        return seed
    with open(CONTENT_FILE) as f:
        return json.load(f)


def save_content(data: dict) -> None:
    CONTENT_FILE.write_text(json.dumps(data, indent=2))


def make_token() -> str:
    expires = int(time.time()) + SESSION_HOURS * 3600
    payload = f"{expires}"
    sig = hmac.new(SECRET_KEY.encode(), payload.encode(), hashlib.sha256).hexdigest()
    return f"{payload}.{sig}"


def verify_token(token):
    if not token or "." not in token:
        return False
    try:
        payload, sig = token.rsplit(".", 1)
        expected = hmac.new(SECRET_KEY.encode(), payload.encode(), hashlib.sha256).hexdigest()
        if not hmac.compare_digest(sig, expected):
            return False
        return int(payload) > int(time.time())
    except Exception:
        return False


def require_auth(session: str = Cookie(default=None, alias=SESSION_COOKIE)):
    if not verify_token(session):
        raise HTTPException(status_code=303, headers={"Location": "/admin/login"})
    return True


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("site.html", {"request": request, "c": load_content()})


@app.get("/writing", response_class=HTMLResponse)
def writing(request: Request):
    return templates.TemplateResponse("writing.html", {"request": request, "c": load_content()})


@app.get("/admin/login", response_class=HTMLResponse)
def login_page(request: Request, error: str = None):
    return templates.TemplateResponse("login.html", {"request": request, "error": error})


@app.post("/admin/login")
def login(password: str = Form(...)):
    if password != ADMIN_PASSWORD:
        return RedirectResponse("/admin/login?error=Invalid+password", status_code=303)
    resp = RedirectResponse("/admin", status_code=303)
    resp.set_cookie(SESSION_COOKIE, make_token(), httponly=True, samesite="lax",
                    max_age=SESSION_HOURS * 3600)
    return resp


@app.post("/admin/logout")
def logout():
    resp = RedirectResponse("/admin/login", status_code=303)
    resp.delete_cookie(SESSION_COOKIE)
    return resp


@app.get("/admin", response_class=HTMLResponse)
def admin_page(request: Request, _: bool = Depends(require_auth)):
    return templates.TemplateResponse("admin.html", {"request": request, "c": load_content()})


@app.post("/admin/save")
async def admin_save(request: Request, _: bool = Depends(require_auth)):
    body = await request.json()
    save_content(body)
    return JSONResponse({"ok": True})


@app.get("/admin/reset")
def admin_reset(_: bool = Depends(require_auth)):
    with open(SEED_FILE) as f:
        save_content(json.load(f))
    return RedirectResponse("/admin", status_code=303)


@app.get("/healthz")
def healthz():
    return {"ok": True}
