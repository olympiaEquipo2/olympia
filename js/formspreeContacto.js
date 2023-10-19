  var form = document.getElementById("formContacto");
     
  
    async function handleSubmit(event) {
      event.preventDefault();

      var status = document.getElementById("form-status");
      var data = new FormData(event.target);
      fetch(event.target.action, {
        method: form.method,
        body: data,
        headers: {
            'Accept': 'application/json'
        }
      }).then(response => {
        if (response.ok) {
          status.innerHTML = "Gracias por contactarnos. Le responderemos a la brevedad!";
          form.reset()
        } else {
          response.json().then(data => {
            if (Object.hasOwn(data, 'errors')) {
              status.innerHTML = data["errors"].map(error => error["message"]).join(", ")
            } else {
              status.innerHTML = "Ocurrió un error. Intentelo nuevamente!"
            }
          })
        }
      }).catch(error => {
        status.innerHTML = "Ocurrió un error. Intentelo nuevamente!"
      });
    }
    
    form.addEventListener("submit", handleSubmit)