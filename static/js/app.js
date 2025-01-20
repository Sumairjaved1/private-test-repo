document.addEventListener('DOMContentLoaded', function () {
    // Handle Create Item
    document.getElementById('create-form').addEventListener('submit', function (e) {
        e.preventDefault();
        const id = document.getElementById('create-id').value;
        const value = document.getElementById('create-value').value;

        fetch('/item', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ id, value })
        })
        .then(response => response.json())
        .then(data => {
            displayMessage(data.message || data.error);
            document.getElementById('create-form').reset();
            getItems(); // Refresh the item list
        })
        .catch(error => console.error('Error:', error));
    });

    // Handle Update Item
    document.getElementById('update-form').addEventListener('submit', function (e) {
        e.preventDefault();
        const id = document.getElementById('update-id').value;
        const value = document.getElementById('update-value').value;

        fetch(`/item/${id}`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ value })
        })
        .then(response => response.json())
        .then(data => {
            displayMessage(data.message || data.error);
            document.getElementById('update-form').reset();
            getItems(); // Refresh the item list
        })
        .catch(error => console.error('Error:', error));
    });

    // Handle Delete Item
    document.getElementById('delete-form').addEventListener('submit', function (e) {
        e.preventDefault();
        const id = document.getElementById('delete-id').value;

        fetch(`/item/${id}`, {
            method: 'DELETE',
        })
        .then(response => response.json())
        .then(data => {
            displayMessage(data.message || data.error);
            document.getElementById('delete-form').reset();
            getItems(); // Refresh the item list
        })
        .catch(error => console.error('Error:', error));
    });

    document.getElementById('get-item-form').addEventListener('submit', function (e) {
        e.preventDefault();
        const itemId = document.getElementById('item-id').value;
    
        fetch(`/item/${itemId}`, {
            method: 'GET',
        })
        .then(response => response.json())
        .then(data => {
            console.log(data);  // Log the response data for debugging
            if (data.error) {
                alert(`Error: ${data.error}`);
            } else {
                alert(`Item: ${JSON.stringify(data)}`);
            }
        })
        .catch(error => {
            console.error('Error:', error);
            alert('An error occurred while fetching the item');
        });
    });

    // Display Items
    function getItems() {
        fetch('/items') // Get all items
            .then(response => response.json())
            .then(data => {
                let itemList = '';
                for (const [id, value] of Object.entries(data)) {
                    itemList += `<div><strong>ID:</strong> ${id} <br><strong>Value:</strong> ${value}</div>`;
                }
                document.getElementById('items-list').innerHTML = itemList;
            })
            .catch(error => console.error('Error:', error));
    }

    // Display Message
    function displayMessage(message) {
        const messageBox = document.getElementById('message');
        messageBox.textContent = message;
    }

    // Initial fetch to display items
    getItems();
});

document.getElementById('create-form').addEventListener('submit', function(event) {
    event.preventDefault();

    const id = document.getElementById('create-id').value;
    const value = document.getElementById('create-value').value;

    // Example of submitting the form data via Fetch API
    fetch('/item', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({ id: id, value: value })
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message); // Show success message
    })
    .catch(error => {
        alert('Error: ' + error.message); // Show error message
    });
});
