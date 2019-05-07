from regex_extractor import RegExExtractor
from xpath_extractor import XPathExtractor
from roadrunner_extractor import RoadRunnerExtractor
import json


if __name__ == "__main__":
    # RTVSLO data extraction
    with open("../resources/rtvslo.si/Audi A6 50 TDI quattro_ nemir v premijskem razredu - RTVSLO.si.html",
              encoding="UTF-8") as file:
        data = file.read().replace('\r', '').replace('\n', '')
        result_regex = RegExExtractor.find_information_rtvslo(data)
        result_xpath = XPathExtractor.find_information_rtvslo(data)
        #print(result_regex)
        print(json.dumps(result_regex))
        print(json.dumps(result_xpath))

    with open("../resources/rtvslo.si/Volvo XC 40 D4 AWD momentum_ suvereno med najboljše v razredu - RTVSLO.si.html",
              encoding="UTF-8") as file:
        data = file.read().replace('\r', '').replace('\n', '')
        result_regex = RegExExtractor.find_information_rtvslo(data)
        result_xpath = XPathExtractor.find_information_rtvslo(data)
        #print(result_regex)
        print(json.dumps(result_regex))
        print(json.dumps(result_xpath))

    # Overstock data extraction
    with open("../resources/overstock.com/jewelry01.html") as file:
        data = file.read().replace('\r', '').replace('\n', '')
        result_regex = RegExExtractor.find_information_overstock(data)
        result_xpath = XPathExtractor.find_information_overstock(data)
        #print(result_regex)
        print(json.dumps(result_regex))
        print(json.dumps(result_xpath))

    with open("../resources/overstock.com/jewelry02.html") as file:
        data = file.read().replace('\r', '').replace('\n', '')
        result_regex = RegExExtractor.find_information_overstock(data)
        result_xpath = XPathExtractor.find_information_overstock(data)
        #print(result_regex)
        print(json.dumps(result_regex))
        print(json.dumps(result_xpath))

    # Amazon data extraction
    with open("../resources/amazon.co.uk/EMPIRE Merchandising 669490 Your Empire Needs You Star Wars, Vader, Science "
              "Fiction Sci Fi, Film Poster 61 x 91.5 cm_ Amazon.co.uk_ Amazon.co.uk_.html", encoding="UTF-8") as file:
        data = file.read().replace('\r', '').replace('\n', '')
        result_regex = RegExExtractor.find_information_amazon(data)
        result_xpath = XPathExtractor.find_information_amazon(data)
        #print(result_regex)
        print(json.dumps(result_regex))
        print(json.dumps(result_xpath))

    with open("../resources/amazon.co.uk/Vintage Anti-Capitalist PYRAMID OF THE CAPITALIST SYSTEM c1911 250gsm Gloss Art "
              "Card Reproduction Poster_ Amazon.co.uk_ Amazon.co.uk_.html", encoding="UTF-8") as file:
        data = file.read().replace('\r', '').replace('\n', '')
        result_regex = RegExExtractor.find_information_amazon(data)
        result_xpath = XPathExtractor.find_information_amazon(data)
        #print(result_regex)
        print(json.dumps(result_regex))
        print(json.dumps(result_xpath))

    # Roadrunner
    with open("../resources/rtvslo.si/Audi A6 50 TDI quattro_ nemir v premijskem razredu - RTVSLO.si.html",
              encoding="UTF-8") as file1, open("../resources/rtvslo.si/Volvo XC 40 D4 AWD momentum_ suvereno med najboljše"
                                               " v razredu - RTVSLO.si.html", encoding="UTF-8") as file2:
        data1 = file1.read().replace('\r', '').replace('\n', '')
        data2 = file2.read().replace('\r', '').replace('\n', '')
        print(RoadRunnerExtractor.generate_wrapper(data1, data2))

    with open("../resources/overstock.com/jewelry01.html") as file1, open("../resources/overstock.com/jewelry02.html") as \
            file2:
        data1 = file1.read().replace('\r', '').replace('\n', '')
        data2 = file2.read().replace('\r', '').replace('\n', '')
        print(RoadRunnerExtractor.generate_wrapper(data1, data2))

    with open("../resources/amazon.co.uk/EMPIRE Merchandising 669490 Your Empire Needs You Star Wars, Vader, Science "
              "Fiction Sci Fi, Film Poster 61 x 91.5 cm_ Amazon.co.uk_ Amazon.co.uk_.html", encoding="UTF-8") as file1,\
            open("../resources/amazon.co.uk/Vintage Anti-Capitalist PYRAMID OF THE CAPITALIST SYSTEM c1911 250gsm Gloss Art "
             "Card Reproduction Poster_ Amazon.co.uk_ Amazon.co.uk_.html", encoding="UTF-8") as file2:
        data1 = file1.read().replace('\r', '').replace('\n', '')
        data2 = file2.read().replace('\r', '').replace('\n', '')
        print(RoadRunnerExtractor.generate_wrapper(data1, data2))
