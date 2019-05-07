import utilities
from bs4 import BeautifulSoup
from bs4 import Comment
import re


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

        #return RoadRunnerExtractor.extract_wrapper(wrapper_site.findChildren(recursive=False)[0],
        #                                           site.findChildren(recursive=False)[0])
        return RoadRunnerExtractor.extract_wrapper(wrapper_site.find("body"),
                                                   site.find("body"))


    @staticmethod
    def string_check(s):
        if s is None:
            return ""
        return s.replace("?", "\?").replace(".", "\.")

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

        wrapper = list()



        if getattr(site1, "name", None) is None or getattr(site2, "name", None) is None:
            return ""
        # Compares tags from both websites and adds same tags to 'wrapper' (one by one, sequentially)
        elif getattr(site1, "name", None) == getattr(site2, "name", None) and site1.get("id") == site2.get("id"):

            if "| 28. december 2018 ob 08:51" in site1.text or "| 28. december 2018 ob 08:51" in site2.text:
                print("WQEQWE")
                print(site1.find(text=True, recursive=True).replace(" ", ""))

            # skip script and style tags and account for random whitespaces (maybe change .* to \s*)
            if getattr(site1, "name") in ["script", "style"]:
                wrapper.append(".*<" + getattr(site1, "name", None) + ".*>")
                wrapper.append(".*</" + getattr(site1, "name") + ">.*")
                return ''.join(wrapper)
            else:

                if getattr(site1, "name") in ["img", "input", "br"]:
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
            if RoadRunnerExtractor.checkSqueres(site1[i], site[t1]) == 1:
                if wrapperExists == 0:
                    w = RoadRunnerExtractor.extract_wrapper(site1[i], site[t1]) 
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

    test1 = "<HTML>Books of:<B>Mike Jones</B><IMG SRC='mike.png' /><IMG SRC='mike.png' /><UL><LI><I>Title:</I><p>Databases</p></LI><LI><I>Title:</I><p>HTML Premier</p></LI><p>ata mining</p><p>Data mining</p></UL></HTML>"
    #print(test1.lower())
    #
    test2 = "<HTML>Books of:<B>Paul Smith</B><UL><LI><I>Title:</I><p>Web mining</p></LI><LI><I>Title:</I><p>Data mining</p></LI><LI><I>Title:</I><p>ata mining</p></LI><p>Data mining</p><p>ata mining</p></UL></HTML>"

    #test1 = '<html><div id="sub-menu">        <div class="top-container sub-menu-items" data-simplebar="init" id="sub-menu-scroll">            <div class="simplebar-track vertical" style="visibility: visible;">                <div class="simplebar-scrollbar" style="top: 2px; height: 25px;"></div>            </div>            <div class="simplebar-track horizontal" style="visibility: hidden;">                <div class="simplebar-scrollbar"></div>            </div>            <div class="simplebar-scroll-content" style="padding-right: 20px; margin-bottom: -20px;">                <div class="simplebar-content" style="padding-bottom: 20px;"> <span class=""> <a class="" href="https://www.rtvslo.si/zivljenjski-slog/ture-avanture">                                                               Ture avanture                           </a> </span> <span class=""> <a class="" href="https://www.rtvslo.si/zivljenjski-slog/kulinarika">                                                              Kulinarika                          </a> </span> <span class=""> <a class="" href="https://www.rtvslo.si/zivljenjski-slog/lepota-bivanja">                                                              Lepota bivanja                          </a> </span> <span class=""> <a class="active" href="https://www.rtvslo.si/zivljenjski-slog/avtomobilnost">                                                             Avtomobilnost                           </a> </span> <span class=""> <a class="" href="https://www.rtvslo.si/zivljenjski-slog/moda">                                                                Moda                            </a> </span> <span class=""> <a class="" href="https://www.rtvslo.si/zivljenjski-slog/ture-avanture/196x-ljubezen">                                                             196x ljubezen                           </a> </span> <span class="sub-menu-last-update" id="layout-last-update">3. 4. 2019 | 15.25</span> </div>            </div>        </div>    </div>    <div id="mobile-menu-wrapper">        <div id="right-menu-icon"> <span></span> <span></span> <span></span> <span></span> </div>    </div></html>'
    #test2 = '<html><div id="mobile-menu-wrapper">        <div id="right-menu-icon"> <span></span> <span></span> <span></span> <span></span> </div>    </div></html>'
    #print(test2.lower())
    #s = BeautifulSoup(test1, "html.parser")
    #print(s)
    #s = BeautifulSoup(test2, "html.parser")
    #print(s)
    #test1 = '<HTML><p class="Body"></p> <p class="Body">Samo poglejte njegovo masko – to ogromno satovje z radarji na takem položaju, da se ti na avtocesti tudi pri 120 km/h vsi spoštljivo umikajo, saj so prepričani, da gre za Pahorjev ali Šarčev avto. Seveda, novi A6 lahko cesto in promet skenira s kar petimi radarji, petimi kamerami, infrardečo kamero za nočni vid, dvanajstimi ultrazvočnimi senzorji in laserskim čitalnikom – lidarjem. V glavnem vojaška tehnologija v službi varnosti za fante, ki smo radi gledali Top Gun, Bonda in druge možakarja s finimi igračami.</p> <p class="Body"><strong>Novo poglavje<br/></strong>Vozniški delovni prostor je novo poglavje digitalne dobe, z dvema ogromnima zaslonoma, ki tako kot naprednejši telefoni dregnejo blazinice vaših prstov, kot se sprehajate po steklu. A še bolj se nam zdi pomembno, da so osnovna stikala tam, kjer jih pričakujete. Najprej so torej zagotovili enostavno osnovo, tisti bolj "advanced" vozniki pa si lahko nato vse skupaj še veliko bolj prilagodijo. Velik korak naprej pri kabinskem udobju zaznavajo tudi na zadnji klopi, tam je prostora v vseh smereh precej več.</p> <p class="Body">Če vam pogled na Audijev spisek dodatne opreme ne odvzame volje do življenja, potem vsekakor toplo priporočamo nakup zračnega vzmetenja, saj dobi z njim A6 več različnih in vozniško zelo uporabnih karakterjev.</p> <p class="Body">Enako velja za seksi luči z inteligentno matrično osvetlitvijo, pa za športno podvozje in vsekakor za štirikolesno krmiljenje. S tem postane A6 med ovinki v občutku na volanu še veliko krajši in bolj agilen. Vse našteto smo preskušali v družbi agregata 50 TDI, ki je v resnici klasični trilitrski dizel, podkrepljen z elektromotorjem. Ja, ta audi je mehki hibrid z izjemnim navorom in dovolj moči kadar koli in kjer koli. Si pa mislimo, da bo največji del trga zadovoljil že učinkovit dvolitrski mehki hibrid z močjo 150 kilovatov.</p> <p> <iframe allowfullscreen="" border="0" frameborder="0" height="350" src="./Audi A6 50 TDI quattro_ nemir v premijskem razredu - RTVSLO.si_files/LCypVFeHy_c.html" width="100%"></iframe> </p> <p><strong>Ključni tehnični podatki:</strong></p> <p>- na testu Audi A6 50 TDI quattro tiptronic</p> <p><strong>Mere:</strong> <br/>- dolžina: 4,9 m <br/>- medosna razdalja: 2,9 m <br/>- obračalni krog: 12,1 m <br/>- prtljažnik: 530 l <br/>- masa: 1.900 kg</p> <p><strong>Pogon:</strong> <br/>- trilitrski šestvaljni dizelski motor <br/>- moč: 210 kW <br/>- navor: 620 Nm <br/>- 8-stopenjski samodejni menjalnik <br/>- pogon na vsa štiri kolesa <br/>- pnevmatike: 225/60 R17 <br/>- poraba: 6,6 l/100 km = 8,9 EUR/100 km <br/>- posoda za gorivo: 73 l <br/>- doseg: 1.106 km <br/>- izpusti CO<sub>2</sub>: 147 g/km</p> <p><strong>Stroški pri 15.000 km in 5-letni uporabi:</strong> <br/>- nakupna cena: 69.080 EUR <br/>- stroški finančnega lizinga: 4.463 EUR/5 let <br/>- stroški registracije: 10.829 EUR/5 let <br/>- stroški vzdrževanja: 1.926 EUR/5 let <br/>- stroški goriva: 6.702 EUR/75.000 km <br/>- strošek 1 kompleta pnevmatik: 716 EUR <br/>- vrednosti po 5 letih po Eurotaxu: 33.964 EUR</p> <p>- stroški skupaj: 1.001 EUR/mesec</p> <p></p></HTML>'
    #test2 = '<HTML><p>XC 40 je od tal odmaknjen konkretnih 21 cm, a sta vzmetenje in krmilni mehanizem tako nastavljena, da ponuja tudi v hitro odpeljanih ovinkih zelo dolgo nevtralno in predvidljivo lego. V premeru preskušanega modela, ki je imel v paketu R design vzmetenje še nekoliko bolj trdo, se je to samo še bolj potrdilo, a je v tem primeru treba računati na manj udobno vožnjo čez različne asfaltne grbine. Podoben razmislek velja opraviti tudi pri izbiri motorja.</p> <p>Preskušani 2-litrski dizel s 190 KM predstavlja vrh ponudbe, ki z močjo, udobjem in tudi povprečno porabo navduši predvsem pri avtocestnih dolgoprogaških izzivih, v počasni mestni vožnji ter pri pogostih postankih in speljevanjih pa deluje preveč robusten.</p> <p>XC 40 je s čvrsto gradnjo, funkcionalno in udobno kabino ter številnimi asistenčnimi sistemi in izstopajočim skandinavskim dizajnom v premišljenem trenutku vstopil na trg modnih mestnih terencev, v katerem se brez ene same sence dvoma suvereno postavi med najdražje in najbolj premijske v mestu.</p> <p><strong>Ključni tehnični podatki:</strong> <br/>- na testu Volvo XC40 2.0 TD avt awd momentum</p> <p>Mere: <br/>- dolžina: 4,4 m <br/>- medosna razdalja: 2,7 m <br/>- obračalni krog: 11,4 m <br/>- oddaljenost od tal: 21 cm <br/>- prtljažnik: 432 l <br/>- masa: 2.250 kg <br/>Pogon: <br/>- 2-litrski 4-valjni bencinski motor <br/>- moč: 140 kW <br/>- navor: 400 Nm <br/>- 8-stopenjski samodejni menjalnik <br/>- pogon na vsa štiri kolesa <br/>- pnevmatike: 235/50 R19 <br/>- poraba: 6,3 l/100 km = 8,2 EUR/100km <br/>- posoda za gorivo: 54 l <br/>- doseg: 857 km <br/>- izpusti CO2: 133 g/km</p> <p>Stroški pri 15.000 km in 5-letni uporabi: <br/>- nakupna cena: 43.619 EUR <br/>- stroški finančnega leasinga: 3.268 EUR/5 let <br/>- stroški registracije: 8.701 EUR/5 let <br/>- stroški vzdrževanja: 2.320 EUR/5 let <br/>- stroški goriva: 6.190 EUR/75.000 km <br/>- strošek 1 kompleta pnevmatik: 923 EUR <br/>- vrednosti po 5 letih po Eurotaxu: 18.886 EUR <br/>- stroški skupaj: 774 EUR/mesec</p></HTML>'


    data1 = str(preprocess(data1, parser="lxml"))
    data2 = str(preprocess(data2, parser="lxml"))

    w = RoadRunnerExtractor.find_information([data1, data2], parser="lxml")
    #w = RoadRunnerExtractor.find_information([test2, test1], parser="html.parser")
    #print(data1.lower())
    #print(len(w), len(data1), len(data2))
    print(data1)
    print(w.replace(".*.*", ".*").replace("/", "\/").replace("\\\\", "\\").replace("> <", "><").lower())
    #print(w.replace(".*.*", ".*").replace("\/", "/").replace(".*", "").replace("\\\\", "\\").replace("> <", "><").lower())
    #print(data1)

    #d1 = BeautifulSoup(data1, "html.parser")
    #print(d1.findChildren()[0])
    #print(str(d1.findChildren()[0]))
    #d1body = str(d1.find("body"))

    #print(d1body)
    #for tag in d1.recursiveChildGenerator():
    #    try:
    #        #print(tag.attrs)
    #        tag.attrs = {key:value for key,value in tag.attrs.items() if key == "id"}
    #    except:
    #        pass
    #for tag in d1.findAll(["script", "style"]):
    #    tag.extract()
    #d1body = str(d1.find("body"))
    #print("qwe: ", d1.find("body"))
    #print(w)

    print(w)
    print(data1)

    x = re.search(w, data1)
    print(x)
