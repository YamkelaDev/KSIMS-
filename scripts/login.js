// login.js
const loginForm = document.getElementById('login-form');

loginForm.addEventListener('submit', async (e) => {
  e.preventDefault();
  
  const email = document.getElementById('email').value;
  const password = document.getElementById('password').value;
  
  try {
    const userCredential = await firebase.auth().signInWithEmailAndPassword(email, password);
    alert('Login successful!');
    window.location.href = 'dashboard.html'; // Redirect to the dashboard page
  } catch (error) {
    alert('Invalid email or password!');
  }
});
