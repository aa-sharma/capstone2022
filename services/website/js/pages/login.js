import Form from "../modules/form.js";

const constraints = {
  email: {
    presence: true,
    email: true,
  },
  password: {
    presence: true,
    length: {
      minimum: 6,
    },
  },
};

const formId = "loginForm";
const errorTitle = "Invalid Form Details";
const errorMsg =
  "Invalid form details. Please check error messages on the form.";
const endpointUrl = "/api/auth";

const form = new Form({
  endpointUrl,
  constraints,
  formId,
  errorTitle,
  errorMsg,
});

form.initForm(async ({ json }) => {
  localStorage["token"] = json.token;
  window.location.assign("/");
});
