<?php
	class RegisterView extends View {
		public function show() {
		
			$this->title = "Registrazione - CAI Sovico";
			$this->scripts = array();
			
			include("templates/registerTemplate.php");
		}
		
	}
?>
