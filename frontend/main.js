async function validateUser(){
    const id=document.getElementById("user_id").value;
    const email=document.getElementById("email").value;

    const data={
        "id":id,
        "email":email
    }

    const req=await fetch("http://127.0.0.1:8000/validateUser",{
        method:'POST',
        headers:{
            "Content-Type":"application/json"
        },
        body:JSON.stringify(data)
    })

    const response=await req.json();

    if(req.status === 404){
        document.getElementById("id_error").innerText="User not found";
        document.getElementById("email_error").innerText="User not found";
        
    }else{
        window.location.href="user.html";
    }
    
}
