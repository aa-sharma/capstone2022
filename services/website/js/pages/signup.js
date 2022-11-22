import Form from "../modules/form.js";

const constraints = {
  name: {
    length: {
      minimum: 3,
    },
  },
  email: {
    email: true,
  },
  password: {
    length: {
      minimum: 6,
    },
  },
};

const formId = "signupForm";
const errorTitle = "Invalid Form Details";
const errorMsg =
  "Invalid form details. Please check error messages on the form.";

const endpointUrl = "/api/users";

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
