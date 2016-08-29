var io = require('socket.io').listen(80);

io.sockets.on('connection', function (socket) {
    socket.on("getSomeData", function(name,fn) {
        fn({data: "some random data"});
    });
});