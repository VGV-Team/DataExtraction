import re

import utilities


class RegExExtractor:
    @staticmethod
    def find_information_rtvslo(website):
        return {
            "Title": utilities.clean_text(utilities.extract_data(website, "<h1>", "</h1>")),
            "Subtitle": utilities.clean_text(
                utilities.extract_data(website, "<div class=\"subtitle\">", "</div>")),
            "Author": utilities.clean_text(
                utilities.extract_data(website, "<div class=\"author-name\">", "</div>")),
            "PublishedTime": utilities.clean_text(
                utilities.extract_data(website, "<div class=\"publish-meta\">", "<br>")),
            "Lead": utilities.clean_text(utilities.extract_data(website, "<p class=\"lead\">", "</p>")),
            "Content": utilities.clean_text(
                utilities.extract_data(website, "<div class=\"article-body\">", "<div class=\"article-column\">"))
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
            "Title": utilities.clean_text(utilities.extract_data(website, "<span id=\"productTitle\"", "</span>")),
            "Price": utilities.clean_text(
                utilities.extract_data(website, "<span id=\"priceblock_ourprice\"", "</span>")),
            "Stars": utilities.clean_text(utilities.extract_data(website, "<i class=\"a-icon a-icon-star", "</i>")),
            "NumberOfReviews": utilities.clean_text(
                utilities.extract_data(website, "<span id=\"acrCustomerReviewText\"", "</span>")),
            "Description": utilities.clean_text(
                utilities.extract_data(website, "<ul class=\"a-unordered-list a-vertical a-spacing-none\">", "</ul>"))
        }
