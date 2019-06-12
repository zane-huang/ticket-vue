import json
import requests
import base64

# load config
config_file = "./config.json"
with open(config_file, 'r', encoding='UTF-8') as cf:
    config = json.load(cf)

# welcome


def print_welcome():
    print(config['welcome']['message'])


# initialize buffer object
pages = dict()

# request a page from the api


def request_page(page_num: int, pages: dict):
    if page_num in pages:
        return
    payload = {"per_page": config['pagination']['items_per_page'],
               "page": page_num}
    full_token = config['authentication']['email'] + \
        "/token:" + config['authentication']['token']
    auth = b"Basic " + base64.b64encode(full_token.encode('UTF-8'))
    headers = {"Accept": "application/json", "Authorization": auth}
    api_uri = "https://" + config['authentication']['subdomain'] + \
              ".zendesk.com/api/v2/tickets.json"
    # TODO: catch exceptions
    res = requests.get(api_uri, params=payload, headers=headers, timeout=5)
    # handle errors
    if res.status_code != 200:
        print("Request to server failed.")
        print("\tPage requested: " + page_num)
        print("\tStatus code: " + res.status_code)
        return None
    pages[page_num] = json.loads(res.text)
    return res.status_code

# interfaces for ticket_viewer


def get_page(page_num: int):
    # already buffered
    if page_num in pages:
        return pages[page_num]
    # try to retrieve from API
    elif request_page(page_num, pages):
        return pages[page_num]
    else:
        return None

def get_ticket(page_num: int, ticket_num: int):
    page = get_page(page_num)
    if page:
        tickets = page['tickets']
        if 0 < ticket_num and ticket_num <= len(tickets):
            return tickets[ticket_num - 1]
    return None
