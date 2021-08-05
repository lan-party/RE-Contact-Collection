import requests
import time
import usaddress

# RIS MEDIA

baseurl = "https://rismedia.com/newsmaker/"
currentid = 2209

while True:
    try:
        resp = requests.get(baseurl+str(currentid))

        print(currentid)
        if '<a href="http://" target="_new">VISIT WEBSITE</a>' not in str(resp.content):
            print("Found one")
            authors = open("rismedia_authors.txt", 'a')
            authors.write(str(currentid)+"\n")
            authors.close()
    except Exception:
        print("Waiting")
        time.sleep(60*30)
    currentid += 1
    time.sleep(1)


# collect name, title, company, website
# manually collect email, phone number, contact form, linkedin, location

authors = open("rismedia_authors.txt", "r").read().splitlines()

for a in range(680, len(authors)):
    resp = requests.get(authors[a])

    name = ""
    title = ""
    company = ""
    if '<strong style="color:#000;">' in str(resp.content):
        info = str(resp.content).split('<strong style="color:#000;">')[1]
        name = info.split("<")[0]

        title = info.split(">")[2]
        title = title.split("<")[0]
        title = title.replace("\\n                  ", "")

        company = info.split(">")[3]
        company = company.split("<")[0]
        company = company.replace("\\n                  ", "")

    website = ""
    if '<div class="nm-userContact">' in str(resp.content):
        website = str(resp.content).split('<div class="nm-userContact">')[1]
        website = website.split("\"")[3]

    print(website)
    print(company)
    print(title)
    print(name)
    print("========== "+str(a)+" - "+authors[a]+" ==========")

    authorscsv = open("rismedia_authors.csv", "a")
    authorscsv.write("\n\""+authors[a]+'","'+name+'","'+title+'","'+company+'","'+website+'"')
    
    time.sleep(1)
