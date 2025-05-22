from sqlalchemy.orm import Session
from database import URL
from cache import cache_url, get_cached_url


# Create and return a shortened URL
def create_short_url(db: Session, original_url: str, short_code: str) -> URL:
    url = URL(original_url=original_url, short_code=short_code)
    db.add(url)
    db.commit()
    db.refresh(url)

    # Cache the mapping
    cache_url(short_code, original_url)
    return url


# Fetch the original URL by short code
def get_original_url(db: Session, short_code: str) -> str:
    # Check Redis cache first
    cached = get_cached_url(short_code)
    if cached:
        return cached

    # Fallback to database
    url = db.query(URL).filter(URL.short_code == short_code).first()
    if url:
        url.clicks += 1
        db.commit()
        # Update cache
        cache_url(short_code, url.original_url)
        return url.original_url

    return None


# Check if short code already exists
def short_code_exists(db: Session, code: str) -> bool:
    return db.query(URL).filter(URL.short_code == code).first() is not None
