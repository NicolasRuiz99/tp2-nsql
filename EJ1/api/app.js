var redis = require('redis');
var express = require('express');
var path = require('path');
var port = 3000

const redisClient = redis.createClient(6379, "redis");
const app = express()
app.set('port', port);
app.set('view engine', 'hbs');

app.get('/', function(req, res) {
    res.render('home');
});

app.get('/cargar', function(req, res) {
    redisClient.lpush(req.query.episodio, [req.query.personaje]);
    res.render('cargar');
})

app.get('/eliminar', function(req, res) {
    redisClient.lrem(req.query.episodio, 1, req.query.personaje);
    res.render('eliminar')
})

app.get('/listar', function(req, res) {
    redisClient.lrange(req.query.episodio, 0, -1, function(err, values) {
        res.render('listado', { personajes: values, nro: req.query.episodio })
    })
})

app.listen(app.get('port'), function() {
    console.log('Server running on port ' + app.get('port'));

})

redisClient.on('connect', function() {
    console.log('Conectado a redis server')
})