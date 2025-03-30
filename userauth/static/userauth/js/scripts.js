const container = document.getElementById('container');
const registerBtn = document.getElementById('register');
const loginBtn = document.getElementById('login');

registerBtn.addEventListener('click', () => {
    container.classList.add("active");
});

loginBtn.addEventListener('click', () => {
    container.classList.remove("active");
});

// Checkbox
function toggleAdminPassword() {
    const adminPasswordField = document.getElementById('admin-password-field');
    const adminCheckbox = document.getElementById('admin');
    if (adminCheckbox.checked) {
        adminPasswordField.style.display = 'block';
    } else {
        adminPasswordField.style.display = 'none';
    }
}

document.getElementById('usuario').addEventListener('change', function() {
    if (this.checked) {
        document.getElementById('admin').checked = false;
        document.getElementById('admin-password-field').style.display = 'none';
    }
});

document.getElementById('admin').addEventListener('change', function() {
    if (this.checked) {
        document.getElementById('usuario').checked = false;
    }
});
