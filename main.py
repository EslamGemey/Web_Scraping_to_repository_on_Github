import requests
import csv
from itertools import zip_longest
from bs4 import BeautifulSoup
import re
import pyfiglet
import termcolor

'''
This project is used for Scrapping a User's Repositories information through a github username:
Examples of information that you can scrape....
1- Repository name
2- Repository URL
3- Stars 
4- forks
5- Issues
'''

print(termcolor.colored(pyfiglet.figlet_format("GitHub Scraper Tool"), color="green"),end=" ")

print(termcolor.colored("-"*100,color="green"))

# main program function
def getHubScrape():
    username = str(input("enter GitHub username: "))
    repo_info = []
    names = []
    urls = []
    stars = []
    forks = []
    issues = []
    url = "https://github.com/" + username + "?tab=repositories"

    while 1:
        web_url = requests.get(url)
        result = web_url.content
        soup = BeautifulSoup(result, "lxml")
        listOfRipo = soup.find_all("ul", {"data-filterable-for": "your-repos-filter"})
        for repo in listOfRipo:
            a_repo = repo.find_all("li", {
                "class": re.compile('^col-12 d-flex width-full py-4 border-bottom color-border-muted public')})

            for repoName in a_repo:
                name = repoName.find_all("h3", {"class": "wb-break-all"})
                for link in name:
                    repo_name = link.find_all("a", {"itemprop": "name codeRepository"})
                    for r in repo_name:
                        names.append((""+r.text).replace("\n        ",""))
                        url2 = str(r.get("href"))
                        urls.append("https://github.com/" + url2)

                        # get stars and forks, issues
                        web_url = requests.get("https://github.com/" + url2)
                        result = web_url.content
                        soup = BeautifulSoup(result, "lxml")
                        complete_stars = soup.find_all("span", {"id": "repo-stars-counter-star"})
                        for repo1 in range(len(complete_stars)):
                            stars.append(complete_stars[repo1].text)

                        complete_fork = soup.find_all("span", {"id": "repo-network-counter"})
                        for fork in range(len(complete_fork)):
                            forks.append(complete_fork[fork].text)

                        complete_issues = soup.find("span", {"id": "issues-repo-tab-count"})

                        if complete_issues is not None:
                            issues.append(complete_issues.text)
                        else:
                            issues.append('0')
        repo_info = [names, urls, stars, forks, issues]
        export_file = zip_longest(*repo_info)

        # saving results in CSV file
        with open("res.csv", "w") as myfile:
            wr = csv.writer(myfile)
            wr.writerow(
                ["Repository Name", "Repositories URL", "Number Of Stars", "Number Of Forks", "Number Of Issues"])
            wr.writerows(export_file)

        # get the repo information of the next page
        web_url = requests.get(url)
        result = web_url.content
        soup = BeautifulSoup(result, "lxml")
        next_page = soup.find_all('div', {'class':'paginate-container'})

        if(len(next_page) == 0):
            break
        firstPage_Next=next_page[0]
        print(next_page)
        for page in next_page:
            resultPage = page.find_all('a', {'rel': 'nofollow'})
            for node in resultPage:
                if node.text == "Next":
                    firstPage_Next=node
                    print(node.text)
                else:
                    firstPage_Next=None
        if firstPage_Next is not None:
            url = firstPage_Next.get('href')
            print(url)
        else:
            print("--OK--")
            # exit from loop
            break
    for user in repo_info:
        print(user)


# Execution
getHubScrape()