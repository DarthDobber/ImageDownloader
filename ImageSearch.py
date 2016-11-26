#Searching and Downloading Google Images/Image Links

#Import Libraries

import time       #Importing the time library to check the time of code execution
import sys    #Importing the System Library
import random  #Importing the random Library
import argparse #Argument Parsing



########### Edit From Here ###########

parser = argparse.ArgumentParser()
parser.add_argument("-s", "--search", action='store', dest='search', help="Enter the image search term you wish to look for, If the search term has spaces put it within quotes")
args = parser.parse_args()

########### End of Editing ###########




#Downloading entire Web Document (Raw Page Content)
def download_page(url):
    version = (3,0)
    cur_version = sys.version_info
    if cur_version >= version:     #If the Current Version of Python is 3.0 or above
        import urllib.request    #urllib library for Extracting web pages
        try:
            headers = {}
            headers['User-Agent'] = "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36"
            req = urllib.request.Request(url, headers = headers)
            resp = urllib.request.urlopen(req)
            respData = str(resp.read())
            return respData
        except Exception as e:
            print(str(e))
    else:                        #If the Current Version of Python is 2.x
        import urllib2
        try:
            headers = {}
            headers['User-Agent'] = "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"
            req = urllib2.Request(url, headers = headers)
            response = urllib2.urlopen(req)
            page = response.read()
            return page
        except:
            return"Page Not found"



#Finding 'Next Image' from the given raw page
def _images_get_next_item(s):
    start_line = s.find('rg_di')
    if start_line == -1:    #If no links are found then give an error!
        end_quote = 0
        link = "no_links"
        return link, end_quote
    else:
        start_line = s.find('"class="rg_meta"')
        start_content = s.find('"ou"',start_line+1)
        end_content = s.find(',"ow"',start_content+1)
        content_raw = str(s[start_content+6:end_content-1])
        final_content = trim_link(content_raw)
        return final_content, end_content


#Getting all links with the help of '_images_get_next_image'
def _images_get_all_items(page):
    items = []
    while True:
        item, end_content = _images_get_next_item(page)
        if item == "no_links":
            break
        else:
            items.append(item)      #Append all the links in the list named 'Links'
            time.sleep(0.1)        #Timer could be used to slow down the request for image downloads
            page = page[end_content:]
    return items

#Finding 'Next Image' from the given raw page
def async_images_get_next_item(s):
    start_line = s.find('rg_di')
    if start_line == -1:    #If no links are found then give an error!
        end_quote = 0
        link = "no_links"
        return link, end_quote
    else:
        start_line = s.find('rg_meta')
        ou_start = s.find('"ou',start_line+1)
        start_content = s.find('http', ou_start+1)
        end_content = s.find('"ow',start_content+1)
        content_raw = str(s[start_content:end_content-4]).replace("\\", "")
        final_content = trim_link(content_raw)
        return final_content, end_content


#Getting all links with the help of '_images_get_next_image'
def async_images_get_all_items(page):
    items = []
    while True:
        item, end_content = async_images_get_next_item(page)
        if item == "no_links":
            break
        else:
            items.append(item)      #Append all the links in the list named 'Links'
            time.sleep(0.2)        #Timer could be used to slow down the request for image downloads
            page = page[end_content:]
    return items

def get_next_google_page(ei, scroll, start, page):
    i = 1
    if scroll == 684:
        ndsp = random.randint(28,40)
        imgevent_url = 'https://www.google.com/imgevent?ei=' + ei + '&iact=ms&forward=1&scroll=' + str(scroll) + '&page=' + str(page) + '&start=' + str(start) + '&ndsp=' + str(ndsp) + '&bih=946&biw=1920'
        resp = download_page(imgevent_url)
        #print(resp)
        scroll = scroll + random.randint(850,1000)
        start = start + random.randint(32,38)
        page = page + 1
        time.sleep(0.2)
    else:
        while i<4:            
            ndsp = random.randint(28,40)
            imgevent_url = 'https://www.google.com/imgevent?ei=' + ei + '&iact=ms&forward=1&scroll=' + str(scroll) + '&page=' + str(page) + '&start=' + str(start) + '&ndsp=' + str(ndsp) + '&bih=946&biw=1920'
            resp = download_page(imgevent_url)
            scroll = scroll + random.randint(850,1000)
            start = start + random.randint(32,38)
            page = page + 1
            #print(resp)
            i = i + 1
            time.sleep(0.2)
    return scroll, start, page

def get_EIValue(s):
    start_line = s.find('{kEI:')
    if start_line == -1:    #If no links are found then give an error!
        end_quote = 0
        link = "no_links"
        return link, end_quote
    else:
        start_content = s.find('{kEI:')
        end_content = s.find('kEXPI:',start_content+1)
        content_raw = str(s[start_content+7:end_content-3])
        return content_raw

def get_VEDvalue(s):
    start_line = s.find('{kEI:')
    if start_line == -1:    #If no links are found then give an error!
        end_quote = 0
        link = "no_links"
        return link, end_quote
    else:
        start_content = s.find('<div id="rg"')
        end_content = s.find('"><div',start_content+1)
        content_raw = str(s[start_content+23:end_content-2])
        return content_raw

def get_extension(s):
    start_content = s.rfind('.')
    end_content = len(s)
    content_raw = str(s[start_content:end_content])
    return content_raw

def trim_link(link):
    content_raw = link.lower()
    if content_raw.find('.jpg') != -1:
        final_content = str(link[0:content_raw.find('.jpg')+4])
    elif content_raw.find('.jpeg') != -1:
        final_content = str(link[0:content_raw.find('.jpeg')+5])
    elif content_raw.find('.png') != -1:
        final_content = str(link[0:content_raw.find('.png')+4])
    elif content_raw.find('.gif') != -1:
        final_content = str(link[0:content_raw.find('.gif')+4])
    else:
        final_content = link
    return final_content

############## Main Program ############


if args.search is not None:
    t0 = time.time()   #start the timer

    #Download Image Links
    items = []
    iteration = "Item name = " + str(args.search)
    print (iteration)
    print ("Evaluating Page 1")
    search_keywords = str(args.search)
    search = search_keywords.replace(' ','%20')    
    url = 'https://www.google.com/search?q=' + search + '&espv=2&biw=1366&bih=667&site=webhp&source=lnms&tbm=isch&sa=X&ei=XosDVaCXD8TasATItgE&ved=0CAcQ_AUoAg'
    raw_html =  (download_page(url))
    time.sleep(0.1)
    items = items + (_images_get_all_items(raw_html))
    q=100
    r=1
    scroll_value = 684
    start_value = 34
    page_value = 1
    eiValue = get_EIValue(raw_html)
    vedValue = get_VEDvalue(raw_html)
    vetValue = "1" + vedValue + "." + eiValue + "i"
    while q<1200:
        print("Evaluating Page " + str(r+1))
        scroll_value, start_value, page_value = get_next_google_page(eiValue, scroll_value, start_value, page_value)
        url2='https://www.google.com/search?async=_id:rg_s,_pms:s&ei=' + eiValue + '&espv=2&yv=2&q=' + search + '&start=' + str(q) + '&asearch=ichunk&tbm=isch&vet=' + vetValue + '&ved=' + vedValue + '&ijn=' + str(r)
        raw_html2 =  (download_page(url2))
        #print(raw_html2)
        time.sleep(0.1)
        items = items + (async_images_get_all_items(raw_html2))
        q = q + 100
        r = r + 1
    print ("Image Links = "+str(items))
    print ("Total Image Links = "+str(len(items)))
    print ("\n")


    #This allows you to write all the links into a test file. This text file will be created in the same directory as your code. You can comment out the below 3 lines to stop writing the output to the text file.
    info = open('output.txt', 'a')        #Open the text file called output.txt
    info.write(str(args.search) + ": " + str(items) + "\n\n\n")         #Write the title of the page
    info.close()                            #Close the file

    t1 = time.time()    #stop the timer
    total_time = t1-t0   #Calculating the total time required to crawl, find and download all the links of 60,000 images
    print("Total time taken: "+str(total_time)+" Seconds")
    print ("Starting Download...")

    ## To save imges to the same directory
    # IN this saving process we are just skipping the URL if there is any error

    k=0
    errorCount=0
    while(k<len(items)):
        import urllib.request 
        from urllib import error

        try:
            #print(items[k])
            req = urllib.request.Request(items[k], headers={"User-Agent": "Mozilla/5.0 (X11; Linux i686) AppleWebKit/537.17 (KHTML, like Gecko) Chrome/24.0.1312.27 Safari/537.17"})
            response = urllib.request.urlopen(req)
            extension = get_extension(items[k])
            output_file = open(str(k+1)+extension,'wb')
            data = response.read()
            output_file.write(data)
            response.close();

            print("completed ====> "+str(k+1))

            k=k+1;

        except IOError:   #If there is any IOError

            errorCount+=1
            print("IOError on image "+str(k+1))
            k=k+1;

        except error.HTTPError as e:  #If there is any HTTPError

            errorCount+=1
            print("HTTPError"+str(k))
            k=k+1;
        except error.URLError as e:

            errorCount+=1
            print("URLError "+str(k))
            k=k+1;

    print("\n")
    print("All are downloaded")
    print("\n"+str(errorCount)+" ----> total Errors")

else:
    print("Please Enter a search term using either -s or --search")
#----End of the main program ----#
