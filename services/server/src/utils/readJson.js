const logger = require("./logger");
const path = require("path");
const fsPromises = require("fs/promises");

const readJson = async (file) => {
  const filePath = path.resolve(__dirname, "../..", file);
  try {
    const data = await fsPromises.readFile(filePath);
    const json = JSON.parse(data);
    return json;
  } catch (err) {
    logger.error(err);
  }
};

module.exports = readJson;
