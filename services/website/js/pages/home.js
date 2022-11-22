import API from "../modules/api.js";

const token = localStorage["token"];

const setUserDetails = async () => {
  const userDetailsEl = document.getElementById("user-details");

  const api = new API({ url: "/api/auth", token });
  const { json } = await api.call();

  userDetailsEl.innerHTML = `
    <span>Hello ${json.name}</span>
    <div class="text-sm">
      Currently Logged in as: ${json.email}
    </div>
  `;
};

if (token) {
  setUserDetails();
}
