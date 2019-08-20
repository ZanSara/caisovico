<?php
	class PublicView extends View {
		public function show() {
			$this->title = "Prenotazioni - CAI Sovico";
			$this->scripts = array();
			
            include("templates/headTemplate.php");
			include("templates/bannerTemplate.php");
			
			include("templates/aboutModal.php");
			
		    include("templates/publicTemplate.php");
		    include("templates/footPublicTemplate.php");
		}
	}
?>
