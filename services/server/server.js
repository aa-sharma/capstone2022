const express = require("./src/config/express-p");
const { connectDB, initExercises } = require("./src/config/db");
const http = require("http");
const path = require("path");
const io = require("./src/websockets/ws-server");
const logger = require("./src/utils/logger");
const createAdminUser = require("./src/config/createAdminUser");
const cors = require("cors");

const app = express();
const server = http.createServer(app);

const runServer = async () => {
  // Connect DB
  await connectDB();

  // Init middleware
  app.useP(express.json({ extended: false }));

  app.useP(cors());

  app.getP("/", (req, res) =>
    res.json({ msg: "Welcome to the Apollo API..." })
  );

  app.useP("/api/users", require("./src/routes/users"));
  app.useP("/api/auth", require("./src/routes/auth"));
  app.useP("/api/exercise", require("./src/routes/exercise"));
  app.useP("/api/initilize", require("./src/routes/initilize-data"));
  app.useP(
    "/api/user-level-progress",
    require("./src/routes/user-level-progress")
  );

  await createAdminUser();

  if (process.env.NODE_ENV === "development") {
    // Do something
  }

  const PORT = process.env.SERVER_PORT || 5000;

  io.listen(server);
  server.listen(PORT, () => logger.info(`Server started on port ${PORT}`));
};

runServer();

// print object
// logger.info(JSON.stringify(object, null, 4))
