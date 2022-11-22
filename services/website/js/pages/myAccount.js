import API from "../modules/api.js";
import Form from "../modules/form.js";
import Toast from "../modules/toast.js";

const token = localStorage["token"];
const nameInput = document.getElementById("name");
const productCodeInput = document.getElementById("productCode");
const passwordInput = document.getElementById("password");

const setUserDetails = async () => {
  const api = new API({ url: "/api/auth", token });
  const { json } = await api.call();
  nameInput.value = json.name;
  productCodeInput.value = json.productCode || "";
  passwordInput.value = "";
};

const constraints = {
  name: {
    length: {
      minimum: 3,
    },
  },
  productCode: {
    length: {
      minimum: 6,
      maximum: 20,
    },
  },
};

const method = "PUT";
const formId = "updateForm";
const errorTitle = "Invalid Form Details";
const errorMsg =
  "Invalid form details. Please check error messages on the form.";

const endpointUrl = "/api/users";

const toast = new Toast();
const form = new Form({
  endpointUrl,
  method,
  token,
  constraints,
  formId,
  errorTitle,
  errorMsg,
});

form.initForm((json) => {
  toast.display({
    level: "success",
    title: "Update Successful",
    msg: "Successfully updated user settings!",
  });
  passwordInput.value = "";
});

setUserDetails();
