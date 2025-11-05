from .api_consumer import FakeAPI


def main() -> None:
    api = FakeAPI(timer=(2, 3))
    api.fetch_multiple(size=5, format_='csv')


if __name__ == "__main__":
    main()
