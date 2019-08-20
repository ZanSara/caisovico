<?php
include("Model.php");

	class RegisterModel extends Model {
	
        public function register($username, $password) {
        
            // Sanitize and validate the data passed in
            $username = filter_input(INPUT_POST, 'username', FILTER_SANITIZE_STRING);
            
            $prep_stmt = "SELECT * FROM Utenti WHERE username = ? LIMIT 1";
            $stmt = $this->mysqli->prepare($prep_stmt);
         
           // check existing username
            if ($stmt) {
                $stmt->bind_param('s', $username);
                $stmt->execute();
                $stmt->store_result();
         
                if ($stmt->num_rows == 1) {
                    return "Nome utente già esistente. Scegline uno diverso.";
                }
            } else {
                return "Database error";
            }
         
            // Create hashed password using the password_hash function.
            // This function salts it with a random salt and can be verified with
            // the password_verify function.
            $password = password_hash($password, PASSWORD_BCRYPT);
     
            // Insert the new user into the database 
            if ($insert_stmt = $this->mysqli->prepare("INSERT INTO Utenti (username, password) VALUES (?, ?)")) {
                $insert_stmt->bind_param('ss', $username, $password);
                // Execute the prepared query.
                if (! $insert_stmt->execute()) {
                    return "Database error on INSERT";
                }
            }
            return "OK";
        }
    }
?>
