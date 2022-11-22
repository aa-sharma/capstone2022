import Toast from "./toast.js";
import { SERVER_BASE_URL } from "./constants.js";

class API {
  constructor({ url, method, token, body }) {
    this.url = SERVER_BASE_URL + url;
    this.method = method || "GET";
    this.body = body;
    this.toast = new Toast();

    this.headers = {
      "Content-Type": "application/json",
    };
    if (token) {
      this.headers["x-auth-token"] = token;
    }
  }

  async call(handleSuccess) {
    try {
      let options = {
        method: this.method,
        headers: this.headers,
      };

      if (this.body) {
        options["body"] = JSON.stringify(this.body);
      }

      const res = await fetch(this.url, options);
      const json = await res.json();
      if (res.status >= 200 && res.status < 300) {
        if (typeof handleSuccess === "function") {
          handleSuccess({ res, json });
        }
      } else {
        console.error(json);
        this.toast.display({
          level: "error",
          title: "Error",
          msg: json.errors[0].msg,
        });
      }
      return { res, json };
    } catch (err) {
      console.error(err);
      this.toast.display({
        level: "error",
        title: "Error",
        msg: "There was an unknown error, check console for details.",
      });
    }
  }
}

export default API;
