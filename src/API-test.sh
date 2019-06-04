ticket_file=../data/tickets.json

curl https://$subdomain.zendesk.com/api/v2/imports/tickets/create_many.json \
     -u $email/token:$token \
     -X POST -d @$ticket_file \
     -H "Content-Type: application/json"
