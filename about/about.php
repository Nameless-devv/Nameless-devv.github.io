<?php
// Check if form data is received via POST
if ($_SERVER["REQUEST_METHOD"] == "POST") {
  $name = $_POST['name'];
  $email = $_POST['email'];
  $message = $_POST['message'];
  
  // Add your code here to send an email, store the data, etc.
  // For now, we’ll simulate a successful response
  $response = array("success" => true);

  // Send response back as JSON
  echo json_encode($response);
}
?>