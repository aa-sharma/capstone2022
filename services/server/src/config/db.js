const mongoose = require("mongoose");
const config = require("config");
const logger = require("../utils/logger");

const connectDB = async () => {
  try {
    mongoose.connect(
      `mongodb://${process.env.MONGO_INITDB_ROOT_USERNAME}:${process.env.MONGO_INITDB_ROOT_PASSWORD}@${process.env.DB_HOST}:${process.env.DB_PORT}/${process.env.MONGO_INITDB_DATABASE}`,
      {
        useNewUrlParser: true,
      }
    );

    logger.info("MongoDB Connected...");
  } catch (err) {
    logger.error(err.message);
    process.exit(1);
  }
};

module.exports = connectDB;
