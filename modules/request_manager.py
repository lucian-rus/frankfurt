# note that this file is project specific
import requests

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
TOTAL_COUNT_URI = "/v1/search/total_count"
EQUITY_SEARCH_URI = "/v1/search/equity_search"
ITEM_MASTER_DATA_URI = "/v1/data/equity_master_data?isin="
ITEM_FUNDAMENTALS_URI = "/v1/data/equity_key_data?isin="

# API-related constants
MAX_ENTRIES = 300


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


def request_single():
    response = post_data(URL + EQUITY_SEARCH_URI, 1, None)
    print(response.json())


def request_all(total):
    if not total:
        response = post_data(URL + TOTAL_COUNT_URI, None, None)
        # should add error handling
        total_count = int(response.text)

    total_count = total
    current_counter = 1
    offset = 0
    limit = MAX_ENTRIES

    while total_count > 0:
        if total_count < limit:
            limit = total_count

        total_count = total_count - limit
        offset = offset + limit

        response = post_data(URL + EQUITY_SEARCH_URI, limit, offset)
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

            # should include error handling
            result_list.append(
                {
                    "name": item["name"]["originalValue"],
                    "isin": item["isin"],
                    "market_cap": response.json()["marketCapitalization"],
                    "no_of_shares": response.json()["numberOfShares"],
                    "p_e_ratio": response.json()["priceEarningsRatio"],
                    "profit_per_share": response.json()["winPerShare"],
                }
            )
            # print(result_list)

def get_list():
    return result_list