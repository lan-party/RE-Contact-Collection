import requests
import time
import usaddress


# INMAN

baseurl = "https://www.inman.com/category/"
categories = ["agent", "brokerage", "technology", "marketing"]
currentpage = 1
currentcategory = 0

for a in range(currentcategory, len(categories)):
    endofcategory = False
    while not endofcategory:
        try:
            resp = requests.get(baseurl+categories[a]+"/page/"+str(currentpage))
            if resp.status_code == 404:
                endofcategory = True
            else:
                authors = str(resp.content).split("/author/")
                authorfile = open("inman_authors.txt", "r+")
                authorfilecontents = authorfile.read()
                newcontents = ""
                for b in range(1, len(authors)):
                    author = authors[b].split("/")[0]
                    print(categories[a]+" - "+str(currentpage)+" - "+author)
                    if author not in authorfilecontents and author not in newcontents:
                        print("Found one")
                        newcontents += "\n"+author
                authorfile.write(newcontents)
                authorfile.close()
        except Exception:
            print("Waiting")
            time.sleep(60*15)
        currentpage += 1
        time.sleep(1)
    currentpage = 0


# collect name, facebook, linkedin, twitter, instagram
# manually collect location from linkedin available contacts

authors = open("inman_authors.txt", "r").read().splitlines()

for a in range(775, len(authors)):
    resp = requests.get(authors[a])

    name = ""
    if '<div class="name">' in str(resp.content):
        name = str(resp.content).split('<div class="name">')[1]
        name = name.split('</div>')[0]

    facebook = ""
    if '<div class="social_row facebook">' in str(resp.content):
        facebook = str(resp.content).split('<div class="social_row facebook">')[1]
        facebook = facebook.split('"')[1]

    linkedin = ""
    if '<div class="social_row linkedin">' in str(resp.content):
        linkedin = str(resp.content).split('<div class="social_row linkedin">')[1]
        linkedin = linkedin.split('"')[1]

    twitter = ""
    if '<div class="social_row twitter">' in str(resp.content):
        twitter = str(resp.content).split('<div class="social_row twitter">')[1]
        twitter = twitter.split('"')[1]

    instagram = ""
    if '<div class="social_row instagram">' in str(resp.content):
        instagram = str(resp.content).split('<div class="social_row instagram">')[1]
        instagram = instagram.split('"')[1]

    print(instagram)
    print(twitter)
    print(linkedin)
    print(facebook)
    print(name)
    print("========== "+str(a)+" - "+authors[a]+" ==========")

    authorscsv = open("inman_authors.csv", "a")
    authorscsv.write("\n\""+authors[a]+'","'+name+'","'+facebook+'","'+linkedin+'","'+twitter+'","'+instagram+'"')
    
    time.sleep(1)
