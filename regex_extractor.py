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
        current_row = 0
        table_start = website[utilities.find_string(website,
                                                    "<table border=\"0\" cellpadding=\"2\" "
                                                    "cellspacing=\"0\" width=\"100%\">"):]

        while True:
            if current_row % 2 == 0:
                index = utilities.find_string(table_start, "<tr bgcolor=\"#ffffff\">")
            else:
                index = utilities.find_string(table_start, "<tr bgcolor=\"#dddddd\">")
            if index is None:
                break

            row_start = table_start[index:]

            # start from data table
            column_start = row_start[utilities.find_string(row_start, "<td valign=\"top\">"):]

            title = utilities.clean_text(utilities.extract_data(column_start, "<b>", "</b>"))

            # start from left part of data table
            data_start = column_start[utilities.find_string(column_start, "<table>"):]
            left_column = data_start[utilities.find_string(data_start, "<td valign=\"top\">"):]

            # 1st row with listed price information
            next_tr = left_column[utilities.find_string(left_column, "<tr>"):]
            list_price_row = utilities.extract_data(next_tr, "<tr>", "</tr>")
            list_price = utilities.clean_text(
                utilities.extract_data(list_price_row, "<td align=\"left\" nowrap=\"nowrap\">", "</td>"))

            # 2nd row with current price information - +1 is for starting from next <tr>
            next_tr = next_tr[1 + utilities.find_string(next_tr[1:], "<tr>"):]
            price_row = utilities.extract_data(next_tr, "<tr>", "</tr>")
            price = utilities.clean_text(
                utilities.extract_data(price_row, "<td align=\"left\" nowrap=\"nowrap\">", "</td>"))

            # 3rd row with savings information - +1 is for starting from next <tr>
            next_tr = next_tr[1 + utilities.find_string(next_tr[1:], "<tr>"):]
            saving_row = utilities.extract_data(next_tr, "<tr>", "</tr>")
            saving_value = utilities.extract_data(saving_row, "<td align=\"left\" nowrap=\"nowrap\">", "</td>")
            saving = utilities.clean_text(utilities.extract_data(saving_value, "$", " "))
            saving_percent = utilities.clean_text(
                utilities.extract_data(saving_value, "(", ")")).replace("(", "").replace(")", "")

            # start from right part of data table
            content = utilities.clean_text(utilities.extract_data(next_tr, "<td valign=\"top\">", "</tr>"))

            current_row = current_row + 1
            table_start = next_tr

            results.append(
                {
                    "Title": title,
                    "ListPrice": list_price,
                    "Price": price,
                    "Saving": saving,
                    "SavingPercent": saving_percent,
                    "Content": content
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
