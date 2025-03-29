from conftest import vcr_c  # noqa

from whitebit_httpx_client import WhiteBITClient


@vcr_c.use_cassette("markets/test_get_markets.yaml")
def test_get_markets(white_bit_client: WhiteBITClient):
    markets = white_bit_client.get_markets()
    assert isinstance(markets, list)
    assert len(markets) > 100


@vcr_c.use_cassette("markets/test_get_markets.yaml")
async def test_async_get_markets(white_bit_client: WhiteBITClient):
    markets = await white_bit_client.async_get_markets()
    assert isinstance(markets, list)
    assert len(markets) > 100
