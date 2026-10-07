#!/usr/bin/env python3
"""WoW gold research toolkit (EU, Retail).

Subcommands
  pages   Fetch guide pages (robots.txt respected, rate limited, cached) -> clean text in out/pages/
  token   Current EU WoW Token price from the official Blizzard API
  prices  Live EU commodity-AH prices for items in watchlist.txt (official Blizzard API)
  farms   Gold/hour for farms in a yaml file, computed from live prices

Prices come from Blizzard's own API, not from third-party sites, so they are first-hand.
Guide pages are only evidence for *what* to farm; gold/hour is always computed from live prices.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import time
import urllib.robotparser
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
import yaml
from bs4 import BeautifulSoup

ROOT = Path(__file__).parent
OUT = ROOT / "out"
CACHE = ROOT / ".cache"
USER_AGENT = "wowgold-research/1.0 (personal research; respects robots.txt)"
REGION = "eu"
NAMESPACE_DYNAMIC = "dynamic-eu"
NAMESPACE_STATIC = "static-eu"
LOCALE = "en_GB"
COPPER_PER_GOLD = 10_000


# ----------------------------------------------------------------------------- pages


class PoliteFetcher:
    """GET with robots.txt check, per-host delay, on-disk cache. Never tries to evade blocks."""

    def __init__(self, delay: float = 3.0, cache_hours: float = 12.0, session=None):
        self.delay = delay
        self.cache_seconds = cache_hours * 3600
        self.session = session or requests.Session()
        self.session.headers["User-Agent"] = USER_AGENT
        self._robots: dict[str, urllib.robotparser.RobotFileParser | None] = {}
        self._last_hit: dict[str, float] = {}
        CACHE.mkdir(exist_ok=True)

    def _allowed(self, url: str) -> bool:
        p = urlparse(url)
        base = f"{p.scheme}://{p.netloc}"
        if base not in self._robots:
            rp = urllib.robotparser.RobotFileParser()
            try:
                r = self.session.get(base + "/robots.txt", timeout=15)
                if r.status_code == 200:
                    rp.parse(r.text.splitlines())
                    self._robots[base] = rp
                else:  # no robots.txt (or 4xx) -> no restrictions published
                    self._robots[base] = None
            except requests.RequestException:
                self._robots[base] = None
        rp = self._robots[base]
        return True if rp is None else rp.can_fetch(USER_AGENT, url)

    def get(self, url: str) -> tuple[int, str, bool]:
        """Return (status, body, from_cache). status 0 = network failure, -1 = blocked by robots."""
        key = CACHE / (hashlib.sha256(url.encode()).hexdigest() + ".html")
        if key.exists() and time.time() - key.stat().st_mtime < self.cache_seconds:
            return 200, key.read_text(encoding="utf-8"), True
        if not self._allowed(url):
            return -1, "", False
        host = urlparse(url).netloc
        wait = self.delay - (time.time() - self._last_hit.get(host, 0))
        if wait > 0:
            time.sleep(wait)
        try:
            r = self.session.get(url, timeout=30)
        except requests.RequestException as e:
            return 0, str(e), False
        self._last_hit[host] = time.time()
        if r.status_code == 200:
            key.write_text(r.text, encoding="utf-8")
        return r.status_code, r.text, False


def html_to_text(html: str, base_url: str = "") -> dict:
    """Reduce a guide page to title, update-date hints and readable text (headings, lists, tables)."""
    soup = BeautifulSoup(html, "html.parser")
    links: list[tuple[str, str]] = []
    seen_links: set[str] = set()
    for a in soup.find_all("a", href=True):
        href = urljoin(base_url, a["href"]).split("#")[0]
        if href.startswith("http") and href not in seen_links:
            seen_links.add(href)
            links.append((a.get_text(" ", strip=True)[:120], href))
    for t in soup(["script", "style", "nav", "footer", "header", "aside", "form", "noscript", "svg"]):
        t.decompose()
    title = (soup.title.string or "").strip() if soup.title and soup.title.string else ""
    dates = set()
    for m in soup.find_all("meta"):
        k = (m.get("property") or m.get("name") or "").lower()
        if any(s in k for s in ("modified", "updated", "published", "date")):
            dates.add(f"{k}={m.get('content', '')}")
    for t in soup.find_all("time"):
        dates.add(f"time={t.get('datetime') or t.get_text(strip=True)}")
    lines: list[str] = []
    root = soup.find("main") or soup.find("article") or soup.body or soup
    for el in root.find_all(["h1", "h2", "h3", "h4", "p", "li", "tr"]):
        if el.name == "tr":
            cells = [c.get_text(" ", strip=True) for c in el.find_all(["th", "td"])]
            txt = " | ".join(c for c in cells if c)
        else:
            txt = el.get_text(" ", strip=True)
        if not txt:
            continue
        prefix = {"h1": "# ", "h2": "## ", "h3": "### ", "h4": "#### ", "li": "- "}.get(el.name, "")
        lines.append(prefix + txt)
    # drop consecutive duplicates (nested li/p)
    out = [l for i, l in enumerate(lines) if i == 0 or l != lines[i - 1]]
    return {"title": title, "dates": sorted(dates), "text": "\n".join(out), "links": links}


def looks_like_article(url: str) -> bool:
    segs = [x for x in urlparse(url).path.split("/") if x]
    return bool(segs) and "-" in segs[-1] and len(segs[-1]) > 15 and not re.search(r"/(tag|category|page|author|feed)/", url)


def cmd_pages(args) -> int:
    urls = [u.strip() for u in Path(args.urls).read_text().splitlines() if u.strip() and not u.startswith("#")]
    fetcher = PoliteFetcher(delay=args.delay, cache_hours=args.cache_hours)
    pages_dir = OUT / "pages"
    pages_dir.mkdir(parents=True, exist_ok=True)
    report, done, queue = [], set(), list(urls)
    followed = 0
    follow_hosts = set(args.follow or [])
    while queue:
        url = queue.pop(0)
        if url in done:
            continue
        done.add(url)
        status, body, cached = fetcher.get(url)
        entry = {"url": url, "status": status, "cached": cached}
        if status == 200 and body.lstrip()[:1] in "[{":  # JSON endpoint: keep raw
            name = re.sub(r"[^a-z0-9]+", "-", (urlparse(url).netloc + urlparse(url).path + urlparse(url).query).lower()).strip("-")[:120]
            path = pages_dir / f"{name}.json"
            path.write_text(body, encoding="utf-8")
            entry.update(file=str(path), chars=len(body))
        elif status == 200:
            doc = html_to_text(body, url)
            name = re.sub(r"[^a-z0-9]+", "-", (urlparse(url).netloc + urlparse(url).path).lower()).strip("-")[:120]
            path = pages_dir / f"{name}.md"
            links_md = "\n".join(f"- [{t}]({h})" for t, h in doc["links"][:300])
            path.write_text(
                f"<!-- source: {url} fetched: {datetime.now(timezone.utc).isoformat()} -->\n"
                f"<!-- page dates: {'; '.join(doc['dates']) or 'none found'} -->\n"
                f"# {doc['title']}\n\n{doc['text']}\n\n## LINKS\n{links_md}\n",
                encoding="utf-8",
            )
            entry.update(file=str(path), chars=len(doc["text"]), dates=doc["dates"])
            if urlparse(url).netloc in follow_hosts and url in urls:  # only follow from seed pages
                for _, href in doc["links"]:
                    if (urlparse(href).netloc in follow_hosts and looks_like_article(href)
                            and href not in done and href not in queue and followed < args.max_follow):
                        queue.append(href)
                        followed += 1
        elif status == -1:
            entry["error"] = "disallowed by robots.txt - skipped"
        else:
            entry["error"] = f"HTTP {status}" if status else f"network error: {body[:120]}"
        report.append(entry)
        print(f"[{entry['status']:>3}] {url}  {entry.get('file', entry.get('error', ''))}")
    (OUT / "pages_report.json").write_text(json.dumps(report, indent=2))
    failed = [r for r in report if r["status"] != 200]
    if failed:
        print(f"\n{len(failed)}/{len(report)} pages failed. 403 from a proxy = network policy, not a scraper bug.", file=sys.stderr)
    return 1 if failed and len(failed) == len(report) else 0


# ------------------------------------------------------------------- Blizzard API


class Blizzard:
    def __init__(self, client_id: str, client_secret: str, session=None):
        self.id, self.secret = client_id, client_secret
        self.session = session or requests.Session()
        self.session.headers["User-Agent"] = USER_AGENT
        self._token: str | None = None

    @classmethod
    def from_env(cls) -> "Blizzard":
        load_dotenv(ROOT / ".env")
        cid, sec = os.environ.get("BLIZZARD_CLIENT_ID"), os.environ.get("BLIZZARD_CLIENT_SECRET")
        if not cid or not sec:
            sys.exit("Set BLIZZARD_CLIENT_ID / BLIZZARD_CLIENT_SECRET (see .env.example).")
        return cls(cid, sec)

    def _auth(self) -> str:
        if not self._token:
            r = self.session.post(
                "https://oauth.battle.net/token",
                data={"grant_type": "client_credentials"},
                auth=(self.id, self.secret),
                timeout=30,
            )
            r.raise_for_status()
            self._token = r.json()["access_token"]
        return self._token

    def get(self, path: str, **params) -> dict:
        params.setdefault("locale", LOCALE)
        r = self.session.get(
            f"https://{REGION}.api.blizzard.com{path}",
            params=params,
            headers={"Authorization": f"Bearer {self._auth()}"},
            timeout=120,
        )
        r.raise_for_status()
        return r.json()

    def token_price_gold(self) -> tuple[float, int]:
        d = self.get("/data/wow/token/index", namespace=NAMESPACE_DYNAMIC)
        return d["price"] / COPPER_PER_GOLD, d["last_updated_timestamp"]

    def commodities(self) -> list[dict]:
        return self.get("/data/wow/auctions/commodities", namespace=NAMESPACE_DYNAMIC)["auctions"]

    def find_item_id(self, name: str) -> int | None:
        d = self.get("/data/wow/search/item", namespace=NAMESPACE_STATIC, **{f"name.{LOCALE}": name, "orderby": "id:desc", "_pageSize": 50})
        wanted = name.casefold()
        for res in d.get("results", []):
            data = res["data"]
            if data["name"].get(LOCALE, "").casefold() == wanted:
                return data["id"]
        return None


def load_dotenv(path: Path) -> None:
    if path.exists():
        for line in path.read_text().splitlines():
            if "=" in line and not line.lstrip().startswith("#"):
                k, v = line.split("=", 1)
                os.environ.setdefault(k.strip(), v.strip())


# ------------------------------------------------------------------------ pricing


@dataclass
class PriceStats:
    floor: float  # cheapest unit, gold
    buy_100: float | None  # avg unit price to buy 100 units (walks the order book)
    median: float  # quantity-weighted median
    units: int  # total units listed
    listings: int


def price_stats(auctions: list[dict]) -> PriceStats | None:
    """auctions: [{'quantity': int, 'unit_price': copper}, ...] for ONE item."""
    if not auctions:
        return None
    rows = sorted(((a["unit_price"], a["quantity"]) for a in auctions))
    total = sum(q for _, q in rows)
    half, acc, median = total / 2, 0, rows[0][0]
    for p, q in rows:
        acc += q
        if acc >= half:
            median = p
            break

    def avg_to_buy(n: int) -> float | None:
        if total < n:
            return None
        need, cost = n, 0
        for p, q in rows:
            take = min(q, need)
            cost, need = cost + take * p, need - take
            if need == 0:
                break
        return cost / n / COPPER_PER_GOLD

    return PriceStats(rows[0][0] / COPPER_PER_GOLD, avg_to_buy(100), median / COPPER_PER_GOLD, total, len(rows))


def group_by_item(auctions: list[dict], item_ids: set[int]) -> dict[int, list[dict]]:
    out: dict[int, list[dict]] = {i: [] for i in item_ids}
    for a in auctions:
        iid = a["item"]["id"]
        if iid in out:
            out[iid].append(a)
    return out


def read_lines(path: str) -> list[str]:
    return [l.strip() for l in Path(path).read_text().splitlines() if l.strip() and not l.startswith("#")]


def cmd_token(args) -> int:
    gold, ts = Blizzard.from_env().token_price_gold()
    print(f"EU WoW Token: {gold:,.0f} gold (as of {datetime.fromtimestamp(ts / 1000, timezone.utc):%Y-%m-%d %H:%M} UTC)")
    return 0


def resolve_ids(api: Blizzard, names: list[str]) -> dict[str, int | None]:
    idcache = CACHE / "item_ids.json"
    CACHE.mkdir(exist_ok=True)
    known = json.loads(idcache.read_text()) if idcache.exists() else {}
    for n in names:
        if n not in known or known[n] is None:
            known[n] = api.find_item_id(n)
    idcache.write_text(json.dumps(known, indent=1))
    return {n: known[n] for n in names}


def snapshot(api: Blizzard, names: list[str]) -> dict[str, PriceStats | None]:
    ids = resolve_ids(api, names)
    grouped = group_by_item(api.commodities(), {i for i in ids.values() if i})
    return {n: (price_stats(grouped[i]) if i else None) for n, i in ids.items()}


def cmd_prices(args) -> int:
    names = read_lines(args.watchlist)
    snap = snapshot(Blizzard.from_env(), names)
    OUT.mkdir(exist_ok=True)
    stamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    print(f"EU commodity AH @ {stamp}\n{'item':32} {'floor':>10} {'buy100':>10} {'median':>10} {'units':>10}")
    rec = {"taken_at": stamp, "items": {}}
    for n, s in snap.items():
        if s is None:
            print(f"{n:32} NOT FOUND (not a commodity, or name mismatch)")
            continue
        b = f"{s.buy_100:,.1f}" if s.buy_100 else "n/a"
        print(f"{n:32} {s.floor:>10,.1f} {b:>10} {s.median:>10,.1f} {s.units:>10,}")
        rec["items"][n] = s.__dict__
    with (OUT / "price_history.jsonl").open("a") as f:
        f.write(json.dumps(rec) + "\n")
    return 0


def farm_gold_per_hour(farm: dict, prices: dict[str, PriceStats | None], ah_cut: float, use: str = "buy_100") -> tuple[float, list[str]]:
    total, notes = float(farm.get("direct_gold_per_hour", 0)), []
    for it in farm.get("items", []):
        s = prices.get(it["name"])
        if s is None:
            notes.append(f"no price for {it['name']} (counted as 0)")
            continue
        unit = getattr(s, use) or s.median  # conservative: what a buyer actually pays at depth
        total += it["per_hour"] * unit * (1 - ah_cut)
    return total, notes


def cmd_farms(args) -> int:
    cfg = yaml.safe_load(Path(args.file).read_text())
    names = sorted({i["name"] for f in cfg["farms"] for i in f.get("items", [])})
    prices = snapshot(Blizzard.from_env(), names)
    print(f"{'farm':40} {'gold/hour':>12}  (AH cut {cfg.get('ah_cut', 0.05):.0%}, priced at depth-100 average)")
    for f in cfg["farms"]:
        gph, notes = farm_gold_per_hour(f, prices, cfg.get("ah_cut", 0.05))
        print(f"{f['name']:40} {gph:>12,.0f}")
        for n in notes:
            print(f"    ! {n}")
    return 0


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("pages")
    p.add_argument("--urls", default=str(ROOT / "urls.txt"))
    p.add_argument("--delay", type=float, default=3.0)
    p.add_argument("--cache-hours", type=float, default=12.0)
    p.add_argument("--follow", action="append", help="host whose article links on seed pages are also fetched")
    p.add_argument("--max-follow", type=int, default=15)
    p.set_defaults(fn=cmd_pages)
    sub.add_parser("token").set_defaults(fn=cmd_token)
    p = sub.add_parser("prices")
    p.add_argument("--watchlist", default=str(ROOT / "watchlist.txt"))
    p.set_defaults(fn=cmd_prices)
    p = sub.add_parser("farms")
    p.add_argument("--file", default=str(ROOT / "farms.example.yaml"))
    p.set_defaults(fn=cmd_farms)
    args = ap.parse_args(argv)
    return args.fn(args)


if __name__ == "__main__":
    sys.exit(main())
