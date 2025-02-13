document.getElementById("contact-form").addEventListener("submit", function(event) {
    event.preventDefault(); // Prevents the default form submission (page reload)

    // Get the values from the form fields
    let name = document.getElementById("name").value;
    let email = document.getElementById("email").value;
    let message = document.getElementById("message").value;

    // Display a loading message or status
    let messageStatus = document.getElementById("message-status");
    messageStatus.innerHTML = "Sending your message...";

    // Simulate message sending (you can replace this with actual form submission code)
    setTimeout(function() {
        // Simulating message sent successfully
        messageStatus.innerHTML = "Message sent successfully! Thank you, " + name + ".";

        // After showing success, reload the page after a short delay
        setTimeout(function() {
            location.reload(); // Reload the page
        }, 2000); // Adjust delay before reload as needed (in ms)
    }, 1000); // Simulate sending delay (in ms)
});