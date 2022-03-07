const io = require("socket.io")(5000, {
  cors: {
    origin: "*",
  },
});

io.on("connection", (socket) => {
  console.log("a user connected");
  console.log(socket.id);
  socket.on("disconnect", () => {
    console.log("user disconnected");
  });

  socket.on("click", (data) => {
    console.log(data);
  });
});
