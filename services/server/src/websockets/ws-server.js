const { Server } = require("socket.io");
const logger = require("../utils/logger");
const wsAuth = require("./ws-auth");

const io = new Server({
  cors: { origin: "*" },
});

io.use((socket, next) => wsAuth(socket, next));

io.on("connection", (socket) => {
  logger.info(`there was a connection from: ${socket.user.email}`);
  const room = socket.user._id.toString();
  socket.join(room);

  socket.on("python_client_connected", (message) => {
    io.to(room).emit("python_client_connected", message);
  });

  socket.on("user_start_exercise", (message) => {
    io.to(room).emit("user_start_exercise", message);
  });

  socket.on("user_stop_exercise", (message) => {
    io.to(room).emit("user_stop_exercise", {
      msg: "User requested to stop exercise",
    });
  });

  socket.on("python_client_data", (message) => {
    io.to(room).emit("python_client_data", message);
  });

  socket.on("disconnect", (reason) => {
    logger.info(JSON.stringify(reason, null, 4));
    io.to(room).emit("user_stop_exercise", {
      msg: "User disconnected",
    });
  });
});

module.exports = io;
