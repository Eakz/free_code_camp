# wow_gold_scraper

Evidence-first WoW gold research (Retail, EU). Run it where the network is open (your machine, or an environment that allows the hosts).

```
pip install -r requirements.txt
cp .env.example .env        # add free Blizzard API client id/secret: https://develop.battle.net/access/clients
python wowgold.py token                 # live EU WoW Token price
python wowgold.py pages                 # guide pages in urls.txt -> out/pages/*.md (robots.txt respected)
python wowgold.py prices                # live EU commodity prices for watchlist.txt -> out/price_history.jsonl
python wowgold.py farms --file my.yaml  # gold/hour from live prices (see farms.example.yaml)
python -m pytest tests                  # offline tests
```

Method: guide pages say *what* to farm and how many items per hour; the gold/hour is then computed from live
Blizzard prices (priced at order-book depth of 100 units, minus the 5% AH cut), never copied from a guide.
It does not bypass blocks: a 403/robots refusal is reported and skipped.
