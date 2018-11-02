var http = require('http');
var request = require('request');

var server = http.createServer((req, resp)=>{
    console.log(req.method, req.url);
    let target = 'http://localhost:5000' + req.url;;
    if (req.url.indexOf('/api/v1/corporations') == 0) {
        if ('OPTIONS' == req.method) {
            resp.setHeader('Access-Control-Allow-Origin', '*');
            resp.setHeader('Access-Control-Allow-Methods', 'GET, PUT, POST, OPTIONS');
            resp.setHeader('Access-Control-Allow-Credentials', 'true');
            resp.setHeader('Access-Control-Allow-Headers', 'Content-Type,authorization')
            resp.setHeader('Content-Type', 'application/json')
            resp.end(JSON.stringify({ allow:'GET' }));
            return ;
        }
        target = 'https://namex-dev.pathfinder.gov.bc.ca' + req.url;
    }
    console.log(req.url + ' -> ' + target);

    var forward = request(target);
    req.pipe(forward);
    forward.pipe(resp);
});
var port = 5001;
server.listen(port, ()=>{
    console.log('listening port ' + port + '...');
});
