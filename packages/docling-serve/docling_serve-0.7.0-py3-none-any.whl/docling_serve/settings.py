from pathlib import Path
from typing import Optional, Union

from pydantic_settings import BaseSettings, SettingsConfigDict

from docling_serve.datamodel.engines import AsyncEngine


class UvicornSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="UVICORN_", env_file=".env", extra="allow"
    )

    host: str = "0.0.0.0"
    port: int = 5001
    reload: bool = False
    root_path: str = ""
    proxy_headers: bool = True
    timeout_keep_alive: int = 60
    ssl_certfile: Optional[Path] = None
    ssl_keyfile: Optional[Path] = None
    ssl_keyfile_password: Optional[str] = None
    workers: Union[int, None] = None


class DoclingServeSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="DOCLING_SERVE_",
        env_file=".env",
        env_parse_none_str="",
        extra="allow",
    )

    enable_ui: bool = False
    artifacts_path: Optional[Path] = None
    static_path: Optional[Path] = None
    options_cache_size: int = 2
    allow_external_plugins: bool = False

    cors_origins: list[str] = ["*"]
    cors_methods: list[str] = ["*"]
    cors_headers: list[str] = ["*"]

    eng_kind: AsyncEngine = AsyncEngine.LOCAL
    eng_loc_num_workers: int = 2


uvicorn_settings = UvicornSettings()
docling_serve_settings = DoclingServeSettings()
