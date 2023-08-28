const cookie_agreement = document.querySelector('.cookie_agreement');
const btn_cookie = document.querySelector('.btn_cookie');

setTimeout(function(){
  cookie_agreement.classList.add('active');
}, 5000);

btn_cookie.addEventListener('click' ,()=> {
  cookie_agreement.classList.remove('active');
});