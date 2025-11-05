from .api_consumer import FakeAPI
from .settings import load_settings, Settings

def main() -> None:
    settings = load_settings()

    if settings.is_valid:
        api = FakeAPI(
            timer=settings.timer,
            root_dir=settings.root_dir,
        )
        api.fetch_multiple(size=settings.size, format_=settings.format_)


if __name__ == "__main__":
    main()
