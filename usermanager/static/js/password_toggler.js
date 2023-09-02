// Общая функция переключения видимости пароля
const togglePasswordVisibility = (inputElem, toggleElem) => {
  if (inputElem.type === "password") {
    inputElem.type = "text";
    toggleElem.innerHTML = '<i class="far fa-eye">'; 
  } else {
    inputElem.type = "password";
    toggleElem.innerHTML = '<i class="far fa-eye-slash">';
  }
}

// Код только для страницы регистрации  
if (document.getElementById('registerForm')) {

    const register_password  = document.getElementById('id_password1');
    const register_toggle = document.getElementById('toggle_password1');
    const register_password_confirm = document.getElementById('id_password2');
    const register_toggle_confirm = document.getElementById('toggle_password2');
  
    register_toggle.addEventListener("click", () => {
      togglePasswordVisibility(register_password, register_toggle);
    });

    register_toggle_confirm.addEventListener("click", () => {
        togglePasswordVisibility(register_password_confirm, register_toggle_confirm);
      });
}

// Код только для страницы авторизации  
if (document.getElementById('loginForm')) {

  const login_password = document.getElementById('id_password');
  const login_toggle = document.getElementById('toggle_password');

  login_toggle.addEventListener("click", () => {
    togglePasswordVisibility(login_password, login_toggle);
  });
}