function validarSignUp(event) {
    event.preventDefault(); // Previene el envío del formulario

    let username = document.getElementById('id_username').value;
    let firstName = document.getElementById('id_first_name').value;
    let lastName = document.getElementById('id_last_name').value;
    let email = document.getElementById('id_email').value;
    let password1 = document.getElementById('id_password1').value;
    let password2 = document.getElementById('id_password2').value;
    let pic = document.getElementById('id_pic').value;

    let errorMessage = '';

    if (!username) {
        errorMessage += 'El campo Usuario es obligatorio.\n';
    }
    if(username.lenght<=3){
        alert('Porfavor su nombre de usuario debe ser mayor a 3 caracteres');
    }
    if (!firstName) {
        errorMessage += 'El campo Nombre es obligatorio.\n';
    }
    if(firstName.lenght<=3){
        alert('Porfavor su nombre debe ser mayor a 3 caracteres');
    }
    if (!lastName) {
        errorMessage += 'El campo Apellido es obligatorio.\n';
    }
    if(lastName.lenght<=3){
        alert('Porfavor su apellido debe ser mayor a 3 caracteres');
    }
    if (!email) {
        errorMessage += 'El campo Email es obligatorio.\n';
    } 
    else {
        const emailPattern = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailPattern.test(email)) {
            errorMessage += 'El Email no es válido.\n';
        }
    }
    if (password1=='' || password2=='') {
        errorMessage += 'Los campos de Contraseña son obligatorios.\n';
    } 
    if (password1.lenght<=8 || password2.lenght<=8){
        alert('Cada contraseña debe ser mayor a 8 caracteres');
    }
    if (password1 !== password2) {
        errorMessage += 'Las contraseñas no coinciden.\n';
    }

    if (errorMessage) {
        alert(errorMessage);
    } 
    else {
        document.getElementById('signupForm').submit();
    }
}