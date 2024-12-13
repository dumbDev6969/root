function submitForm() {
    const form = document.getElementById('contactForm');
    const formData = new FormData(form);
    const jsonData = {};
    formData.forEach((value, key) => {
        jsonData[key] = value;
    });
    console.log('JSON data:', jsonData);

    fetch('http://127.0.0.1:11352/contact_sendmail', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(jsonData),
    })
    .then(response => response.json())
    .then(data => {
        alert('Message sent successfully!');
        console.log('Success:', data);
    })
    .catch((error) => {
        alert('Message sending failed!');
        console.error('Error:', error);
    });
}