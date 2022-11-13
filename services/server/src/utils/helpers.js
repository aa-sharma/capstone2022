const mongoose = require("mongoose");
const path = require("path");
const fsPromises = require("fs/promises");
const jwt = require("jsonwebtoken");

const structuredClone = (val) => JSON.parse(JSON.stringify(val));

const isValidObjectId = (id) => {
  const ObjectId = mongoose.Types.ObjectId;
  if (ObjectId.isValid(id)) {
    if (String(new ObjectId(id)) === id) return true;
    return false;
  }
  return false;
};

const paginationResponse = (items, pageNumber, pageSize) => {
  let perPage = parseInt(pageSize);
  if (!perPage) {
    perPage = 10;
  }

  const pageCount = Math.ceil(items.length / perPage);

  let page = parseInt(pageNumber);
  if (!page) {
    page = 1;
  }

  if (page > pageCount) {
    page = pageCount;
  }

  return {
    page: page,
    pageCount: pageCount,
    items: items.slice(page * perPage - perPage, page * perPage),
  };
};

const readJson = async (file) => {
  const filePath = path.resolve(__dirname, "../..", file);
  const data = await fsPromises.readFile(filePath);
  const json = JSON.parse(data);
  return json;
};

const signJWT = async (user) => {
  const payload = {
    user: {
      id: user.id,
    },
  };

  return new Promise(function (resolve, reject) {
    jwt.sign(
      payload,
      process.env.JWT_SECRET,
      {
        expiresIn: 86400,
      },
      (err, token) => {
        if (err) reject(err);
        resolve(token);
      }
    );
  });
};

module.exports = {
  isValidObjectId,
  paginationResponse,
  readJson,
  signJWT,
  structuredClone,
};
