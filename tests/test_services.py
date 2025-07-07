from services.exchange_factory import ExchangeFactory

def test_get_client_default():
    client = ExchangeFactory.get_client()
    assert client is not None
