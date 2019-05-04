from regex_extractor import RegExExtractor
from xpath_extractor import XPathExtractor

if __name__ == "__main__":
    # RTVSLO data extraction
    with open("resources/rtvslo.si/Audi A6 50 TDI quattro_ nemir v premijskem razredu - RTVSLO.si.html",
              encoding="UTF-8") as file:
        data = file.read().replace('\r', '').replace('\n', '')
        result_regex = RegExExtractor.find_information_rtvslo(data)
        result_xpath = XPathExtractor.find_information_rtvslo(data)
        print(result_regex)

    with open("resources/rtvslo.si/Volvo XC 40 D4 AWD momentum_ suvereno med najboljše v razredu - RTVSLO.si.html",
              encoding="UTF-8") as file:
        data = file.read().replace('\r', '').replace('\n', '')
        result_regex = RegExExtractor.find_information_rtvslo(data)
        result_xpath = XPathExtractor.find_information_rtvslo(data)
        print(result_regex)

    # Overstock data extraction
    with open("resources/overstock.com/jewelry01.html") as file:
        data = file.read().replace('\r', '').replace('\n', '')
        result_regex = RegExExtractor.find_information_overstock(data)
        result_xpath = XPathExtractor.find_information_overstock(data)
        print(result_regex)

    with open("resources/overstock.com/jewelry02.html") as file:
        data = file.read().replace('\r', '').replace('\n', '')
        result_regex = RegExExtractor.find_information_overstock(data)
        result_xpath = XPathExtractor.find_information_overstock(data)
        print(result_regex)

    # Amazon data extraction
    with open("resources/amazon.co.uk/EMPIRE Merchandising 669490 Your Empire Needs You Star Wars, Vader, Science "
              "Fiction Sci Fi, Film Poster 61 x 91.5 cm_ Amazon.co.uk_ Amazon.co.uk_.html", encoding="UTF-8") as file:
        data = file.read().replace('\r', '').replace('\n', '')
        result_regex = RegExExtractor.find_information_amazon(data)
        result_xpath = XPathExtractor.find_information_amazon(data)
        print(result_regex)

    with open("resources/amazon.co.uk/Vintage Anti-Capitalist PYRAMID OF THE CAPITALIST SYSTEM c1911 250gsm Gloss Art "
              "Card Reproduction Poster_ Amazon.co.uk_ Amazon.co.uk_.html", encoding="UTF-8") as file:
        data = file.read().replace('\r', '').replace('\n', '')
        result_regex = RegExExtractor.find_information_amazon(data)
        result_xpath = XPathExtractor.find_information_amazon(data)
        print(result_regex)
