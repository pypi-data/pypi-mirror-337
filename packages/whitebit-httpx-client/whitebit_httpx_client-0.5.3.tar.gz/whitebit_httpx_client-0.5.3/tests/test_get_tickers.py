from conftest import vcr_c  # noqa

from whitebit_httpx_client import WhiteBITClient


@vcr_c.use_cassette("ticker/test_get_ticker.yaml")
def test_get_tickers(white_bit_client: WhiteBITClient):
    tickers = white_bit_client.get_tickers()
    assert isinstance(tickers, dict)


@vcr_c.use_cassette("ticker/test_get_ticker.yaml")
async def test_async_get_tickers(white_bit_client: WhiteBITClient):
    tickers = await white_bit_client.async_get_tickers()
    assert isinstance(tickers, dict)
    assert len(tickers) > 100
