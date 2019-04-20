from lxml.html.soupparser import fromstring

import utilities


class XPathExtractor:
    @staticmethod
    def find_information_rtvslo(website):
        tree = fromstring(website)
        return {
            "Title": tree.xpath("//h1/text()")[0],
            "Subtitle": tree.xpath("//div[@class='subtitle']/text()")[0],
            "Author": tree.xpath("//div[@class='author-name']/text()")[0],
            "PublishedTime": utilities.clean_text(tree.xpath("//div[@class='publish-meta']/text()")[0])[0],
            "Lead": tree.xpath("//p[@class='lead']/text()")[0],
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

    @staticmethod
    def find_information_amazon(website):
        tree = fromstring(website)
        return {
            "Title": utilities.clean_text(tree.xpath("//span[@id='productTitle']/text()")[0]),
            "Price": tree.xpath("//span[@id='priceblock_ourprice']/text()")[0],
            "Stars": tree.xpath("//a[@class='a-popover-trigger a-declarative']/i/span/text()")[0],
            "NumberOfReviews": tree.xpath("//span[@id='acrCustomerReviewText']/text()")[0],
            "Description": utilities.clean_text(
                "||".join(tree.xpath("//ul[@class='a-unordered-list a-vertical a-spacing-none']//span/text()")))
        }
