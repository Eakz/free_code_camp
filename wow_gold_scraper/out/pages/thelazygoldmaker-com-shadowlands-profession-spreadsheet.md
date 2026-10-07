<!-- source: https://thelazygoldmaker.com/shadowlands-profession-spreadsheet fetched: 2026-10-07T20:45:30.434829+00:00 -->
<!-- page dates: article:modified_time=2020-11-14T20:26:25+00:00 -->
# Shadowlands Profession Spreadsheet - The Lazy Goldmaker

I have created a Spreadsheet that automatically calculates profits for the major crafts available in Shadowlands professions.
The Spreadsheet contains all the crafting professions and their recipes.
# Versions
There are two versions of my spreadsheet available depending on your preferences.
One is a downloadable excel file.
The other is a google sheets variant.
The downloadable excel file has some additional features, but it does not work if you are not using Microsoft Office or if you are not on a Windows-based computer.
# Features
The main feature is automated calculation of crafting profits. The pricing data is downloaded from the Tradeskillmaster API.
This gives us access to several TSM based price sources. The default price used in the calculations is 66%dbmarket+34%dbminbuyout. This gives us a weighted average of the market value and the current minimum price that weighs the current price higher than DBmarket does.
You can alter the price source in my spreadsheet. The Excel version supports 4 different price sources (Dbmarket, minbuyout, dbhistorical and dbregionmarket). You can combine two of them to make your own weighted price. In the google sheets version you can currently only choose the weighting between dbmarket and minbuyout.
## Data downloads
The API call is managed a bit different in the two versions. The Excel version uses a simple VBA macro to call the TSM API.
The google sheets version relies on a script that downloads the pricing data.
You can find the source code for the VBA macro here .
# Current Version
The spreadsheet is currently in beta for Shadowlands. Without live data I can’t confirm that everything works, I’ll be updating it to make sure it works as soon as SL is live and we get live data from the TSM API.  Let me know if you see any errors or I’ve missed any recipes!
# Getting the Google Sheet
The link to the google sheets is view only as it needs to remain a master version that only I can edit. To get your own you need to make a copy to your google drive. You do so by clicking file and make a copy. Any edit access requests will be ignored.
# How to set it up
When you open it you should go to the Input worksheet.
You need to add your API key to the white box. The API key is found on your tradeskillmaster account page at tradeskillmaster.com/user. If you do not have a TSM user you will have to register one to utilize the spreadsheet.
The region should be the two-letter abbreviation for your region, US or EU.
The realm name should be written in all lower caps. spaces should be replaced by dashes (-) and special characters should be ignored. Examples:
Emerald Dream = emerald-dream
Mal’Ganis = malganis
After filling in the realm data and the API key you can choose your faction and set the price. For most of you it will be easiest to just use the default price.
Then you click the Get Pricing Data button or the UPDATE button. They are located in the same space to the right of your API key.
## Setting recipe ranks
The sheet contains all the recipe ranks for Shadowlands base legendary items. It cannot currently find the different values of the different levels, as I can’t look at the output from the TSM API to tell how I would split them.
Contact me if you have any questions or need help. I suggest joining me on discord where I can answer your questions and talk to you in a more informal and live manner. You can find it here:
## https://discord.gg/cYKRGxw
### Share this if you like it
- Share on Facebook (Opens in new window) Facebook
- Share on X (Opens in new window) X
- Share on Reddit (Opens in new window) Reddit

## LINKS
- [Home](https://thelazygoldmaker.com)
- [Shadowlands Profession Spreadsheet](https://thelazygoldmaker.com/shadowlands-profession-spreadsheet)
- [Common Issues](https://thelazygoldmaker.com/common-issues)
- [The Repository](https://thelazygoldmaker.com/the-repository)
- [TSM Groups](https://thelazygoldmaker.com/tsm-groups)
- [About me](https://thelazygoldmaker.com/about-2/about)
- [WoW setup](https://thelazygoldmaker.com/about-2/wow-setup)
- [My philosophy](https://thelazygoldmaker.com/my-philosophy)
- [Privacy Policy](https://thelazygoldmaker.com/privacy-policy.html)
- [](https://thelazygoldmaker.com/)
- [](http://www.twitter.com/lazygoldmaker)
- [One is a downloadable excel file.](https://bit.ly/Lazy-SL-Sheet)
- [The other is a google sheets variant.](https://docs.google.com/spreadsheets/d/1kUZogifqblkxXmiT4IgUveraay1xRH-BZsu7su-cpDA/edit?usp=sharing)
- [macro here](http://pastebin.com/eHTyqd24)
- [tradeskillmaster.com/user.](http://tradeskillmaster.com/user)
- [Share on Facebook (Opens in new window) Facebook](https://thelazygoldmaker.com/shadowlands-profession-spreadsheet?share=facebook)
- [Share on X (Opens in new window) X](https://thelazygoldmaker.com/shadowlands-profession-spreadsheet?share=twitter)
- [Share on Reddit (Opens in new window) Reddit](https://thelazygoldmaker.com/shadowlands-profession-spreadsheet?share=reddit)
- [](https://patreon.com/thelazygoldmaker)
- [](https://www.youtube.com/channel/UCo0PzAb5xh6j1PVM4Xe9EOA)
- [](https://www.tradeskillmaster.com/a/lazygold)
- [](http://eepurl.com/czw47b)
- [My Tweets](https://twitter.com/lazygoldmaker)
- [Analyzing the Gold Cap Challenge](https://thelazygoldmaker.com/analyzing-the-gold-cap-challenge)
- [Combined Enchanting and Jewelcrafting spreadsheet](https://thelazygoldmaker.com/combined-enchanting-jewelcrafting-spreadsheet)
- [Luxury mounts: The Mecha-Mogul Mk2](https://thelazygoldmaker.com/luxury-mounts-the-mecha-mogul-mk2)
- [Phase 3 is coming, here’s what you need to know!](https://thelazygoldmaker.com/phase-3-is-coming-heres-what-you-need-to-know)
- [Cooking: the easiest mass crafting setup in 12.1](https://thelazygoldmaker.com/cooking-the-easiest-mass-crafting-setup-in-12-1)
- [HowlThemes](http://www.howlthemes.com)
- [Read more about these purposes](https://cookiedatabase.org/tcf/purposes/)
