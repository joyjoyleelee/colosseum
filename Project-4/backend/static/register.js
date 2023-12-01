function registerUser() {
    var username = document.getElementById('username').value;
    var password = document.getElementById('password').value;

    // You can access the entered values here (e.g., send them to a server)
    console.log('Username:', username);
    console.log('Password:', password);

    // Add additional logic or redirect here if needed
    const sendData = async () =>{
        //TODO: Implement send to backend
        //User http://locahost:8080/register when testing locally
        const response = await fetch('/registerUser', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username: username,
                password: password,
            }),
        });
        if (!response.ok) {
            console.log(response.ok)
            throw new Error('User was not registered');
        }
        const responseData = await response.json();
        console.log(responseData);
    }
    sendData()
}