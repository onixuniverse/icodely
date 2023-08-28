const input_password = document.getElementById('id_password');
const switch_password = document.getElementById('switch_password');

switch_password.addEventListener('click' ,() => {
  if(input_password.type === 'password') {
      input_password.type = 'text';
      switch_password.innerHTML = '<i class="">';
  } else {
      input_password.type = 'password';
      switch_password.innerHTML = '<i class="">';
  }
});