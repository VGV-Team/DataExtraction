import utilities
from bs4 import BeautifulSoup


class RoadRunnerExtractor:

    @staticmethod
    def find_information(websites, parser="lxml"):
        wrapper = websites[0]
        websites = websites[1:]
        for website in websites:
            new_wrapper = ""
            wrapper_site = BeautifulSoup(wrapper, parser)
            site = BeautifulSoup(website, parser)

            wrapper_tags = [child for child in wrapper_site.recursiveChildGenerator() if getattr(child, "name", None) is not None]

            site_tags = [child for child in site.recursiveChildGenerator() if getattr(child, "name", None) is not None]
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
        elif getattr(site1, "name", None) == getattr(site2, "name", None) and site1.get("id") == site2.get("id"):
            
            # skip script and style tags and account for random whitespaces (maybe change .* to \s*)
            if getattr(site1, "name") in ["script", "style"]:
                wrapper = ".*<" + getattr(site1, "name", None) + ".*>"
                wrapper += ".*</" + getattr(site1, "name") + ">.*"
                return wrapper
            else:
                id = site1.get("id")
                if id is not None:
                    wrapper = "<" + getattr(site1, "name", None) + ".*id=\"" + id + "\".*>"
                else:
                    wrapper = "<" + getattr(site1, "name", None) + ".*>"


            # If text is constant (no mismatch), add it to regex
            if site1.find(text=True, recursive=False) == site2.find(text=True, recursive=False):
                if site1.find(text=True, recursive=False) == " ":
                    wrapper += "\s*"
                else:
                    wrapper += RoadRunnerExtractor.string_check(site1.find(text=True, recursive=False))
            else:
                # This is something we need to extract
                wrapper += "(.*)"

            children1 = site1.findChildren(recursive=False)
            children2 = site2.findChildren(recursive=False)
            k = 0
            i = 0
            while i < len(children1):
                for j in range(k, len(children2)):
                    w = RoadRunnerExtractor.extract_wrapper(children1[i], children2[j])
                    if w == "":
                        continue
                    else:
                        y = 0
                        if j - k > 0:
                            m = k
                            while m < j:
                                x, y, w2 = RoadRunnerExtractor.mismatch(children1, children2, m, 1)
                                m = m + y 
                                wrapper += w2
                        wrapper += w
                        k = j+1
                        break
                x, y, w = RoadRunnerExtractor.mismatch(children1, children2, i, 0)
                i = i + x
                wrapper += w

            wrapper += "<\/" + getattr(site1, "name", None) + ">"    
            
            
        return wrapper

    @staticmethod
    def mismatch(site1, site2, t1, ind):
        if ind == 0:
            c1 = site1[t1]
            i, j, w =RoadRunnerExtractor.optionals(site2, site1, c1, t1) 
            return j, i, w
        if ind == 1:
            c2 = site2[t1] 
            return RoadRunnerExtractor.optionals(site1, site2, c2, t1)
        return 1, 1, ""
            

    @staticmethod
    def optionals(site1, site, c, t1):
        for i in range(len(site1)):
            if getattr(site1[i], "name", None) == getattr(c, "name", None) and site1[i].get("id") == c.get("id"):
                return 1, 1, ""
        #checking for optional iterators
        j = t1 - 1
        wrapperExists = 0
        w = ""
        while j >= 0 and getattr(site[t1], "name", None) == getattr(site[j], "name", None) and site[t1].get("id") == site[j].get("id"):
            print(getattr(site[t1], "name", None) + " " + "yes1")
            if RoadRunnerExtractor.checkSqueres(site[t1], site[j]) == 1:
                print("yes11")
                if wrapperExists == 0 :
                    print("yes12")
                    w = RoadRunnerExtractor.extract_wrapper(site[t1], site[j]) 
                    wrapperExists = 1
                j = j - 1;
            else:
                break
        k = t1 + 1
        while  k < len(site) and getattr(site[t1], "name", None) == getattr(site[k], "name", None) and site[t1].get("id") == site[k].get("id") :
            print(getattr(site[t1], "name", None) + " " + "yes2")
            if RoadRunnerExtractor.checkSqueres(site[t1], site[k]) == 1:
                print("yes21")
                if wrapperExists == 0 :
                    print("yes22")
                    w = RoadRunnerExtractor.extract_wrapper(site[t1], site[k]) 
                    wrapperExists = 1
                k = k + 1;
            else:
                break

        if j == t1-1 and k == t1+1:
            w = "(" + RoadRunnerExtractor.extract_wrapper(c, c) + ")?"
            return 1, 1, w
        elif j != t1-1 and k == t1+1:
            return t1-j, 1, "((" + w + ")+)?"
        elif j == t1-1 and k != t1+1:
            return 1, k-t1, "((" + w + ")+)?"
        elif j != t1-1 and k != t1+1:
            #return t1-j, k-t1, "((" + w + ")+)?"
            return t1-j, k-t1, "((" + w + ")+)?"

    @staticmethod
    def checkSqueres(site1, site2):
        children1 = site1.findChildren(recursive=False)
        children2 = site2.findChildren(recursive=False)
        print(str(len(children1)) + " " + str(len(children2)))
        if len(children1) == len(children2):
            for i in range(len(children1)):
                if getattr(children1[i], "name", None) != getattr(children2[i], "name", None) or children1[i].get("id") != children2[i].get("id"):
                    return 0
                if checkSqueres(children1[i], children2[i]) == 0:
                    return 0
            return 1
        return 0





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

    test1 = "<HTML>Books of:<B>Mike Jones</B><IMG SRC='mike.png' /><IMG SRC='mike.png' /><UL><LI><I>Title:</I><p>Databases</p></LI><LI><I>Title:</I><p>HTML Premier</p></LI><LI><I>Title:</I><p>Javascript</p></LI></UL></HTML>"
    #print(test1.lower())
    test2 = "<HTML>Books of:<B>Paul Smith</B><UL><LI><I>Title:</I><p>Web mining</p></LI><LI><I>Title:</I><p>Data mining</p></LI></UL></HTML>"

    #test1 = '<html><div id="sub-menu">        <div class="top-container sub-menu-items" data-simplebar="init" id="sub-menu-scroll">            <div class="simplebar-track vertical" style="visibility: visible;">                <div class="simplebar-scrollbar" style="top: 2px; height: 25px;"></div>            </div>            <div class="simplebar-track horizontal" style="visibility: hidden;">                <div class="simplebar-scrollbar"></div>            </div>            <div class="simplebar-scroll-content" style="padding-right: 20px; margin-bottom: -20px;">                <div class="simplebar-content" style="padding-bottom: 20px;"> <span class=""> <a class="" href="https://www.rtvslo.si/zivljenjski-slog/ture-avanture">                                                               Ture avanture                           </a> </span> <span class=""> <a class="" href="https://www.rtvslo.si/zivljenjski-slog/kulinarika">                                                              Kulinarika                          </a> </span> <span class=""> <a class="" href="https://www.rtvslo.si/zivljenjski-slog/lepota-bivanja">                                                              Lepota bivanja                          </a> </span> <span class=""> <a class="active" href="https://www.rtvslo.si/zivljenjski-slog/avtomobilnost">                                                             Avtomobilnost                           </a> </span> <span class=""> <a class="" href="https://www.rtvslo.si/zivljenjski-slog/moda">                                                                Moda                            </a> </span> <span class=""> <a class="" href="https://www.rtvslo.si/zivljenjski-slog/ture-avanture/196x-ljubezen">                                                             196x ljubezen                           </a> </span> <span class="sub-menu-last-update" id="layout-last-update">3. 4. 2019 | 15.25</span> </div>            </div>        </div>    </div>    <div id="mobile-menu-wrapper">        <div id="right-menu-icon"> <span></span> <span></span> <span></span> <span></span> </div>    </div></html>'
    #test2 = '<html><div id="mobile-menu-wrapper">        <div id="right-menu-icon"> <span></span> <span></span> <span></span> <span></span> </div>    </div></html>'
    #print(test2.lower())
    #s = BeautifulSoup(test1, "html.parser")
    #print(s)
    #s = BeautifulSoup(test2, "html.parser")
    #print(s)

    w = RoadRunnerExtractor.find_information([data1, data2], parser="html.parser")
    #w = RoadRunnerExtractor.find_information([test2, test1], parser="html.parser")
    #print(data1.lower())
    #print(len(w), len(data1), len(data2))
    #print(w.replace(".*.*", ".*").replace("/", "\/").replace("\\\\", "\\").replace("> <", "><").lower())
    print(w.replace(".*.*", ".*").replace("\/", "/").replace(".*", "").replace("\\\\", "\\").replace("> <", "><").lower())
    #print(data1)

