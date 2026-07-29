document.addEventListener("DOMContentLoaded", function () {

    // ==========================
    // Show / Hide Password
    // ==========================
    const togglePassword = document.getElementById("togglePassword");
    const password = document.getElementById("password");

    if (togglePassword && password) {
        togglePassword.addEventListener("click", function () {

            if (password.type === "password") {
                password.type = "text";
                this.classList.remove("fa-eye");
                this.classList.add("fa-eye-slash");
            } else {
                password.type = "password";
                this.classList.remove("fa-eye-slash");
                this.classList.add("fa-eye");
            }

        });
    }

    // ==========================
    // Dark Mode
    // ==========================
    const darkToggle = document.getElementById("darkMode");

    if (darkToggle) {

        if (localStorage.getItem("theme") === "dark") {
            document.body.classList.add("dark");
            darkToggle.checked = true;
        }

        darkToggle.addEventListener("change", function () {

            if (this.checked) {
                document.body.classList.add("dark");
                localStorage.setItem("theme", "dark");
            } else {
                document.body.classList.remove("dark");
                localStorage.setItem("theme", "light");
            }

        });

    }

    // ==========================
    // Save Button
    // ==========================
    const saveBtn = document.getElementById("saveBtn");

    if (saveBtn) {
        saveBtn.addEventListener("click", function () {

            alert("Settings Saved Successfully!");

        });
    }

    // ==========================
    // Notification Toggle
    // ==========================
    const notification = document.getElementById("notification");

    if (notification) {

        notification.addEventListener("change", function () {

            if (this.checked) {
                console.log("Notifications Enabled");
            } else {
                console.log("Notifications Disabled");
            }

        });

    }

});