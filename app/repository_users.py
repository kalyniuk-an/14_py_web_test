from sqlalchemy.orm import Session

from app.models import User
from app.schemas import UserCreate
from app.services.auth import auth_service


def get_user_by_email(email: str, db: Session) -> User | None:
    """Retrieve a user by email address.

    Args:
        email (str): Email address to search for.
        db (Session): SQLAlchemy database session.

    Returns:
        User | None: The user if found, otherwise None.
    """
    return db.query(User).filter(User.email == email).first()


def create_user(body: UserCreate, db: Session) -> User:
    """Create a new user with a hashed password.

    Args:
        body (UserCreate): User registration data.
        db (Session): SQLAlchemy database session.

    Returns:
        User: The created user.
    """
    hashed_password = auth_service.get_password_hash(body.password)


    user = User(
        username=body.username,
        email=body.email,
        password=hashed_password,
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return user


def update_token(user: User, refresh_token: str | None, db: Session) -> None:
    """Update the refresh token for a user.

    Args:
        user (User): User whose token is updated.
        refresh_token (str | None): New refresh token or None.
        db (Session): SQLAlchemy database session.

    Returns:
        None: No value is returned.
    """
    user.refresh_token = refresh_token
    db.commit()


def confirm_user_email(user: User, db: Session) -> None:
    """Confirm a user's email address.

    Args:
        user (User): User whose email is confirmed.
        db (Session): SQLAlchemy database session.

    Returns:
        None: No value is returned.
    """
    user.confirmed = True
    db.commit()
    db.refresh(user)


def update_avatar(user: User, avatar_url: str, db: Session) -> User:
    """Update the user's avatar URL.

    Args:
        user (User): User whose avatar is updated.
        avatar_url (str): URL of the new avatar.
        db (Session): SQLAlchemy database session.

    Returns:
        User: The updated user.
    """
    user.avatar = avatar_url
    db.commit()
    db.refresh(user)

    return user
