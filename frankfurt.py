from modules import request_manager

# @todo
### add json body alteration posibility

# request_single()
request_manager.request_data(None)
res_list = request_manager.get_list()

file = open("./output/frankfurt.csv", "a")
for item in res_list:
    # print(item)
    file.write(
        item["name"]
        + ","
        + item["isin"]
        + ","
        + str(item["market_cap"])
        + ","
        +  str(item["no_of_shares"])
        + ","
        +  str(item["p_e_ratio"])
        + ","
        +  str(item["profit_per_share"])
        + "\n"
    )
file.close()

# we can use slug param to generate the page for each company
# we can use isin to formulate the endpoint to which to request more data regarding the company
### GET https://api.boerse-frankfurt.de/v1/data/price_information/single?isin=DE0007030009&mic=XFRA -> gets data about price and stuff
### GET https://api.boerse-frankfurt.de/v1/data/equity_master_data?isin=DE0007030009 -> gets data about industry and stuff
