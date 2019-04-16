from regex_extractor import RegExExtractor

if __name__ == "__main__":
    # RTVSLO data extraction
    with open("resources/rtvslo.si/Audi A6 50 TDI quattro_ nemir v premijskem razredu - RTVSLO.si.html",
              encoding="UTF-8") as file:
        data = file.read().replace('\r', '').replace('\n', '')
        result = RegExExtractor.find_information_rtvslo(data)
        print(result)
    with open("resources/rtvslo.si/Volvo XC 40 D4 AWD momentum_ suvereno med najboljše v razredu - RTVSLO.si.html",
              encoding="UTF-8") as file:
        data = file.read().replace('\r', '').replace('\n', '')
        result = RegExExtractor.find_information_rtvslo(data)

    # Overstock data extraction
    with open("resources/overstock.com/jewelry01.html") as file:
        data = file.read().replace('\r', '').replace('\n', '')
        result = RegExExtractor.find_information_overstock(data)
        print(result)
    with open("resources/overstock.com/jewelry02.html") as file:
        data = file.read().replace('\r', '').replace('\n', '')
        result = RegExExtractor.find_information_overstock(data)
        print(result)
