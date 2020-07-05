let
    sequenceNumberByClient = new Map();
const uuidv4 = require('uuid/v4');
var amqp = require('amqplib/callback_api');
if (!process.env.NODE_ENV)
    process.env.NODE_ENV = 'development';
require('./config/config.js');
const configuration = global.gConfig;

const http = require('http');
const io = require("socket.io");
const server = http.createServer();
server.listen(configuration['port'], configuration['hostname']);
const socket = io.listen(server);
console.info(`Hostname : ${configuration['hostname']}, port ${configuration['port']}`);

socket.on("connection",  (socket) => {
    console.info(`Client connected [id=${socket.id}]`);
    const nameIdentifier = socket.request._query['clientId'];
    console.log(nameIdentifier);
    if (!nameIdentifier){
        console.error("nameIdentifier not found from query.");
        socket.disconnect();
        return;
    }
    // initialize this client's sequence number
    sequenceNumberByClient.set(socket, 1);
    // when socket disconnects, remove it from the list:
    const username = configuration['rabbitmq']['username'];
    const password = configuration['rabbitmq']['password'];
    const url = configuration['rabbitmq']['url'];
    let messageExchange = configuration['rabbitmq']['exchanges'].filter(o => o['name'] === 'team12-messages');
    console.log(messageExchange);
    if (!messageExchange || !messageExchange.length || messageExchange.length === 0){
        throw 'Vehicle exchange not found';
    }
    messageExchange = messageExchange[0];
    console.log(`vehicle exchange : ${JSON.stringify(messageExchange)}`);
    amqp.connect(`amqp://${username}:${password}@${url}`, function (error0, connection) {
        if (error0) {
            throw error0;
        }
            connection.createChannel(function (error1, channel) {
            const exchange = messageExchange['name'];
            channel.checkExchange(exchange);
            const uuid = uuidv4();
            channel.assertQueue(`${nameIdentifier}-${uuid}`, messageExchange['queueConfig'], function (error2, q) {
                if (error2) {
                    throw error2;
                }
                channel.bindQueue(q.queue, exchange, nameIdentifier);

                channel.consume(q.queue, function(msg) {
                    if(msg.content) {
                        socket.emit("message", msg.content.toString());
                    }
                }, {
                    noAck: false
                });
            });
        });
    });
    socket.on("disconnect", () => {
        sequenceNumberByClient.delete(socket);
        console.info(`Client gone [id=${socket.id}]`);
    });
});
