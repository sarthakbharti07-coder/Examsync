from functools import lru_cache

from supabase import Client, create_client

from app.core.config import settings


@lru_cache
def get_storage_client() -> Client:
    if not settings.supabase_url or not settings.supabase_secret_key:
        raise RuntimeError("Supabase Storage credentials are not configured")

    return create_client(
        settings.supabase_url,
        settings.supabase_secret_key,
    )


def upload_file(storage_key: str, content: bytes) -> None:
    client = get_storage_client()

    client.storage.from_(settings.supabase_storage_bucket).upload(
        path=storage_key,
        file=content,
        file_options={
            "content-type": "application/pdf",
            "upsert": "false",
        },
    )


def delete_file(storage_key: str) -> None:
    client = get_storage_client()

    client.storage.from_(settings.supabase_storage_bucket).remove([storage_key])
