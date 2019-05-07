import re

import utilities


class RegExExtractor:
    @staticmethod
    def find_information_rtvslo(website):
        return {
            "Title": utilities.clean_text(re.findall(r"<h1>.+?</h1>", website)[0]),
            "Subtitle": utilities.clean_text(re.findall(r"<div class=\"subtitle\">.+?</div>", website)[0]),
            "Author": utilities.clean_text(re.findall(r"<div class=\"author-name\">.+?</div>", website)[0]),
            "PublishedTime": utilities.clean_text(re.findall(r"<div class=\"publish-meta\">.+?<br>", website)[0]),
            "Lead": utilities.clean_text(re.findall(r"<p class=\"lead\">.+?</p>", website)[0]),
            "Content": utilities.clean_text(re.findall(r"<div class=\"article-body\">.+?<div class=\"article-column\">", website)[0])
        }

    @staticmethod
    def find_information_overstock(website):
        results = []

        titles = re.findall(r"<td valign=\"top\">\s*<a href=\"[^\"]+\">\s*<b>[^<]+", website)
        list_prices = re.findall(r"<s>\$[^<]+</s>", website)
        prices = re.findall(r"<b>\$[^<]+</b>", website)
        savings = re.findall(r"<span class=\"littleorange\">\$[^(]+", website)
        savings_percent = re.findall(r"\([0-9]*%\)", website)
        contents = re.findall("<span class=\"normal\">[^<]+<br>", website)

        for i in range(len(titles)):
            results.append(
                {
                    "Title": utilities.clean_text(titles[i]),
                    "ListPrice": utilities.clean_text(list_prices[i]),
                    "Price": utilities.clean_text(prices[i]),
                    "Saving": utilities.clean_text(savings[i]),
                    "SavingPercent": utilities.clean_text(savings_percent[i]).replace("(", "").replace(")", ""),
                    "Content": utilities.clean_text(contents[i])
                })
        return results

    @staticmethod
    def find_information_amazon(website):
        return {
            "Title": utilities.clean_text(re.findall(r"<span id=\"productTitle\".+?</span>", website)[0]),
            "Price": utilities.clean_text(re.findall(r"<span id=\"priceblock_ourprice\".+?</span>", website)[0]),
            "Stars": utilities.clean_text(re.findall(r"<i class=\"a-icon a-icon-star.+?</i>", website)[0]),
            "NumberOfReviews": utilities.clean_text(re.findall(r"<span id=\"acrCustomerReviewText\".+?</span>", website)[0]),
            "Description": utilities.clean_text(
                re.findall(r"<ul class=\"a-unordered-list a-vertical a-spacing-none\">.+?</ul>", website)[0])
        }
