import Toast from "./toast.js";
import { SERVER_BASE_URL } from "./constants.js";
import API from "./api.js";

class Form {
  constructor({
    endpointUrl,
    method,
    constraints,
    token,
    formId,
    errorTitle,
    errorMsg,
  }) {
    this.constraints = constraints;
    this.toast = new Toast();
    this.form = document.getElementById(formId);
    this.inputs = document.getElementsByTagName("input");

    this.errorTitle = errorTitle;
    this.errorMsg = errorMsg;

    this.method = method || "POST";
    this.token = token || null;
    this.endpointUrl = endpointUrl;
  }

  async initForm(handleSuccess) {
    this.handleSuccess = handleSuccess;
    for (let i = 0; i < this.inputs.length; i++) {
      this.inputs.item(i).addEventListener("change", (ev) => {
        const errors = validate(this.__getFormObject(), this.constraints) || {};
        this.__showErrorsForInput(ev.target, errors[ev.target.id]);
      });
    }

    this.form.addEventListener("submit", async (e) => {
      e.preventDefault();
      await this.__handleFormSubmit();
    });
  }

  async __handleFormSubmit() {
    const errors = validate(this.__getFormObject(), this.constraints);
    if (errors) {
      for (let input of this.inputs) {
        this.__showErrorsForInput(input, errors[input.id]);
      }
      this.toast.display({
        level: "error",
        title: this.errorTitle,
        msg: this.errorMsg,
      });
    } else {
      await this.__handleFormSuccess();
    }
  }

  async __handleFormSuccess() {
    const body = this.__getFormObject();

    const api = new API({
      url: this.endpointUrl,
      method: this.method,
      token: this.token,
      body,
    });
    await api.call(this.handleSuccess);
  }

  __showErrorsForInput(input, errors) {
    const redText = input.nextElementSibling;
    const label = input.previousElementSibling;
    if (errors) {
      redText.innerText = errors[0];
      input.classList.add("border-danger");
      input.classList.remove("border-success");
      label.classList.add("text-danger");
      label.classList.remove("text-success");
    } else {
      redText.innerText = "";
      input.classList.remove("border-danger");
      input.classList.add("border-success");
      label.classList.remove("text-danger");
      label.classList.add("text-success");
    }
  }

  __getFormObject = () => {
    const formObject = {};
    for (let input of this.inputs) {
      formObject[input.name] = input.value;
    }
    return formObject;
  };
}

export default Form;
