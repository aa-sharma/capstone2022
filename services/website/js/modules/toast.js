class Toast {
  constructor(toastOptions) {
    this.innerHTML = ``;
    this.toastOptions = toastOptions || {
      animation: true,
      autohide: true,
      delay: 5000,
    };
  }

  display({ level, title, msg }) {
    this.innerHTML = `
      <div
      id="toast"
      class="toast z-10 position-fixed"
      style="right: 1%; bottom: 5%; z-index: 20"
      >
        <div class="toast-header justify-content-between ${
          level == "error"
            ? "bg-danger"
            : level == "success"
            ? "bg-success"
            : ""
        }">
          <!-- <img src="..." class="rounded mr-2" alt="..." /> -->
          <span class="text-light">
          ${
            level == "error"
              ? '<i class="fa-solid fa-square-xmark fa-xl"></i>'
              : level == "success"
              ? '<i class="fa-solid fa-square-check fa-xl"></i>'
              : ""
          }
          </span>
          <strong class="mr-auto text-light">${title}</strong>
          <button
            type="button"
            class="btn-close"
            style="margin-left: 0;"
            data-dismiss="toast"
            aria-label="Close"
          >
          </button>
        </div>
        <div class="toast-body">${msg}</div>
      </div>
    `;
    const body = document.getElementsByTagName("body")[0];

    let toastEl =
      document.getElementById("toast") || document.createElement("div");

    toastEl.id = "toast";
    toastEl.innerHTML = this.innerHTML;

    body.appendChild(toastEl);

    toastEl = toastEl.firstElementChild;
    const toast = new bootstrap.Toast(toastEl, this.toastOptions);

    this.__initClose(toast, toastEl);

    toast.show();
  }

  __initClose(toast, toastEl) {
    const titleEl = toastEl.firstElementChild;
    for (let button of titleEl.children) {
      if (button.tagName.toLowerCase() === "button") {
        button.addEventListener("click", () => {
          toast.hide();
        });
      }
    }
  }
}

export default Toast;
