let Socket=io();
Socket.on('connect',()=>{
    Socket.emit('ok',{data:'OK'})
})