from __init__ import *

@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )

@app.on_event("startup")
async def on_startup():
    db = session()
    user = db.query(User).filter(User.is_admin == True).all()
    if user:
        pass
    else:
        await create_admin(db)


@app.get("/")
def root_main():
    return RedirectResponse("/docs")


def start():
    if __name__ == "__main__":
        uvicorn.run("app:app", port=5000, reload=True)


start()
