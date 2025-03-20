# note that this file is project specific
import requests

# @todo
### move to class
### update logging capabilities
### enable file overwrites
### add pandas and prepare for data analysis
### start working on cli

# JSON that describes the body of the request
REQUEST_BODY = {
    "indices": [],
    "regions": [],
    "countries": [],
    "sectors": [],
    "types": [],
    "forms": [],
    "segments": [],
    "markets": [],
    "stockExchanges": [],
    "lang": "en",
    "offset": 0,
    "limit": 0,
    "sorting": "TURNOVER",  # -> gets the volume
    "sortOrder": "DESC",
}

# generic URL used for all requests
URL = "https://api.boerse-frankfurt.de"

# specific URIs constants
EQUITY_SEARCH_URI = "/v1/search/equity_search"
ITEM_MASTER_DATA_URI = "/v1/data/equity_master_data?isin="
ITEM_FUNDAMENTALS_URI = "/v1/data/equity_key_data?isin="

# API-related constants
MAX_ENTRIES = 300


# class RequestManager:
#     def __init__(self):
#         self.base_url = ""
#         self.request_body = {}

#     def set_request_body(self, request_body):
#         self.request_body = request_body

#     def set_base_url(self, base_url):
#         self.base_url = base_url

#     def post_request(
#         self,
#         uri,
#         item_limit=None,
#         list_offset=None,
#         item_sorting=None,
#         sorting_order=None,
#     ):
#         # Construct the full URL
#         full_url = self.base_url + uri
        
#         if item_limit:
#             self.request_body["limit"] = item_limit
#         if list_offset:
#             self.request_body["offset"] = list_offset
#         if item_sorting:
#             self.request_body["limit"] = item_sorting
#         if sorting_order:
#             self.request_body["offset"] = sorting_order

#         print("trying", full_url)
#         self.post_response = requests.post(full_url, json=self.request_body)
#         return self.post_response

#     def get_request(self, uri):
#         response = requests.get(self.base_url + uri)
#         return response



# results
result_list = []


# internal functions
def post_data(url, limit, offset):
    if limit:
        REQUEST_BODY["limit"] = limit
    if offset:
        REQUEST_BODY["offset"] = offset
    response = requests.post(url, json=REQUEST_BODY)
    return response


def get_data(url, limit):
    if limit:
        REQUEST_BODY["limit"] = limit

    response = requests.get(url)
    return response


# can make requests up to a limit of 300

# POST at api.boerse-frankfurt.de/v1/search/equity_search
# body {"indices":[],"regions":[],"countries":[],"sectors":[],"types":[],"forms":[],"segments":[],"markets":[],"stockExchanges":[],"lang":"en","offset":0,"limit":300,"sorting":"NAME","sortOrder":"ASC"}


def request_data(total):
    if not total:
        response = post_data(URL + EQUITY_SEARCH_URI, None, None)
        # should add error handling
        total_count = int(response.json()["recordsTotal"])
        total = total_count
    else:
        total_count = total
    
    current_counter = 1
    offset = 0
    limit = MAX_ENTRIES

    file1 = open("./output/frankfurt_companies.json", "a")
    file2 = open("./output/frankfurt_fundamentals.json", "a")
    while total_count > 0:
        if total_count < limit:
            limit = total_count

        total_count = total_count - limit
        offset = offset + limit

        response = post_data(URL + EQUITY_SEARCH_URI, limit, offset)
        file1.write(response.text)

        # extract the list
        json_list = response.json()["data"]
        for item in json_list:
            # print(item["name"]["originalValue"], "->", item["isin"])
            ### this is not working, check why
            # response = get_data(URL + ITEM_MASTER_DATA_URI + item["isin"], None)
            # print(response.json())
            response = get_data(URL + ITEM_FUNDAMENTALS_URI + item["isin"], None)
            # print(response.json())

            print("computing: " + str(current_counter) + "/" + str(total))
            current_counter = current_counter + 1

            # handle stupid case with `,` char in name
            name = item["name"]["originalValue"]
            name = name.replace(",", ".")

            market_cap = None
            no_of_shares = None
            p_e_ratio = None
            profit_per_share = None

            if "marketCapitalization" in response.json():
                market_cap = response.json()["marketCapitalization"]
            if "numberOfShares" in response.json():
                no_of_shares = response.json()["numberOfShares"]
            if "priceEarningsRatio" in response.json():
                p_e_ratio = response.json()["priceEarningsRatio"]
            if "winPerShare" in response.json():
                profit_per_share = response.json()["winPerShare"]

            # should include error handling
            result_list.append(
                {
                    "name": name,
                    "isin": item["isin"],
                    "market_cap": market_cap,
                    "no_of_shares": no_of_shares,
                    "p_e_ratio": p_e_ratio,
                    "profit_per_share": profit_per_share,
                }
            )

            file2.write(response.text)
            # print(result_list)

    file1.close()
    file2.close()


def get_list():
    return result_list
