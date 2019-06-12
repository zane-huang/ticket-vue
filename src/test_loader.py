import ticket_loader as tl
import datetime

# test request_page function
pages = dict()
for page_num in range(10):
    tl.request_page(page_num, pages)
    if pages[page_num]:
        print(f'Page {page_num} loaded with #items = ' +
              str(len(pages[page_num]['tickets'])))

# test buffering mechanism with redundant calls to the API
start = datetime.datetime.now()
for i in range(100):
    page = tl.get_page(3)
end = datetime.datetime.now()
print(f'Finished loading one page 100 times in ' + str(end - start))
