onready_callbacks = [];
function onready(fnc) {
	  onready_callbacks.push(fnc);
}

function ready(prefix) {
    console.log("ready");
	  for (var i = 0; i < onready_callbacks.length; i++) {
		    onready_callbacks[i]();
	  }
}
