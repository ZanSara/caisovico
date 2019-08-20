<?php
include_once("config.php");

abstract class Model {

	protected $mysqli, $year;

	public function __construct($dbhost=DB_HOSTNAME, $dbuser=DB_USERNAME, $dbpwd=DB_PASSWORD, $dbname = DB_DBNAME) {
		$this->mysqli = new mysqli($dbhost, $dbuser, $dbpwd, $dbname);
		if($this->mysqli->connect_error != NULL) {
			die("Errore durante la connessione al server. ");// . $mysqli->connect_error);
		}
		$this->mysqli->set_charset("utf8");
		
		$this->year = date('Y');
		
		// In case I need some further operations to happen at construction time
		$this->customConstructor();
		
	}
	
	public function customConstructor(){}
	
	public function real_escape_string($string){
	    return $this->mysqli->real_escape_string($string);
	}

	public function __destruct() {
		$this->mysqli->close();
	}
	
	
	// *************** Utilities **********************************************
	
	public function getYear(){
	    return $this->year;
	}
	
	// Correct the strtotime output for leap years
	//  Input: date MUST STRICTLY BE in DD-MM-YYYY format
	//  Output: unless specified otherwhise, date in "z" format: "day number", db-friendly
	public function correct_date($date, $year, $format="z"){
        if($year % 4 == 0){
            return date($format, strtotime($date)-1); //   ONLY dd-mm-yyyy OR mm/dd/yyyy are recognized correctly
        }else{
            return date($format, strtotime($date));
        }
	}
	
	// Convert month number into month name
    public function convert_month($monthnum){
        
        switch ((int)$monthnum):
            case 6:
                return 'Giugno';
            case 7:
                return 'Luglio';
            case 8:
                return 'Agosto';
            case 9:
                return 'Settembre';
            default:
                throw new Exception("Il numero corrisponde a un mese non incluso nel periodo di gestione (giugno-settembre)");
                //return 'FuoriStagione';
        endswitch;
        throw new Exception("Il numero corrisponde a un mese non incluso nel periodo di gestione (giugno-settembre)");
        //return "Errore";
    } 
    
     // Convert month name into month number
    public function decode_month($monthname){

        switch ($monthname):
            case 'Giugno':
                return '06';
            case 'Luglio':
                return '07';
            case 'Agosto':
                return '08';
            case 'Settembre':
                return '09';
            default:
                throw new Exception("Il nome corrisponde a un mese non incluso nel periodo di gestione (giugno-settembre)");
                //return 'ERRORE';
        endswitch;
        throw new Exception("Il nome corrisponde a un mese non incluso nel periodo di gestione (giugno-settembre)");
        //return "Errore";
    } 


    // ************* Login management *******************************
    
    public function protectPage(){
        //session_start(); 
        if (!isset($_SESSION['username']) or !isset($_SESSION['login_string'])) {
            header("Location: ".ROOT."/login/" );
        }
    }
    
/*   
    function sec_session_start() {
        $session_name = 'sec_session_id';   // Set a custom session name
        
        // Sets the session name. 
        // This must come before session_set_cookie_params due to an undocumented bug/feature in PHP.
        session_name($session_name);
     
        $secure = true;
        $httponly = true;   // This stops JavaScript being able to access the session id.
        
        // Forces sessions to only use cookies.
        if (ini_set('session.use_only_cookies', 1) === FALSE) {
            header("Location: /caipren/login"); // Do something better...
            exit();
        }
        // Gets current cookies params.
        $cookieParams = session_get_cookie_params();
        session_set_cookie_params(
            $cookieParams["lifetime"],
            $cookieParams["path"], 
            $cookieParams["domain"], 
            $secure,
            $httponly);
     
        session_start();            // Start the PHP session 
        session_regenerate_id(true);    // regenerated the session, delete the old one. 
    }



    public function login_check() {
        // Check if all session variables are set 
        if (isset($_SESSION['username']) and isset($_SESSION['login_string']) ) {
        
        //return true;
        
            
            $login_string = $_SESSION['login_string'];
            $username = $_SESSION['username'];
     
            // Get the user-agent string of the user.
            $user_browser = $_SERVER['HTTP_USER_AGENT'];
     
            if ($stmt = $this->mysqli->prepare(   "SELECT password 
                                                  FROM Utenti
                                                  WHERE username = ? LIMIT 1")) {
                // Bind "$user_id" to parameter. 
                $stmt->bind_param('i', $username);
                $stmt->execute();   // Execute the prepared query.
                $stmt->store_result();
     
                if ($stmt->num_rows == 1) {
                    // If the user exists get variables from result.
                    $stmt->bind_result($password);
                    $stmt->fetch();
                    $login_check = hash('sha512', $password . $user_browser);
     
                    if (hash_equals($login_check, $login_string) ){
                        // Logged In!!!! 
                        return true;
                    } 
                } 
            }
        }
        // Not logged in
        return false;
    }
*/
}
?>
