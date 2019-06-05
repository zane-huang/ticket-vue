const http = require('http');
const fs = require('fs');
const request = require('request');

// loading config
const configFile = './config.json';
const config = JSON.parse(fs.readFileSync(configFile, 'utf-8'));

// show the config in console
function showConfig(configFile) {
  fs.readFile(configFile, 'utf-8', (err, data) => {
    if (err) console.log(err);
    else console.log(`Using configuration: \n ${data}`);
  })
}

// calling the List Tickets API
// zane.zendesk.com/api/v2/tickets.json?per_page=25&page=1
// -u {email}/token:{token}
// -H "Accept: application/json"
/* 
  You must set an Accept: application/json header on all requests.
  You must supply a Content-Type: application/json header in PUT and POST requests.
  You may get a text/plain response in case of an error like a bad request. You should treat this as an error you need to fix.
*/

const subdomain = config.authentication.subdomain;
const username = config.authentication.email + '/token';
const password = config.authentication.token;
const fullToken = username + ":" + password;
const auth = "Basic " + Buffer.from(fullToken).toString("base64");

// request tickets and send it to callback
function loadPage(pageNum, per_page = 25, callback) {
  const requestURI = `https://${subdomain}.zendesk.com/api/v2/tickets.json?per_page=${per_page}&page=${pageNum}`;
  console.log(`sending request ${requestURI}`);
  request({
      method: 'GET',
      uri: requestURI,
      headers: {Accept: 'application/json', Authorization: auth}
    },
    (err, res, body) => {
      if (err) { return console.log(err); }
      callback(body);
    });
}

// start the server at hostname:port
const hostname = '127.0.0.1';
const port = 3000;

const server = http.createServer(function(req, res) {
  console.log('request made from node: ' + req.url);
  res.writeHead(200, {'Content-Type': 'application/json'});
  const myObj = {
    msg: "hey",
    time: "2019-06-04"
  };
  res.end(JSON.stringify(config));

});

server.listen(port, hostname, () => {
  console.log(`Server running at http://${hostname}:${port}`);
  console.log(`Using configuration: \n ${JSON.stringify(config)}`);
  let pages = {};
  loadPage(1, 5, (body) => {pages['1'] = body;});
  setTimeout(() => {console.log(pages)}, 3000);
});






