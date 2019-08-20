<?php
	class LogoutView extends View {
		public function show() {
		    header("Location: ".ROOT."/#".(string)date('j-m', strtotime('yesterday')) );
            die();
		}
		
	}
?>
