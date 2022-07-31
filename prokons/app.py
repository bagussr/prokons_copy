from __init__ import *


# exception for authorize required
@app.exception_handler(AuthJWTException)
def authjwt_exception_handler(request: Request, exc: AuthJWTException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.message}
    )
    


# event on aplicatioan run
@app.on_event("startup")
async def on_startup():
    db = session()
    user = db.query(User).filter(User.is_admin == True).all()
    if user:
        pass
    else:
        await create_admin(db)

# root endpoint and redirect to docs
@app.get("/")
def root_main():
    return RedirectResponse("/docs")


def start():
    if __name__ == "__main__":
        uvicorn.run("app:app", port=5000, reload=True)


start()
