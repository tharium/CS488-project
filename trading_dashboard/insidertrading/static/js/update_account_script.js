document.addEventListener('DOMContentLoaded', function () {
    const updateForm = document.getElementById('updateAccountForm');

    if(updateForm) {
        updateForm.addEventListener('submit', function (e) {
    
            const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    
            let username = document.getElementById('username').value.trim();
            let email = document.getElementById('email').value.trim();
            let password = document.getElementById('password').value;
            let confirmPassword = document.getElementById('confirmPassword').value;
            let blocked_sources = document.getElementById('blocked_sources').value;
            //let blocked_sources_list = blocked_sources.split(',').map(source => source.trim());

            //console.log(username, email, password, confirmPassword);
    
            if (!username){
                username = null;
            }
            if (!email){
                email = null;
            }
            if (!password){
                password = null;
            }
            if (!confirmPassword){
                confirmPassword = null;
            }
            if (!blocked_sources){
                blocked_sources = null;
            }
        });
    }
    
});