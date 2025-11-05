from src.api_consumer.fake_api import FakeAPI


def main() -> None:
    api = FakeAPI()
    api.fetch_multiple(size=5, format_='csv')


if __name__ == "__main__":
    main()
