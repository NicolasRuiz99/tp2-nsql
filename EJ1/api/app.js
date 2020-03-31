var redis = require('redis');
var express = require('express');
var path = require('path');
var port = 3000

const redisClient = redis.createClient(6379, "redis");
const app = express()
app.set('port', port)

app.get('/', function(req, res) {
    res.sendFile(path.join(__dirname + '/index.html'));
});

app.get('/cargar', function(req, res) {
    redisClient.lpush(req.query.episodio, [req.query.personaje]);
    res.send(JSON.stringify("personaje cargado"))
})

app.get('/eliminar', function(req, res) {
    redisClient.lrem(req.query.episodio, 1, req.query.personaje);
    res.send(JSON.stringify("personaje eliminado"))
})

app.get('/listar', function(req, res) {
    redisClient.lrange(req.query.episodio, 0, -1, function(err, values) {
        res.send(JSON.stringify(values))
    })
})

app.listen(app.get('port'), function() {
    console.log('Server running on port ' + app.get('port'));

})

redisClient.on('connect', function() {
    console.log('Conectado a redis server')
})