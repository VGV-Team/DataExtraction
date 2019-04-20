from lxml.html.soupparser import fromstring

import utilities


class XPathExtractor:
    @staticmethod
    def find_information_rtvslo(website):
        tree = fromstring(website)
        return {
            "Title": tree.xpath("//h1/text()"),
            "Subtitle": tree.xpath("//div[@class='subtitle']/text()"),
            "Author": tree.xpath("//div[@class='author-name']/text()"),
            "PublishedTime": utilities.clean_text(tree.xpath("//div[@class='publish-meta']/text()")[0]),
            "Lead": tree.xpath("//p[@class='lead']/text()"),
            "Content": utilities.clean_text(
                (" ".join(tree.xpath("//div[@class='article-body']//*[not(name()='script')]/text()"))))
        }

    @staticmethod
    def find_information_overstock(website):
        tree = fromstring(website)
        results = []

        titles = tree.xpath("//td[@valign='top']/a/b//text()")
        price_parts = tree.xpath("//tr/td[@align='left' and @nowrap='nowrap']//text()")
        list_prices = price_parts[0::3]
        prices = price_parts[1::3]
        savings = price_parts[2::3]
        contents = tree.xpath("//td[@valign='top']/span[@class='normal']/text()")

        for i in range(len(titles)):
            results.append(
                {
                    "Title": titles[i],
                    "ListPrice": list_prices[i],
                    "Price": prices[i],
                    "Saving": utilities.clean_text(utilities.extract_data(savings[i], "$", " ")),
                    "SavingPercent": utilities.clean_text(
                        utilities.extract_data(savings[i], "(", ")")).replace("(", "").replace(")", ""),
                    "Content": contents[i]
                })
        return results
