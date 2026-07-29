const select = document.getElementById("themeSelect");

const savedTheme = localStorage.getItem("theme");

if(savedTheme){

    document.body.classList.add(savedTheme);

    select.value = savedTheme;

}

select.addEventListener("change",function(){

    document.body.classList.remove("light","dark");

    document.body.classList.add(this.value);

    localStorage.setItem("theme",this.value);

});