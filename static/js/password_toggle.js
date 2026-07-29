document.addEventListener("DOMContentLoaded", function () {

    document.querySelectorAll(".toggle-password").forEach(function(toggle){

        toggle.addEventListener("click", function(){

            const input = document.getElementById(this.dataset.target);
            const icon = this.querySelector("i");

            if(input.type === "password"){
                input.type = "text";
                icon.classList.replace("fa-eye","fa-eye-slash");
            }else{
                input.type = "password";
                icon.classList.replace("fa-eye-slash","fa-eye");
            }

        });

    });

});