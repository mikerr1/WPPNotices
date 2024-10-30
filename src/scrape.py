import argparse
import json
import os
import time

import requests
from bs4 import BeautifulSoup

from settings import headers, json_data, API_URL, FORMS_URL

BASE_PATH = os.getcwd()
WAIT_TIME = 3
SCRAPE_RESULT = []
form_path = os.path.join(BASE_PATH, "src", "forms.json")
scrape_result_path = os.path.join(BASE_PATH, "src", "result.csv")
scrape_result_path2 = os.path.join(BASE_PATH, "src", "result2.csv")

parser = argparse.ArgumentParser(prog="scrape.py", description="WP Public Notice Scraper")
parser.add_argument("--update", nargs="?")
parser.add_argument("--search", type=str)
parser.add_argument("--counties", type=str)
args = parser.parse_args()

print("Welcome to WashingtonPost Public Notice Scraping Demo\n"
      "\n==We currently only support county search=="
      "\n==We currently only defaulting to Legal Notice search==")
print("Loading...")
time.sleep(WAIT_TIME)

if args.update == "1":
    print("Updating parameters")
    response = requests.get(FORMS_URL, headers=headers)
    soup = BeautifulSoup(response.text, "lxml")
    forms_json = soup.find("script", {"id": "__NEXT_DATA__"}).contents[0]
    forms_json = json.loads(str(forms_json))
    # print(json.dumps(forms_json, indent=4))
    with open(form_path, "w") as f:
        f.write(json.dumps(forms_json, indent=4))
    print("Parameters updated. To continue scrape please use --search")

# check if forms data exists
if not os.path.exists(form_path):
    parser.error(
        "search parameter does not exist. Please run using -u=1 or --update=1 script first."
    )
else:
    with open(form_path, "r") as f:
        file_content = f.read()
    file_content_json = json.loads(file_content)
    notice_types = file_content_json["props"]["pageProps"]["searchControls"]["facets"]["noticeTypeFacets"]
    counties = \
    file_content_json["props"]["pageProps"]["searchControls"]["facets"][
        "countyFacets"]
    states = \
        file_content_json["props"]["pageProps"]["searchControls"]["facets"][
            "stateFacets"]

def prompt_counties():
    user_input = input("==> Type county to search: ").split(",")
    if not user_input:
        return prompt_counties()

    return [input for input in user_input if len(input) > 0]

def prompt_save():
    user_input = input("==> Type y/n to save as csv? ").strip()
    if not user_input:
        return prompt_save()
    if user_input.lower() == "n":
        exit("Thank you for checking out the demo")
    elif user_input.lower() == "y":
        return True
    else:
        prompt_save()

def scrape(API_URL, headers, json_data, page=None, size=20):
    if page is not None:
        json_data["current"] = page
        json_data["pageSize"] = size
    return requests.post(
        API_URL,
        headers=headers,
        json=json_data,
    )

if not args.counties:
    print("Counties")
    [print(county, end=" , ") for county in counties]
    print("\n")
    counties = prompt_counties()

    # API is still in demo and we populate some cities to always return results
    counties_list = ["Arlington", "Arlington Country", "Washington County", "Washington"]
    [counties_list.append(county) for county in counties]
    json_data["allFilters"].append({"county": counties_list})



    # mapping to county payload
    counties_list = ["Arlington", "Arlington Country", "Washington"]
    [counties_list.append(county) for county in counties]

    print("For demo purpose we added some counties to guarantee result. "
          "And to remind you we default to Legal Notice due to time constraint "
          "\nScraping {}".format(counties_list))
    json_data["allFilters"].append({"county": counties_list})
    time.sleep(5)

    response = scrape(API_URL, headers=headers, json_data=json_data)
    if response.status_code != 200:
        exit("Error please try again")

    # print(response.json())
    response_json = response.json()
    result_data = response_json["results"]
    [SCRAPE_RESULT.append(data) for data in result_data] # save scraped data
    page = response_json["page"]
    total_result = page["total_results"]
    print("Found {} results".format(total_result))

    save = prompt_save()
    if save:
        print("Continuing to gather data...")
        time.sleep(WAIT_TIME)
        total_pages = page["total_pages"]
        current_page = page["current"]
        while current_page < total_pages:
            next_page = current_page + 1
            next_page_scrape = scrape(API_URL,
                                      headers=headers,
                                      json_data=json_data,
                                      page=next_page
                                      )
            if next_page_scrape.status_code != 200:
                exit("Error please try again")
            current_page += 1
            response_json = next_page_scrape.json()
            result_data = response_json["results"]
            [SCRAPE_RESULT.append(data) for data in result_data]

            print("Total gathered:", len(SCRAPE_RESULT), "/", total_result)

        print("Grand total of scraped data:", len(SCRAPE_RESULT), total_result)

        # Clean up text
        cleaned_list = []
        for item in SCRAPE_RESULT:
            cleaned = item["text"].replace("\n", "")
            # print(cleaned)
            item["text"] = cleaned
            cleaned_list.append(item)

        import csv
        csv_header = cleaned_list[0].keys() # quick hack to set keys as headers
        with open(scrape_result_path, "w", encoding="utf-8", newline='') as f:
            writer = csv.DictWriter(f, fieldnames=csv_header)
            writer.writeheader()
            writer.writerows(SCRAPE_RESULT)
            print("Scrape completed")