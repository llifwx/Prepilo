from pathlib import Path

from alembic import command
from alembic.config import Config

from app.core.config import get_settings

from app.modules.subjects import models as subjects_models  # noqa: F401
from app.modules.topics import models as topics_models  # noqa: F401
from app.modules.users import models as users_models  # noqa: F401


def migrate_local_database() -> None:
    settings = get_settings()
    if settings.app_env != "local":
        return

    backend_dir = Path(__file__).resolve().parents[2]
    alembic_config = Config(str(backend_dir / "alembic.ini"))
    alembic_config.set_main_option("script_location", str(backend_dir / "alembic"))
    command.upgrade(alembic_config, "head")
