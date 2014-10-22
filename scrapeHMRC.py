## Grabs data from HMRC's web database of tax exempt heritage art obkects
## and reads them into a delimited text file.

## This code was developed from squinting at the fine work of
## http://programminghistorian.org/ 

# Grab HTML page

import urllib.request
import time

count = 0
pageid = 1504 # first viable ID

while count < 2000:
    url_number = str(pageid)
    url = "http://www.visitukheritage.gov.uk/servlet/com.eds.ir.cto.servlet.CtoDetailServlet?ID="
    full_url = url + url_number

    print("Grabbing web page id " + str(pageid))
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
        startLoc = pageContents.find('Unique ID:')
        endLoc = pageContents.find('Home')
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
    print("Removing blank lines and headers...")
    
    new_text = (stripTags(pageContents))
    new_text = new_text.replace('\n', '') # remove whitespace

# Convert headings to row and column spacing
# Hash is used as a delimiter because it does occur in the data

    new_text = new_text.replace('Unique ID:', '\n')
    new_text = new_text.replace('Category:', '#')
    new_text = new_text.replace('Access Details:', '#')
    new_text = new_text.replace('Contact Name:', '#')
    new_text = new_text.replace('Contact Address:', '#')
    new_text = new_text.replace('Contact Reference:', '#')
    new_text = new_text.replace('Telephone No:', '#')
    new_text = new_text.replace('Fax Number:', '#')
    new_text = new_text.replace('Email:', '#')
    new_text = new_text.replace('Description:', '#')
    new_text = new_text.replace('Web Site(s):', '#')
    new_text = new_text.replace('Other Linked Exempt Items', '')  

# Output new content to a file

    print("\nAdding to file...")

    output_file = open("art4.txt", "a") # a for append, w for write
                    
    output_file.write(new_text)
    output_file.close()

    count += 1
    pageid += 1

    print("\n",count, "items saved successfully.\n")

    time.sleep(0.5)


print ("\nAll operations completed")
