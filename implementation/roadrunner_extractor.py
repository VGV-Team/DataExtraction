from bs4 import BeautifulSoup
from bs4 import Comment


class RoadRunnerExtractor:

    @staticmethod
    def find_information(websites, parser="lxml"):
        wrapper = websites[0]
        websites = websites[1:]
        for website in websites:
            wrapper_site = BeautifulSoup(wrapper, parser)
            site = BeautifulSoup(website, parser)

        return RoadRunnerExtractor.extract_wrapper(wrapper_site.find("body"),
                                                   site.find("body"))


    @staticmethod
    def string_check(s):
        if s is None:
            return ""
        return s.replace("?", "\?").replace(".", "\.")

    @staticmethod
    def extract_wrapper(site1, site2):

        wrapper = list()

        if getattr(site1, "name", None) is None or getattr(site2, "name", None) is None:
            return ""
        # Compares tags from both websites and adds same tags to 'wrapper' (one by one, sequentially)
        elif getattr(site1, "name", None) == getattr(site2, "name", None) and site1.get("id") == site2.get("id"):

            # skip script and style tags and account for random whitespaces (maybe change .* to \s*)
            # This case should never happen because we preprocess the text, but just in case...
            if getattr(site1, "name") in ["script", "style"]:
                wrapper.append(".*<" + getattr(site1, "name", None) + ".*>")
                wrapper.append(".*</" + getattr(site1, "name") + ">.*")
                return ''.join(wrapper)
            else:

                if getattr(site1, "name") in ["img", "input", "br", "area"]:
                    wrapper.append(str(site1).replace("/", "\/") + "\s*")
                    return ''.join(wrapper)

                id = site1.get("id")
                if id is not None:
                    wrapper.append("<" + getattr(site1, "name", None) + " id=\"" + id + "\">")
                else:
                    wrapper.append("<" + getattr(site1, "name", None) + ">")


            # If text is constant (no mismatch), add it to regex
            if site1.find(text=True, recursive=False) == site2.find(text=True, recursive=False):
                if site1.find(text=True, recursive=False) == " ":
                    wrapper.append("\s*")
                else:
                    wrapper.append(RoadRunnerExtractor.string_check(site1.find(text=True, recursive=False)))
            else:
                # This is something we need to extract
                wrapper.append("(.*)")

            children1 = site1.findChildren(recursive=False)
            children2 = site2.findChildren(recursive=False)
            k = 0
            i = 0
            breakTrue = 0
            brothers = 1
            ind = 0
            while i < len(children1):
                for j in range(k, len(children2)):
                    w = RoadRunnerExtractor.extract_wrapper(children1[i], children2[j])
                    if w == "":
                        continue
                    else:
                        #some tags in children2 were skipped
                        if j - k > 0:
                            '''if getattr(children2[k-1], "name", None) == getattr(children2[k], "name", None) and children2[k-1].get("id") == children2[k].get("id") and RoadRunnerExtractor.checkSqueres(children2[k-1], children2[k]) == 1:
                                if getattr(children2[k], "name", None) == getattr(children2[k+1], "name", None) and children2[k].get("id") == children2[k+1].get("id") and RoadRunnerExtractor.checkSqueres(children2[k], children2[k+1]) == 1:
                                    brothers = 1
                                    ind = 0
                                else:
                                    if brothers > 1:
                                        wrapper = wrapper[:(len(wrapper) - brothers)]
                                        wrapper.append("(\s*" + RoadRunnerExtractor.extract_wrapper(children2[ind], children2[ind+1]) + ")+\s*")'''
                            m = k
                            while m < j:
                                x, y, w2 = RoadRunnerExtractor.mismatch(children1, children2, m, 1)
                                m += y
                                wrapper = wrapper[:(len(wrapper) - x)]
                                wrapper.append(w2)
                                ind = 0
                                brothers = 1
                        '''if j == k:
                            if getattr(children2[j-1], "name", None) == getattr(children2[j], "name", None) and children2[j-1].get("id") == children2[j].get("id") and RoadRunnerExtractor.checkSqueres(children2[j-1], children2[j]) == 1:
                                brothers = brothers + 1
                                ind = j - 1
                            else:
                                if brothers > 1:
                                    wrapper = wrapper[:(len(wrapper) - (brothers))]
                                    wrapper.append("(\s*" + RoadRunnerExtractor.extract_wrapper(children2[ind], children2[ind+1]) + ")+\s*")
                                    brothers = 1
                                    ind = 0'''
                        wrapper.append(w)
                        k = j+1
                        breakTrue = 1
                        break
                
                #tag in children1 did not found tag in childern2
                x = 1
                if breakTrue == 0:
                    x, y, w = RoadRunnerExtractor.mismatch(children1, children2, i, 0)
                    '''if brothers > 1:
                        wrapper = wrapper[:(len(wrapper) - brothers)]
                        wrapper.append("\s*(" + RoadRunnerExtractor.extract_wrapper(children2[ind], children2[ind+1]) + ")+\s*")'''
                    wrapper = wrapper[:(len(wrapper) - y)]                  
                    wrapper.append(w)
                    brothers = 1
                    ind = 0
                i = i + x
                breakTrue = 0

            '''if brothers > 1:
                wrapper = wrapper[:(len(wrapper) - brothers)]
                wrapper.append("\s*(" + RoadRunnerExtractor.extract_wrapper(children2[ind], children2[ind+1]) + ")+\s*")
                brothers = 1
                ind = 0'''

            #not all tags in children2 were checked
            if k <= len(children2)-1:
                m = k
                while m < len(children2):
                    x, y, w2 = RoadRunnerExtractor.mismatch(children1, children2, m, 1)
                    m = m + y
                    wrapper = wrapper[:(len(wrapper) - x)]
                    wrapper.append(w2)


            wrapper.append("<\/" + getattr(site1, "name", None) + ">\s*")
            
        return ''.join(wrapper)

    @staticmethod
    def mismatch(site1, site2, t1, ind):
        if ind == 0:
            c1 = site1[t1]
            i, j, w = RoadRunnerExtractor.optionals(site2, site1, c1, t1)
            if w == "":
                #print("in1")
                i, j, w = RoadRunnerExtractor.iterators(site2, site1, c1, t1, i)
            if j == 0:
                j = 1 
            return j, i, w
        if ind == 1:
            c2 = site2[t1] 
            i, j, w = RoadRunnerExtractor.optionals(site1, site2, c2, t1)
            if w == "":
                #print("in2")
                i, j, w = RoadRunnerExtractor.iterators(site1, site2, c2, t1, i)
            if j == 0:
                j = 1
            return i, j, w
        return 0, 0, ""
    
    @staticmethod
    def iterators(site1, site, c, t1, first):
        wrapperExists = 0
        w = RoadRunnerExtractor.extract_wrapper(c, c)
        i = t1-1
        while i>=0 and getattr(site[i], "name", None) == getattr(site[t1], "name", None) and site[i].get("id") == site[t1].get("id"):
            if RoadRunnerExtractor.checkSqueres(site[i], site[t1]) == 1:
                if wrapperExists == 0:
                    w = RoadRunnerExtractor.extract_wrapper(site[i], site[t1])
                    wrapperExists = 1
                i = i - 1
            else:
                break
        #print(str(t1) + " " +str(i))
        j = t1 + 1
        while  j < len(site) and getattr(site[t1], "name", None) == getattr(site[j], "name", None) and site[t1].get("id") == site[j].get("id") :
            if RoadRunnerExtractor.checkSqueres(site[t1], site[j]) == 1:
                if wrapperExists == 0:
                    w = RoadRunnerExtractor.extract_wrapper(site[t1], site[j]) 
                    wrapperExists = 1
                j = j + 1;
            else:
                break
        if i!=t1-1 and j!=t1+1:
            return t1-i, j-t1, "(" + w + ")+"
        elif i == t1-1 and j!=t1+1:
            return 0, j-t1, "(" + w + ")+"
        elif i!=first and j == t1+1:
            return t1-i, 0, "(" + w + ")+"
        elif i==t1-1 and j==t1+1:
            return 0, 0, w

    @staticmethod
    def optionals(site1, site, c, t1):
        for i in range(len(site1)):
            if getattr(site1[i], "name", None) == getattr(c, "name", None) and site1[i].get("id") == c.get("id"):
                return i, 1, ""
        #checking for optional iterators
        j = t1 - 1
        wrapperExists = 0
        w = RoadRunnerExtractor.extract_wrapper(c, c)
        while j >= 0 and getattr(site[t1], "name", None) == getattr(site[j], "name", None) and site[t1].get("id") == site[j].get("id"):
            #print(getattr(site[t1], "name", None) + " " + "yes1")
            if RoadRunnerExtractor.checkSqueres(site[t1], site[j]) == 1:
                #print("yes11")
                if wrapperExists == 0 :
                    #print("yes12")
                    w = RoadRunnerExtractor.extract_wrapper(site[t1], site[j]) 
                    wrapperExists = 1
                j = j - 1;
            else:
                break
        k = t1 + 1
        while  k < len(site) and getattr(site[t1], "name", None) == getattr(site[k], "name", None) and site[t1].get("id") == site[k].get("id") :
            #print(getattr(site[t1], "name", None) + " " + "yes2")
            if RoadRunnerExtractor.checkSqueres(site[t1], site[k]) == 1:
                #print("yes21")
                if wrapperExists == 0 :
                    #print("yes22")
                    w = RoadRunnerExtractor.extract_wrapper(site[t1], site[k]) 
                    wrapperExists = 1
                k = k + 1;
            else:
                break

        if j == t1-1 and k == t1+1:
            w = "(" + w + ")?"
            return 0, 0, w
        elif j != t1-1 and k == t1+1:
            return t1-j, 0, "((" + w + ")+)?"
        elif j == t1-1 and k != t1+1:
            return 0, k-t1, "((" + w + ")+)?"
        elif j != t1-1 and k != t1+1:
            #return t1-j, k-t1, "((" + w + ")+)?"
            return t1-j, k-t1, "((" + w + ")+)?"

    @staticmethod
    def checkSqueres(site1, site2):
        children1 = site1.findChildren(recursive=False)
        children2 = site2.findChildren(recursive=False)
        #print(str(len(children1)) + " " + str(len(children2)))
        if len(children1) == len(children2):
            for i in range(len(children1)):
                if getattr(children1[i], "name", None) != getattr(children2[i], "name", None) or children1[i].get("id") != children2[i].get("id"):
                    return 0
                if RoadRunnerExtractor.checkSqueres(children1[i], children2[i]) == 0:
                    return 0
            return 1
        return 0

    # Removes all attributes except 'id' and remove 'script' and 'style' tags
    # Removes comments
    # Returns <body>
    @staticmethod
    def preprocess(site_text, parser="lxml"):
        site = BeautifulSoup(site_text, parser)
        for tag in site.recursiveChildGenerator():
            try:
                tag.attrs = {key:value for key,value in tag.attrs.items() if key == "id"}
                #if isinstance(tag, Comment) or str(tag).startswith("<!--"):
                #    tag.extract()
            except:
                pass

        for tag in site.findAll(["script", "style"]):
            tag.extract()

        comments = site.findAll(text=lambda text: isinstance(text, Comment))
        for comment in comments:
            comment.extract()

        return site.find("body")

    @staticmethod
    def generate_wrapper(site1, site2):
        data1 = str(RoadRunnerExtractor.preprocess(site1, parser="lxml"))
        data2 = str(RoadRunnerExtractor.preprocess(site2, parser="lxml"))

        wrapper = RoadRunnerExtractor.find_information([data1, data2], parser="lxml")
        return wrapper.replace(".*.*", ".*").replace("/", "\/").replace("\\\\", "\\").replace("> <", "><").lower()


if __name__ == "__main__":
    file1 = open("../resources/rtvslo.si/Audi A6 50 TDI quattro_ nemir v premijskem razredu - RTVSLO.si.html",
                  encoding="UTF-8")
    data1 = file1.read().replace('\r', '').replace('\n', '')
    file2 = open("../resources/rtvslo.si/Volvo XC 40 D4 AWD momentum_ suvereno med najboljše v razredu - RTVSLO.si.html",
              encoding="UTF-8")
    data2 = file2.read().replace('\r', '').replace('\n', '')
    file1.close()
    file2.close()

    soup = BeautifulSoup(data1, "lxml")

    test1 = "<HTML>Books of:<B>Mike Jones</B><IMG SRC='mike.png' /><IMG SRC='mike.png' /><UL><LI><I>Title:</I><p>Databases</p></LI><LI><I>Title:</I><p>HTML Premier</p></LI><p>ata mining</p><p>Data mining</p></UL></HTML>"
    #print(test1.lower())
    #
    test2 = "<HTML>Books of:<B>Paul Smith</B><UL><LI><I>Title:</I><p>Web mining</p></LI><LI><I>Title:</I><p>Data mining</p></LI><LI><I>Title:</I><p>ata mining</p></LI><p>Data mining</p><p>ata mining</p></UL></HTML>"

    data1 = str(RoadRunnerExtractor.preprocess(data1, parser="lxml"))
    data2 = str(RoadRunnerExtractor.preprocess(data2, parser="lxml"))

    w = RoadRunnerExtractor.find_information([data1, data2], parser="lxml")
    #w = RoadRunnerExtractor.find_information([test2, test1], parser="html.parser")
    #print(data1.lower())
    #print(len(w), len(data1), len(data2))
    #print(data1)
    print(w.replace(".*.*", ".*").replace("/", "\/").replace("\\\\", "\\").replace("> <", "><").lower())

