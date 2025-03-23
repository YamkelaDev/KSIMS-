// logout.js
const logoutButton = document.getElementById('logout');

logoutButton.addEventListener('click', async (e) => {
  e.preventDefault();
  
  try {
    await firebase.auth().signOut();
    alert('Logged out successfully!');
    window.location.href = 'login.html'; // Redirect to login page
  } catch (error) {
    alert(error.message);
  }
});
