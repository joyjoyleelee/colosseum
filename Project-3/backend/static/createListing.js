function submitItem() {
    // Implement the logic for form submission here
    // This is a placeholder function, and you should replace it with your actual submission logic
    var itemName = document.getElementById('itemName').value;
    var itemDescription = document.getElementById('itemDescription').value;
    var date = document.getElementById('itemDate').value;
    var itemPrice = document.getElementById('itemPrice').value;

    // You can access the entered values here (e.g., send them to a server)

    // Add additional logic or redirect here if needed
    const sendData = async () =>{
        //TODO: Implement send to backend
        const response = await fetch('/create-listing', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                itemName: itemName,
                itemDescription: itemDescription,
                date: date,
                itemPrice: itemPrice,
            }),
        });
        if (!response.ok) {
            throw new Error('Item not added');
        }

        const responseData = await response.json();
        console.log(responseData);
    }
    sendData()
    console.log('Form Submitted');
}