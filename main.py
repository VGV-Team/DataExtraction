from regex_extractor import RegExExtractor
from xpath_extractor import XPathExtractor

if __name__ == "__main__":
    # RTVSLO data extraction
    with open("resources/rtvslo.si/Audi A6 50 TDI quattro_ nemir v premijskem razredu - RTVSLO.si.html",
              encoding="UTF-8") as file:
        data = file.read().replace('\r', '').replace('\n', '')
        # result_regex = RegExExtractor.find_information_rtvslo(data)
        result_xpath = XPathExtractor.find_information_rtvslo(data)
        print(result_xpath)

    with open("resources/rtvslo.si/Volvo XC 40 D4 AWD momentum_ suvereno med najboljše v razredu - RTVSLO.si.html",
              encoding="UTF-8") as file:
        data = file.read().replace('\r', '').replace('\n', '')
        # result_regex = RegExExtractor.find_information_rtvslo(data)
        result_xpath = XPathExtractor.find_information_rtvslo(data)
        print(result_xpath)

    # Overstock data extraction
    with open("resources/overstock.com/jewelry01.html") as file:
        data = file.read().replace('\r', '').replace('\n', '')
        result_regex = RegExExtractor.find_information_overstock(data)
        result_xpath = XPathExtractor.find_information_overstock(data)
        print(result_xpath)
        
    with open("resources/overstock.com/jewelry02.html") as file:
        data = file.read().replace('\r', '').replace('\n', '')
        result_regex = RegExExtractor.find_information_overstock(data)
        result_xpath = XPathExtractor.find_information_overstock(data)
        print(result_xpath)
