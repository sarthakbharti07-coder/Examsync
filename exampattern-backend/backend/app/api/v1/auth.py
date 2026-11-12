from fastapi import APIRouter, HTTPException, Request, status
from sqlalchemy.exc import IntegrityError

from app.api.deps import CurrentUser, DbSession
from app.core.config import settings
from app.core.rate_limit import limiter
from app.core.security import DUMMY_HASH, create_access_token, hash_password, verify_password
from app.repositories import users as users_repo
from app.schemas.auth import LoginRequest, RegisterRequest, TokenResponse, UserOut

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
@limiter.limit(settings.auth_rate_limit)
def register(request: Request, body: RegisterRequest, db: DbSession):
    if users_repo.get_by_email(db, body.email):
        raise HTTPException(status.HTTP_409_CONFLICT, "An account with this email already exists")
    try:
        return users_repo.create(
            db, email=body.email, hashed_password=hash_password(body.password), full_name=body.full_name
        )
    except IntegrityError:  # lost a race with a concurrent registration
        db.rollback()
        raise HTTPException(status.HTTP_409_CONFLICT, "An account with this email already exists")


@router.post("/login", response_model=TokenResponse)
@limiter.limit(settings.auth_rate_limit)
def login(request: Request, body: LoginRequest, db: DbSession):
    user = users_repo.get_by_email(db, body.email)
    # Always run one hash verification so response time doesn't reveal which emails exist.
    ok = verify_password(body.password, user.hashed_password if user else DUMMY_HASH)
    if not user or not ok or not user.is_active:
        raise HTTPException(
            status.HTTP_401_UNAUTHORIZED, "Incorrect email or password", headers={"WWW-Authenticate": "Bearer"}
        )
    token, expires_in = create_access_token(user.id)
    return TokenResponse(access_token=token, expires_in=expires_in)


@router.get("/me", response_model=UserOut)
def me(user: CurrentUser):
    return user
