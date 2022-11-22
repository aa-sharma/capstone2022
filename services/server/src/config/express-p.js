const express = require("express");

// legendary answer to support async middleware
// https://stackoverflow.com/questions/61086833/async-await-in-express-middleware

// promise-aware handler substitute
function handleP(verb) {
  return function (...args) {
    function wrap(fn) {
      return async function (req, res, next) {
        // catch both synchronous exceptions and asynchronous rejections
        try {
          await fn(req, res, next);
        } catch (e) {
          next(e);
        }
      };
    }

    // reconstruct arguments with wrapped functions
    let newArgs = args.map((arg) => {
      if (typeof arg === "function") {
        return wrap(arg);
      } else {
        return arg;
      }
    });
    // register actual middleware with wrapped functions
    this[verb](...newArgs);
  };
}

// modify prototypes for app and router
// to add useP, allP, getP, postP, optionsP, deleteP variants
["use", "all", "get", "post", "options", "delete", "put"].forEach((verb) => {
  let handler = handleP(verb);
  express.Router[verb + "P"] = handler;
  express.application[verb + "P"] = handler;
});

module.exports = express;
