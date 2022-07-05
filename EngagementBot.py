import sys
import InstaScraper
import TwitterScraper
import FBScraper
import LinkedInScraper
import csv

# Key = Company Name
# Value = social media url
company_list = {'Mindbloom': ['mymindbloom', 'mymindbloom', 'mmindbloom', 'mymindbloom'],
                'Field Trip Health': ['fieldtriphealth', 'fieldtriphealth', 'NA', 'fieldtriphealth'],
                'Nushama': ['i', 'nushamawellness', 'f', 'l'],
                'Nue Life': ['i', 'nuelifehealth', 'f', 'l'],
                'Fluence': ['i', 'Fluencetraining', 'f', 'l'],
                'Osmind': ['i', 'OsmindHQ', 'f', 'l'],
                'Innerwell': ['i', 'HelloInnerwell', 'f', 'l'],
                'Peak Psychedelics': ['i', 'NA', 'f', 'l'],
                }


# Takes userinput, calls Scraper, then passes to handleCSV
def run():
    print(company_list.keys())
    company = input("Choose from the list: ")
    for i in company_list:
        if i == company:
            break
    else:
        print('Run again. Incorrect Company Name')
        sys.exit()

    social_list = ['Insta', 'Twitter', 'FB', 'LinkedIn']
    print(f'\n Which of {company} socials would you like to check?')
    # Removes socialmedia from choice if NA
    index = -1
    for app in company_list.get(company):
        index += 1
        if app == "NA":
            social_list.pop(index)

    social = input(f'{social_list}: ')
    for i in social_list:
        if i == social:
            break
    else:
        print('Run again. Incorrect Social Name')
        sys.exit()

    print(f"\n Loading engagement data for {company}'s {social}...")

    # runs scraper method given name of company and url page to start visit
    # a,b,c,d stands for agruments (Company, Followers, Engagement, Dates)
    if social == 'Insta':
        InstaScraper.run(company, company_list.get(company)[0])
    elif social == 'Twitter':
        a, b, c, d = TwitterScraper.run(company, company_list.get(company)[1])
        handleCSV(a, b, c, d)
    elif social == 'FB':
        FBScraper.run(company, company_list.get(company)[2])
    else:
        LinkedInScraper.run(company, company_list.get(company)[3])


# Data comes in key/value pair. {"Company":, "FollowerCount":, "Engagement":, "Dates":}
def handleCSV(Company, Followers, Engagement, Dates):
    with open('Engagement.csv', 'w', encoding='utf8', newline='') as csv_file:
        header = [f'{Company}', f'{Followers}']
        subheader = ['Engagement', 'Post-Dates']
        writer = csv.writer(csv_file)
        writer.writerow(header)
        writer.writerow(subheader)
        writer.writerows(zip(Engagement, Dates))


# runs code
run()
