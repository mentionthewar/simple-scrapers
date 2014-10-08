## To turn live Discovery data for BT 365 into semicolon delimited text file

## This code was developed from squinting at the fine work of
## http://programminghistorian.org/ 

# Grab HTML page

import urllib.request
import time

def counter(int):
    return count

def page_counter(int):
    return pageid
    
def scraper(count,pageid):
    
    while count < 172:
        url_number = str(pageid)
        url = "http://discovery.nationalarchives.gov.uk/SearchUI/Details?uri=C"
        full_url = url + url_number

        print("Grabbing web page " + url_number + "...")
        response = urllib.request.urlopen(full_url)
        pageContents1 = response.read()

# Write page to holding file

        print("Writing to buffer...")
        buffer_file = open("buffer.txt", "wb") # deal with binary/string issue
        buffer_file.write(pageContents1)
        buffer_file.close()

# Read holding file into memory
        print("Processing buffer...")
        text_file = open("buffer.txt", "r")
        pageContents = text_file.read()
        text_file.close()

# Take out the tags

        print("Stripping tags...")

        def stripTags(pageContents):

    # Choose where in the document to start
            startLoc = pageContents.find('Description:')
            endLoc = pageContents.find('Date:')
            pageContents = pageContents[startLoc:endLoc]
 
            inside = 0
            text = ''
 
            for char in pageContents:
                if char == '<':
                    inside = 1
                elif (inside == 1 and char == '>'):
                    inside = 0
                elif inside == 1:
                    continue
                else:
                    text += char
 
            return text

# Replace dots with commas (for CSV)
        print("Adjusting for CSV...")
    
        new_text = (stripTags(pageContents))
        new_text = new_text.replace('.', ';') # semi-colon separated

# Remove headings
        new_text = new_text.replace('&#163;', '')
        new_text = new_text.replace('Description:', '')
        new_text = new_text.replace('Steamer:', '')
        new_text = new_text.replace('Nature of goods:', '')
        new_text = new_text.replace('Value:', '')
        new_text = new_text.replace('Payment to:', '')
        new_text = new_text.replace('Assured:', '')
        new_text = new_text.replace('Date of Settlement:', '')

# Output new content to a file

        print("\nAdding to file...")

        output_file = open("BT365-9.csv", "a") # a for append, w for write
        output_file.write(new_text)
        output_file.close()

        count += 1
        pageid += 1

        print("\n",count, "items saved successfully.\n")

        time.sleep(2)


    print ("\nAll operations completed")

# Main body of program
# Attempt to provide robustness to server issues

try:
    scraper(0,13362486) # last reached UI
except:
    print("Encountered a problem")
    print("Waiting...")
    time.sleep(10)
    input ("\nPress the enter key to retry")
    print("Retrying...")
    print(count, pageid)
    scraper(count,pageid)
