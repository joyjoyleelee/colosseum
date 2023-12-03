let socketio = io();

function create_listing(){
  console.log("sending create listing info")
  socketio.emit("listing-create", "MARCO")
}

