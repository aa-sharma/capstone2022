const winston = require("winston");
const { combine, timestamp, printf, colorize, json } = winston.format;

const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || "info",
  transports: [
    new winston.transports.Console({
      format: combine(
        colorize(),
        timestamp({
          format: "YYYY-MM-DD hh:mm:ss.SSS A",
        }),
        printf((info) => `[${info.timestamp}] ${info.level}: ${info.message}`)
      ),
    }),
    new winston.transports.File({
      filename: "/var/log/server_logs/server_logs.log",
      format: combine(
        timestamp({
          format: "YYYY-MM-DD hh:mm:ss.SSS A",
        }),
        json()
      ),
    }),
  ],
});

module.exports = logger;
