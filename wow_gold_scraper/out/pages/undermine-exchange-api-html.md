<!-- source: https://undermine.exchange/api.html fetched: 2026-10-07T20:49:41.299312+00:00 -->
<!-- page dates: none found -->
# Undermine Exchange API

# Undermine Exchange API
## Welcome
### What's in the API?
- Current region-wide minimum/median prices and total quantities for all items and battle pets
- Current prices and quantities for individual items and battle pets for all realms in a region
- 14-day hourly resolution price/quantity history for individual items/pets on each realm
- Daily resolution price/quantity history for individual items/pets on each region/realm
- Item-level-specific and pet-breed-specific pricing data
### Additional Resources
Before we get started, please check out Blizzard's Community API . It's available to everyone, and is the source of the auction house snapshot data that powers Undermine Exchange. Use those resources first where you can.
Also check out the TSM Public Web API , which is another excellent pricing API resource.
Finally, if you're inclined to assemble this data yourself, you can find the data collection code for this API and Undermine Exchange as a whole at Project Shatari on Github .
## Limitations
### Rate Limits
To manage our resource usage, the API enforces a rate limit for each API consumer. Each request costs a number of points, and you're provided a sliding window of 3,000 points per hour. If you exceed that points budget, your request will not be serviced, and you'll need to wait for enough points to replenish before your request will return a result.
Each API endpoint described below will include points cost information. Many endpoints will include 2 costs: a lower cost for gzip-compressed responses (preferred), and a higher cost for uncompressed responses.
### Patron Access Limits
Many endpoints are available to the public without any Patreon membership requirements. However, some endpoints do require paid membership to our Patreon campaign, specifically those which mirror functionality where the Undermine Exchange website also requires paid access. All endpoints listed below will state whether they require Free or Paid access.
There are no differences in rate limits between free and paid accounts at this time.
Basically, if it requires a paid account to view on the site, it requires that same paid account to access it via the API. There are no additional costs for API access versus website access: the same tier of support provides access to both.
### Item and Pet Metadata
## Gaining Access
Send HTTP GET requests to https://api.undermine.exchange/ at the paths listed below.
All requests to the API must include your API key. This key is tied to your Patreon account, since Patreon is our user account provider.
Note: Most API calls are free to the public , where you do not need a paid Patreon membership. You don't even need to be a member of our Patreon campaign at all, you just need to log in to our site via Patreon.
### Your API Key
### Using Your Key
### GZip Compression and Quota
## API Paths and URLs
- :region - One of us , eu , tw , kr
- :realm - A realm slug, such as medivh
- :itemId - An item ID, such as 118852
- :itemLevel - An item level, such as 266
- :itemSuffix - An item suffix ID, such as 13157
- :petSpecies - A pet species ID, such as 145
- :petBreed - A pet breed ID, such as 6
## Static Data
#### Realm List
Path | /v1/static/realms.json
Points | 1 point (3 uncompressed)
Access | Free ✅️
#### Suffix List
Path | /v1/static/suffixes.json
Points | 1 point
Access | Free ✅️
## Region Data
### Items
#### Base Item Summary
Path | /v1/region/:region/items.json
Points | 3 points (5 uncompressed)
Access | Free ✅️
A list of every (non-commodity) item for sale in that region, with the median and minimum price (in copper), and how many unique realms are selling it. By "unique realms" we essentially mean connected realms, so if one auction house covers 4 in-game realms, we consider that one "realm" in this count.
The item must be on sale on at least 1 realm to appear in this list. If it's not for sale anywhere, it's not here.
This endpoint does not include separate item level or item suffix pricing, it's only by item ID.
#### Full Item Summary
Path | /v1/region/:region/items.json?detail=full
Points | 3 points (5 uncompressed)
Access | Paid ✅️ ⛔ Become a patron! ⚠️
This includes all the same data as the Base Item Summary, but adds item level pricing as well. Same caveat applies for availability: an item must currently be on sale somewhere in the region to appear in this list, otherwise it's not included.
Also, the "min" and "realms" data is only included for level/suffix variations when that item is from the current expansion.
#### Now Item Detail
Path | /v1/region/:region/items/:itemId/now.json
Points | 3 points (5 uncompressed)
Access | Free ✅️
#### Now Item Level Detail
Path | /v1/region/:region/items/:itemId/:itemLevel/now.json
Points | 3 points (5 uncompressed)
Access | Paid ✅️ ⛔ Become a patron! ⚠️
#### Now Item Suffix Detail
Path | /v1/region/:region/items/:itemId/:itemLevel/:itemSuffix/now.json
Points | 3 points (5 uncompressed)
Access | Paid ✅️ ⛔ Become a patron! ⚠️
#### Daily Item Detail
Path | /v1/region/:region/items/:itemId/daily.json
Points | 5 points (9 uncompressed)
Access | Free ✅️
For each item on each realm, once per day, we find the snapshot in that day with the highest total quantity, and store that quantity and the price at that time.
This endpoint then looks at all the data for that item, summing up the total quantity per day, and averaging (mean) the daily prices, across all the realms in the region. This gives you "total quantity" and "average price" values for that item for each day across the region.
#### Daily Item Level Detail
Path | /v1/region/:region/items/:itemId/:itemLevel/daily.json
Points | 5 points (9 uncompressed)
Access | Paid ✅️ ⛔ Become a patron! ⚠️
#### Daily Item Suffix Detail
Path | /v1/region/:region/items/:itemId/:itemLevel/:itemSuffix/daily.json
Points | 5 points (9 uncompressed)
Access | Paid ✅️ ⛔ Become a patron! ⚠️
### Commodities
#### Base Commodity Summary
Path | /v1/region/:region/commodities.json
Points | 3 point (5 uncompressed)
Access | Free ✅️
This is the latest snapshot of the commodities pricing for that region. The result includes two timestamps: "snapshot" is Blizzard's timestamp when they assembled the data. "lastUpdated" is when Undermine Exchange generated this file. It will typically be a few minutes after "snapshot."
- "snapshot" is Blizzard's timestamp when they assembled the data.
- "lastUpdated" is when Undermine Exchange generated this file. It will typically be a few minutes after "snapshot."
The item list includes items which aren't currently for sale (showing quantity=0), and adds a "seen" timestamp to those records, indicating when that item was last seen for sale.
#### Full Commodity Summary
Path | /v1/region/:region/commodities.json?detail=full
Points | 3 point (5 uncompressed)
Access | Paid ✅️ ⛔ Become a patron! ⚠️
#### Now Commodity Detail
Path | /v1/region/:region/commodities/:itemId/now.json
Points | 1 point
Access | Free ✅️
- "lastSeen" is Blizzard's snapshot timestamp when we last had a nonzero quantity.
- "lastUpdated" is when Undermine Exchange generated this file. It will typically be a few minutes after "lastSeen" (quantity > 0) or an hour after "lastSeen" (quantity = 0). It may also be a date significantly in the past when quantity = 0, this is normal.
#### Now Commodity Level Detail
Path | /v1/region/:region/commodities/:itemId/:itemLevel/now.json
Points | 1 point
Access | Paid ✅️ ⛔ Become a patron! ⚠️
Same as Now Commodity Detail, but for a specific commodity item + level. As mentioned in the Full Commodity Summary, this is very rarely useful, but is here for the sake of completion.
The individual auction rows only have "price", since they're always quantity=1, being treated like non-stackable items. If they had bonuses or modifiers, they would also appear there. Best just to pretend this endpoint doesn't exist, bonuses make no sense on stackable items...
#### Hourly Commodity Detail
Path | /v1/region/:region/commodities/:itemId/hourly.json
Points | 3 points (5 uncompressed)
Access | Free ✅️
The price and quantity of this commodity item in this region at each Blizzard snapshot, for the past 14 days or so. The snapshot timestamps come straight from Blizzard. When quantity becomes zero, we carry the price from the previous snapshot. Snapshots are roughly hourly, but it's not guaranteed (especially during Blizzard's weekly scheduled downtime).
#### Hourly Commodity Level Detail
Path | /v1/region/:region/commodities/:itemId/:itemLevel/hourly.json
Points | 3 points (5 uncompressed)
Access | Paid ✅️ ⛔ Become a patron! ⚠️
Same as the Hourly Commodity Detail, but for a specific commodity item + level. Which we've already described as very unusual and best ignored.
#### Daily Commodity Detail
Path | /v1/region/:region/commodities/:itemId/daily.json
Points | 3 points (5 uncompressed)
Access | Free ✅️
The maximum quantity, and the price at that time, of the commodity item in that region for each day we've seen it. Ever.
#### Daily Commodity Level Detail
Path | /v1/region/:region/commodities/:itemId/:itemLevel/daily.json
Points | 3 points (5 uncompressed)
Access | Paid ✅️ ⛔ Become a patron! ⚠️
Same as Daily Commodity Detail, but for a specific commodity item + level. What are we even doing here.
### Battle Pets
#### Base Pet Summary
Path | /v1/region/:region/pets.json
Points | 1 point (3 uncompressed)
Access | Free ✅️
A list of every battle pet for sale in that region, with the median and minimum price (in copper), and how many unique realms are selling it. By "unique realms" we essentially mean connected realms, so if one auction house covers 4 in-game realms, we consider that one "realm" in this count.
The pet must be on sale on at least 1 realm to appear in this list. If it's not for sale anywhere, it's not here.
This endpoint does not include separate breed pricing, it's only by species ID.
#### Full Pet Summary
Path | /v1/region/:region/pets.json?detail=full
Points | 1 point (3 uncompressed)
Access | Paid ✅️ ⛔ Become a patron! ⚠️
This includes all the same data as the Base Pet Summary, but adds breed pricing as well. Same caveat applies for availability: a pet must currently be on sale somewhere in the region to appear in this list, otherwise it's not included.
#### Now Pet Detail
Path | /v1/region/:region/pets/:petSpecies/now.json
Points | 3 points (5 uncompressed)
Access | Free ✅️
#### Now Pet Breed Detail
Path | /v1/region/:region/pets/:petSpecies/:petBreed/now.json
Points | 3 points (5 uncompressed)
Access | Paid ✅️ ⛔ Become a patron! ⚠️
#### Daily Pet Detail
Path | /v1/region/:region/pets/:petSpecies/daily.json
Points | 5 points (9 uncompressed)
Access | Free ✅️
For each pet on each realm, once per day, we find the snapshot in that day with the highest total quantity, and store that quantity and the price at that time.
This endpoint then looks at all the data for that pet, summing up the total quantity per day, and averaging (mean) the daily prices, across all the realms in the region. This gives you "total quantity" and "average price" values for that pet for each day across the region.
#### Daily Pet Breed Detail
Path | /v1/region/:region/pets/:petSpecies/:petBreed/daily.json
Points | 5 points (9 uncompressed)
Access | Paid ✅️ ⛔ Become a patron! ⚠️
## Realm Data
These endpoints cover a specific realm, instead of the entire region.
Connected realms share an auction house, but you can use any realm in that set to obtain the information. You don't need to know which realms are connected to which other realms. However, in responses, you may see a list of realms together, and that list helps you identify the realms that are connected to each-other.
### Items
#### Base Item Summary
Path | /v1/realm/:region/:realm/items.json
Points | 3 points (7 uncompressed)
Access | Free ✅️
This is the latest snapshot of the non-commodity item pricing for that realm. The result includes two timestamps: "snapshot" is Blizzard's timestamp when they assembled the latest data. "lastUpdated" is when Undermine Exchange generated this file. It will typically be a few minutes after "snapshot."
- "snapshot" is Blizzard's timestamp when they assembled the latest data.
- "lastUpdated" is when Undermine Exchange generated this file. It will typically be a few minutes after "snapshot."
The item list includes items which aren't currently for sale (showing quantity=0), and adds a "seen" timestamp to those records, indicating when that item was last seen for sale.
This endpoint does not include separate item level or item suffix pricing, it's only by item ID.
#### Full Item Summary
Path | /v1/realm/:region/:realm/items.json?detail=full
Points | 3 points (7 uncompressed)
Access | Paid ✅️ ⛔ Become a patron! ⚠️
This contains all the same data as the Base Item Summary, but also includes item level and suffix details for equippable items.
#### Tertiary Stats
Path | /v1/realm/:region/:realm/stats.json
Points | 1 point (3 uncompressed)
Access | Paid ✅️ ⛔ Become a patron! ⚠️
This provides item keys where certain tertiary stats are currently for sale. For example, under the "speed" list, you might find item 169406, level 45, suffix 13152. In that case, there is some auction currently posted for that item + level + suffix combo which has the speed tertiary stat bonus. You can then look that item up via the Now Item Suffix Detail realm endpoint to get pricing and auction data.
#### Now Item Detail
Path | /v1/realm/:region/:realm/items/:itemId/now.json
Points | 1 point
Access | Free ✅️
- "lastSeen" is Blizzard's snapshot timestamp when we last had a nonzero quantity.
- "lastUpdated" is when Undermine Exchange generated this file. It will typically be a few minutes after "lastSeen" (quantity > 0) or an hour after "lastSeen" (quantity = 0). It may also be a date significantly in the past when quantity = 0, this is normal.
#### Now Item Level Detail
Path | /v1/realm/:region/:realm/items/:itemId/:itemLevel/now.json
Points | 1 point
Access | Paid ✅️ ⛔ Become a patron! ⚠️
Same as Now Item Detail, but for a specific non-commodity item + level.
The auction list has a separate entry for each individual item (instead of grouping by price), and also includes item modifiers, bonuses, tertiary stats, and sockets, when present.
Item socket IDs can be mapped via the ItemSocketType in-game enum. See ItemConstantsDocumentation.lua.
#### Now Item Suffix Detail
Path | /v1/realm/:region/:realm/items/:itemId/:itemLevel/:itemSuffix/now.json
Points | 1 point
Access | Paid ✅️ ⛔ Become a patron! ⚠️
Same as Now Item Level Detail, but for a specific non-commodity item + level + suffix.
#### Hourly Item Detail
Path | /v1/realm/:region/:realm/items/:itemId/hourly.json
Points | 3 points (5 uncompressed)
Access | Free ✅️
The price and quantity of this non-commodity item on this realm at each Blizzard snapshot, for the past 14 days or so. The snapshot timestamps come straight from Blizzard. When quantity becomes zero, we carry the price from the previous snapshot. Snapshots are roughly hourly, but it's not guaranteed (especially during Blizzard's weekly scheduled downtime).
#### Hourly Item Level Detail
Path | /v1/realm/:region/:realm/items/:itemId/:itemLevel/hourly.json
Points | 3 points (5 uncompressed)
Access | Paid ✅️ ⛔ Become a patron! ⚠️
Same as Hourly Item Detail, but for a specific non-commodity item + level.
#### Hourly Item Suffix Detail
Path | /v1/realm/:region/:realm/items/:itemId/:itemLevel/:itemSuffix/hourly.json
Points | 3 points (5 uncompressed)
Access | Paid ✅️ ⛔ Become a patron! ⚠️
Same as Hourly Item Detail, but for a specific non-commodity item + level + suffix.
#### Daily Item Detail
Path | /v1/realm/:region/:realm/items/:itemId/daily.json
Points | 3 points (5 uncompressed)
Access | Free ✅️
The maximum quantity, and the price at that time, of the non-commodity item on that realm for each day we've seen it. Ever.
#### Daily Item Level Detail
Path | /v1/realm/:region/:realm/items/:itemId/:itemLevel/daily.json
Points | 3 points (5 uncompressed)
Access | Paid ✅️ ⛔ Become a patron! ⚠️
Same as Daily Item Detail, but for a specific non-commodity item + level.
#### Daily Item Suffix Detail
Path | /v1/realm/:region/:realm/items/:itemId/:itemLevel/:itemSuffix/daily.json
Points | 3 points (5 uncompressed)
Access | Paid ✅️ ⛔ Become a patron! ⚠️
Same as Daily Item Detail, but for a specific non-commodity item + level + suffix.
### Battle Pets
#### Base Pet Summary
Path | /v1/realm/:region/:realm/pets.json
Points | 1 points (3 uncompressed)
Access | Free ✅️
This is the latest snapshot of the battle pet pricing for that realm. The result includes two timestamps: "snapshot" is Blizzard's timestamp when they assembled the latest data. "lastUpdated" is when Undermine Exchange generated this file. It will typically be a few minutes after "snapshot."
- "snapshot" is Blizzard's timestamp when they assembled the latest data.
- "lastUpdated" is when Undermine Exchange generated this file. It will typically be a few minutes after "snapshot."
The pet list includes pets which aren't currently for sale (showing quantity=0), and adds a "seen" timestamp to those records, indicating when that pet was last seen for sale.
This endpoint does not include separate breed pricing, it's only by species ID.
#### Full Pet Summary
Path | /v1/realm/:region/:realm/pets.json?detail=full
Points | 1 points (3 uncompressed)
Access | Paid ✅️ ⛔ Become a patron! ⚠️
This contains all the same data as the Base Pet Summary, but also includes breed pricing details.
#### Now Pet Detail
Path | /v1/realm/:region/:realm/pets/:petSpecies/now.json
Points | 1 point
Access | Free ✅️
- "lastSeen" is Blizzard's snapshot timestamp when we last had a nonzero quantity.
- "lastUpdated" is when Undermine Exchange generated this file. It will typically be a few minutes after "lastSeen" (quantity > 0) or an hour after "lastSeen" (quantity = 0). It may also be a date significantly in the past when quantity = 0, this is normal.
#### Now Pet Breed Detail
Path | /v1/realm/:region/:realm/pets/:petSpecies/:petBreed/now.json
Points | 1 point
Access | Paid ✅️ ⛔ Become a patron! ⚠️
Same as Now Pet Detail, but for a specific species + breed.
The auction list has a separate entry for each individual pet (instead of grouping by price), and also includes item modifiers, when present.
#### Hourly Pet Detail
Path | /v1/realm/:region/:realm/pets/:petSpecies/hourly.json
Points | 3 points (5 uncompressed)
Access | Free ✅️
The price and quantity of this pet on this realm at each Blizzard snapshot, for the past 14 days or so. The snapshot timestamps come straight from Blizzard. When quantity becomes zero, we carry the price from the previous snapshot. Snapshots are roughly hourly, but it's not guaranteed (especially during Blizzard's weekly scheduled downtime).
#### Hourly Pet Breed Detail
Path | /v1/realm/:region/:realm/pets/:petSpecies/:petBreed/hourly.json
Points | 3 points (5 uncompressed)
Access | Paid ✅️ ⛔ Become a patron! ⚠️
Same as Hourly Pet Detail, but for a specific pet species + breed.
#### Daily Pet Detail
Path | /v1/realm/:region/:realm/pets/:petSpecies/daily.json
Points | 3 points (5 uncompressed)
Access | Free ✅️
The maximum quantity, and the price at that time, of the pet on that realm for each day we've seen it. Ever.
#### Daily Pet Breed Detail
Path | /v1/realm/:region/:realm/pets/:petSpecies/:petBreed/daily.json
Points | 3 points (5 uncompressed)
Access | Paid ✅️ ⛔ Become a patron! ⚠️
Same as Daily Pet Detail, but for a specific pet species + breed.
## Support
This service is provided on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied, including, without limitation, any warranties or conditions of TITLE, NON-INFRINGEMENT, MERCHANTABILITY, or FITNESS FOR A PARTICULAR PURPOSE. If something is broken, or wrong, or slow, or late, you can let us know, but there are no guarantees things will get fixed, nor are there any assurances of correct and timely data.
If you have any questions about the API, please reach us at the feedback email listed on our website .

## LINKS
- [Undermine Exchange](https://undermine.exchange/)
- [Blizzard's Community API](https://community.developer.battle.net/documentation/world-of-warcraft)
- [TSM Public Web API](https://support.tradeskillmaster.com/en_US/api-documentation/tsm-public-web-api)
- [Project Shatari on Github](https://github.com/erorus/shatari)
- [Become a patron!](https://www.patreon.com/erorus/membership)
