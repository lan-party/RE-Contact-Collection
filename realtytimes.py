import requests
import time
import usaddress

# REALTY TIMES

baseurl = "https://realtytimes.com/archives/itemlist/user/"
# currentid = 66469
currentid = 834161

while True:
    try:
        resp = requests.get(baseurl+str(currentid))

        print(str(currentid))
        if "userURL" in str(resp.content):
            print("Found one")
            authors = open("realtytimes_authors.txt", 'a')
            authors.write(str(currentid)+"\n")
            authors.close()
    except Exception:
        print("Waiting")
        time.sleep(60*30)
    currentid += 1
    time.sleep(1)


# collect name, email, phone number, website, linkedin, twitter, facebook, youtube, location, number of posts, latest post date

authors = open("realtytimes_authors.txt", "r").read().splitlines()

for a in range(7535, len(authors)):
    resp = requests.get(authors[a])

    name = ""
    if '<meta name="author" content="' in str(resp.content):
        name = str(resp.content).split('<meta name="author" content="')[1]
        name = name.split('"')[0]

    email = ""
    if 'addy_text' in str(resp.content):
        email = str(resp.content).split('addy_text')[1]
        email = email.split("= ")[1]
        email = email.split(";document.")[0]
        email = email.replace("\\' + \\'", "")
        email = email.replace("\\'", "")
        email = email.replace("#", "")
        email = email.split("&")
        reconstructed_email = ""
        for b in range(0, len(email)):
            if ";" not in email[b]:
                reconstructed_email += email[b]
            else:
                reconstructed_email += str(chr(int(email[b].split(";")[0])))+email[b].split(";")[1]
        email = reconstructed_email

    phone = ""
    if "<b>(m) </b> " in str(resp.content):
        phone = str(resp.content).split("<b>(m) </b> ")[1]
        phone = phone[:12]
    elif "<b>(o) </b> " in str(resp.content):
        phone = str(resp.content).split("<b>(o) </b> ")[1]
        phone = phone[:12]

    website = ""
    if 'Website: <a href="' in str(resp.content):
        website = str(resp.content).split('Website: <a href="')[1]
        website = website.split('"')[0]

    linkedin = ""
    if "linkedin.com" in str(resp.content):
        linkedin = str(resp.content).split("linkedin.com")[1]
        linkedin = linkedin.split('"')[0]
        linkedin = "https://www.linkedin.com"+linkedin
        
    twitter = ""
    if "twitter.com" in str(resp.content):
        twitter = str(resp.content).split("twitter.com")[1]
        twitter = twitter.split('"')[0]
        twitter = "https://www.twitter.com"+twitter
        if "intent/tweet?url=" in twitter:
            twitter = ""
        
    facebook = ""
    if "facebook.com" in str(resp.content):
        facebook = str(resp.content).split("facebook.com")[1]
        facebook = facebook.split('"')[0]
        facebook = "https://www.facebook.com"+facebook
        if "/tr?id=" in facebook:
            facebook = ""
        
    youtube = ""
    if "youtube.com" in str(resp.content):
        youtube = str(resp.content).split("youtube.com")[1]
        youtube = youtube.split('"')[0]
        youtube = "https://www.youtube.com"+youtube

    postcount = 0
    if "userItemTitle" in str(resp.content):
        postcount = str(resp.content).count("userItemTitle")

    lastpostdate = ""
    if '<span class="userItemDateCreated">' in str(resp.content):
        lastpostdate = str(resp.content).split('<span class="userItemDateCreated">')[1]
        lastpostdate = lastpostdate.split("<")[0]
        lastpostdate = lastpostdate.replace("\\t", "")
        lastpostdate = lastpostdate.replace("\\n", "")

    location = ""
    if "</em>" in str(resp.content):
        location = str(resp.content).split("</em>")[1]
        if "<br>" in location[:64]:
            location = location.split("<br>")[1]
            location = location.split("<hr/>")[0]
            parsedaddress = usaddress.parse(location)
            location = ""
            for b in range(0, len(parsedaddress)):
                if parsedaddress[b][1] == "PlaceName":
                    location += parsedaddress[b][0]+" "
                if parsedaddress[b][1] == "StateName":
                    location += parsedaddress[b][0]
        else:
            location = ""

    print(location)
    print(lastpostdate)
    print(postcount)
    print(youtube)
    print(facebook)
    print(twitter)
    print(linkedin)
    print(website)
    print(phone)
    print(email)
    print(name)
    print(authors[a]+"\n========================================")

    authorscsv = open("realtytimes_authors.csv", "a")
    authorscsv.write("\n\""+authors[a]+'","'+name+'","'+email+'","'+phone+'","'+website+'","'+linkedin+'","'+twitter+'","'+facebook+'","'+youtube+'","'+location+'","'+str(postcount)+'","'+lastpostdate+'"')
    
    time.sleep(1)
