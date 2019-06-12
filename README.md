# Zendesk Code Challenge  
*Submission by Zeyu Huang (hzy.sync@gmail.com)*

## Introduction  

This program implements a CLI based Ticket Viewer written in python.

It features:  
- A backend `ticket_loader.py` that retrieves data from the tickets API  
  and also buffers data in a dictionary (page number -> tickets) to avoid  
  frequent calls to the APIs.
- A frontend `ticket_viewer.py` that interacts with the user and displays  
  tickets or other information.
- Test for the backend in `test_loader.py`.

## User Guide 

**Instruction for running the application**

I assume that `python3` and `pip3` are present on the machine.

```
# cd to the source folder
cd src/

# install dependencies using pip if necessary
pip3 install requests

# run the application with python3
python3 ./ticket_viewer.py

# test the backend (ticket_loader.py)
python3 ./test_loader.py

```

## TODO

- handle exceptions in using requests.get()

## Issues

## Other methods attempted

Besides the CLI implementation, an backend in Node.js was attempted.  
- This method is implemented in `src/json-server/`.
- If you `cd` to this folder and run `node app`, you can see that it actually retrieves the first 25 tickets from the API using authentication information in `src/json-server/config.json`.