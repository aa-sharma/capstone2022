const { Server } = require("socket.io");
const logger = require("../utils/logger");
const wsAuth = require("./ws-auth");

const io = new Server({
  cors: { origin: "*" },
});

io.use((socket, next) => wsAuth(socket, next));

io.on("connection", (socket) => {
  const room = socket.user._id.toString();
  socket.join(room);

  if (socket.handshake.headers["user-agent"]) {
    logger.info(`Connection From Browser: ${socket.user.email}`);
  } else {
    logger.info(`Connection From Data Processor: ${socket.user.email}`);
  }
  socket.on("python_client_connected", (message) => {
    io.to(room).emit("python_client_connected", message);
  });

  socket.on("user_start_exercise", (message) => {
    io.to(room).emit("user_start_exercise", message);
  });

  socket.on("data_processor_start_exercise", (message) => {
    io.to(room).emit("data_processor_start_exercise", message);
  });

  socket.on("user_stop_exercise", (message) => {
    io.to(room).emit("user_stop_exercise", {
      msg: "User requested to stop exercise",
    });
  });

  socket.on("exercise_completed", (message) => {
    io.to(room).emit("exercise_completed", message);
  });

  socket.on("receive_actual_position", (message) => {
    io.to(room).emit("receive_actual_position", message);
  });

  socket.on("receive_expected_position", (message) => {
    io.to(room).emit("receive_expected_position", message);
  });

  socket.on("fetch_expected_position", (message) => {
    io.to(room).emit("fetch_expected_position", message);
  });

  socket.on("disconnect", (reason) => {
    logger.info(JSON.stringify(reason, null, 4));
    io.to(room).emit("user_stop_exercise", {
      msg: "User disconnected",
    });
  });
});

module.exports = io;
