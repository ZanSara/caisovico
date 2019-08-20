<?php
include("Model.php");

	class LoginModel extends Model {
	
        public function login($username, $password) {
            // Using prepared statements means that SQL injection is not possible. 
            if ($stmt = $this->mysqli->prepare( "SELECT username, password 
                                                 FROM Utenti
                                                 WHERE username = ?
                                                 LIMIT 1"
                                               )) {
                $stmt->bind_param('s', $username);  // Bind "$email" to parameter.
                $stmt->execute();    // Execute the prepared query.
                $stmt->store_result();
         
                // get variables from result.
                $stmt->bind_result($username, $db_password);
                $stmt->fetch();
                
                if ($stmt->num_rows == 1) {
                    
                    // Check if the password in the database matches
                    // the password the user submitted. We are using
                    // the password_verify function to avoid timing attacks.
                    if (password_verify($password, $db_password)) {
                    
                        // Password is correct!
                        // Get the user-agent string of the user.
                        $user_browser = $_SERVER['HTTP_USER_AGENT'];
                        // XSS protection as we might print this value
                        //$username = preg_replace("/[^a-zA-Z0-9_\-]+/", "", $username);
                        $_SESSION['username'] = $username;
                        $_SESSION['login_string'] = hash('sha512', $db_password . $user_browser);
                        
                        // We record the login into the database
                        $now = time();
                        $this->mysqli->query(   "INSERT INTO Logins(username, time, successful)
                                                VALUES ({$username}, {$now}, 1)");
                        // Login successful.
                        return true;
                        
                    
                    } else {
                        // Password is not correct
                        // We record this attempt in the database
                        $now = time();
                        $this->mysqli->query(   "INSERT INTO Logins(username, time, successful)
                                                VALUES ({$username}, {$now}, 0)");
                        return false;
                    }
                } else {
                    // No user exists.
                    return false;
                }
            }
        }
    }
?>
