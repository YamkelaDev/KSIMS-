// register.js
const registerForm = document.getElementById('register-form');

registerForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  
  const email = document.getElementById('email').value;
  const password = document.getElementById('password').value;
  
  try {
    const userCredential = await firebase.auth().createUserWithEmailAndPassword(email, password);
    alert('Registration successful!');
    window.location.href = 'login.html'; // Redirect to login page
  } catch (error) {
    alert(error.message);
  }
});
