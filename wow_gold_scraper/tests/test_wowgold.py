import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
import wowgold as w

HTML = """<html><head><title>Gold Guide</title>
<meta property="article:modified_time" content="2026-08-11T10:00:00Z">
<script>var x=1</script></head><body><nav>menu</nav><main>
<h1>Gold</h1><h2>Herbs</h2><p>Fly the loop.</p><ul><li>Item A</li></ul>
<table><tr><th>Farm</th><th>Gold</th></tr><tr><td>Herbs</td><td>100k</td></tr></table>
</main><footer>bye</footer></body></html>"""


def test_html_to_text():
    d = w.html_to_text(HTML)
    assert d["title"] == "Gold Guide"
    assert any("2026-08-11" in x for x in d["dates"])
    assert "menu" not in d["text"] and "var x" not in d["text"] and "bye" not in d["text"]
    assert "## Herbs" in d["text"] and "- Item A" in d["text"] and "Farm | Gold" in d["text"]


def test_price_stats_order_book():
    # 50 @ 1g, 60 @ 2g, 100 @ 10g (copper unit_price)
    a = [{"quantity": 50, "unit_price": 10000}, {"quantity": 60, "unit_price": 20000}, {"quantity": 100, "unit_price": 100000}]
    s = w.price_stats(a)
    assert s.floor == 1.0
    assert s.units == 210 and s.listings == 3
    assert s.buy_100 == (50 * 1 + 50 * 2) / 100  # 1.5g avg for first 100
    assert s.median == 2.0  # 105th unit sits in the 2g tier


def test_price_stats_thin_market_has_no_depth_price():
    assert w.price_stats([{"quantity": 10, "unit_price": 10000}]).buy_100 is None
    assert w.price_stats([]) is None


def test_group_and_farm_calc():
    auctions = [{"item": {"id": 1}, "quantity": 500, "unit_price": 50000}, {"item": {"id": 2}, "quantity": 5, "unit_price": 1}]
    g = w.group_by_item(auctions, {1})
    assert list(g) == [1] and len(g[1]) == 1
    prices = {"Ore": w.price_stats(g[1]), "Missing": None}
    farm = {"direct_gold_per_hour": 1000, "items": [{"name": "Ore", "per_hour": 100}, {"name": "Missing", "per_hour": 9}]}
    gph, notes = w.farm_gold_per_hour(farm, prices, 0.05)
    assert abs(gph - (1000 + 100 * 5.0 * 0.95)) < 1e-6
    assert len(notes) == 1


class FakeResp:
    def __init__(self, status, text="", js=None):
        self.status_code, self.text, self._js = status, text, js

    def json(self):
        return self._js

    def raise_for_status(self):
        if self.status_code >= 400:
            raise RuntimeError(self.status_code)


class FakeSession:
    def __init__(self, routes):
        self.routes, self.headers, self.calls = routes, {}, []

    def get(self, url, **kw):
        self.calls.append(url)
        return self.routes.get(url, FakeResp(404))

    def post(self, url, **kw):
        return FakeResp(200, js={"access_token": "tok"})


def test_fetcher_respects_robots_and_reports_blocks(tmp_path, monkeypatch):
    monkeypatch.setattr(w, "CACHE", tmp_path)
    s = FakeSession({
        "https://a.test/robots.txt": FakeResp(200, "User-agent: *\nDisallow: /private\n"),
        "https://a.test/ok": FakeResp(200, HTML),
        "https://a.test/private": FakeResp(200, HTML),
        "https://b.test/robots.txt": FakeResp(404),
        "https://b.test/x": FakeResp(403),
    })
    f = w.PoliteFetcher(delay=0, session=s)
    assert f.get("https://a.test/ok")[0] == 200
    assert f.get("https://a.test/ok")[2] is True  # served from cache
    assert f.get("https://a.test/private")[0] == -1
    assert "https://a.test/private" not in s.calls
    assert f.get("https://b.test/x")[0] == 403


def test_blizzard_item_lookup_exact_match():
    s = FakeSession({"https://eu.api.blizzard.com/data/wow/search/item": FakeResp(200, js={"results": [
        {"data": {"id": 5, "name": {"en_GB": "Silver Ore Bar"}}}, {"data": {"id": 7, "name": {"en_GB": "Silver Ore"}}}]})})
    api = w.Blizzard("i", "s", session=s)
    assert api.find_item_id("silver ore") == 7
    assert api.find_item_id("nope") is None
