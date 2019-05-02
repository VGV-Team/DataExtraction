import utilities
from bs4 import BeautifulSoup


class RoadRunnerExtractor:

    @staticmethod
    def find_information(websites, parser="lxml"):
        #print(websites)
        wrapper = websites[0]
        websites = websites[1:]
        for website in websites:
            new_wrapper = ""
            wrapper_site = BeautifulSoup(wrapper, parser)
            site = BeautifulSoup(website, parser)

            wrapper_tags = [child for child in wrapper_site.recursiveChildGenerator()
                            if getattr(child, "name", None) is not None]

            site_tags = [child for child in site.recursiveChildGenerator()
                         if getattr(child, "name", None) is not None]

            # PROBLEM: above code generates childern with each children includign all their children and so on...
            # one solution would be to do this recursively probably

            '''

            k = 0
            for i in range(len(wrapper_tags)):
                for j in range(k, len(site_tags)):
                    print(wrapper_tags[i], " --- ", wrapper_tags[j])
                    if getattr(wrapper_tags[i], "name") == getattr(site_tags[j], "name"):
                        # tags match
                        new_wrapper += str(wrapper_tags[i])
                        k = j + 1
                        break
                    else:
                        # TODO: tag mismatch
                        pass
                    k = j+1

                    # TODO: string matching

            wrapper = new_wrapper

            '''

        #print(wrapper_site.findChildren(recursive=False)[1])

        return RoadRunnerExtractor.extract_wrapper(wrapper_site.findChildren(recursive=False)[0],
                                                   site.findChildren(recursive=False)[0])


    @staticmethod
    def string_check(s):
        if s is None:
            return ""
        return s

    @staticmethod
    def extract_wrapper(site1, site2):
        # TODO: 1. Detect constant strings and add them to wrapper DONE
        # TODO: 2. Detect different strings and add them to wrapper as #text (which we will extract) DONE
        # TODO: 3. Group lists in one wrapper line
        #  (<ul><li>item1</li><li>item2</li></ul> ===> <ul>(<li>#TEXT</li>)*</ul>

        # Assumption: EVERY text element(string) is encapsulated in a HTML tag
        #   BeautifulSoup does that automatically using 'lxml' parser. To prevent that, use 'html.parser'.
        #   This is good, but if some websites do not conform to HTML standard then the generated wrapper will be wrong.
        #   Empirical testing required :)

        wrapper = ""

        if getattr(site1, "name", None) is None or getattr(site2, "name", None) is None:
            return ""

        # Compares tags from both websites and adds same tags to 'wrapper' (one by one, sequentially)
        if getattr(site1, "name", None) == getattr(site2, "name", None):

            wrapper = "<" + getattr(site1, "name", None) + ".*>"
            # If text is constant (no mismatch), add it to regex
            if site1.find(text=True, recursive=False) == site2.find(text=True, recursive=False):
                wrapper += RoadRunnerExtractor.string_check(site1.find(text=True, recursive=False))
            else:
                # This is something we need to extract
                wrapper += "(.*)"

            children2 = site2.findChildren(recursive=False)
            k = 0
            for c1 in site1.findChildren(recursive=False):
                for j in range(k, len(children2)):
                    w = RoadRunnerExtractor.extract_wrapper(c1, children2[j])
                    if w == "":
                        continue
                    else:
                        wrapper += w
                        k = j+1
                        break
            wrapper += "<\/" + getattr(site1, "name", None) + ">"

        return wrapper


if __name__ == "__main__":
    file1 = open("resources/rtvslo.si/Audi A6 50 TDI quattro_ nemir v premijskem razredu - RTVSLO.si.html",
                  encoding="UTF-8")
    data1 = file1.read().replace('\r', '').replace('\n', '')
    file2 = open("resources/rtvslo.si/Volvo XC 40 D4 AWD momentum_ suvereno med najboljše v razredu - RTVSLO.si.html",
              encoding="UTF-8")
    data2 = file2.read().replace('\r', '').replace('\n', '')
    file1.close()
    file2.close()
    #body_start = utilities.find_string(data, "<body")
    #body_end = utilities.find_string(data, "</body")
    #print(data[body_start:body_end])
    soup = BeautifulSoup(data1, "lxml")
    #for c in soup.children:
    #    print("QWE")
    #    for c2 in c.children:
    #        print(c2)
    #print(soup.findChildren(recursive=False))
    #for child in soup.recursiveChildGenerator():
        #print(getattr(soup.recursiveChildGenerator()[child], "name", None))
        #print(child)
        #if getattr(child, "name") == "div":
            #print(child)
            #print(child.findChildren())
            #break

    test1 = "<HTML>Books of:<B>Paul Smith</B><UL><LI><I>Title:</I><p>Web mining</p></LI><LI><I>Title:</I><p>Data mining</p></LI>" \
            "</UL></HTML>"
    print(test1.lower())
    test2 = "<HTML>Books of:<B>Mike Jones</B><IMG SRC='mike.png' /><UL><LI><I>Title:</I><p>Databases</p></LI><LI>" \
            "<I>Title:</I><p>HTML Premier</p></LI><LI><I>Title:</I><p>Javascript</p></LI></UL></HTML>"

    #s = BeautifulSoup(test1, "html.parser")
    #print(s)
    #s = BeautifulSoup(test2, "html.parser")
    #print(s)

    #w = RoadRunnerExtractor.find_information([data1, data2], parser="html.parser")
    w = RoadRunnerExtractor.find_information([test1, test2], parser="html.parser")
    print(len(w), len(data1), len(data2))
    print(w.replace(".*.*", ".*"))
    print(data1)

