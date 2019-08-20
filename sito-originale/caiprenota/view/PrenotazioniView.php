<?php

	class PrenotazioniView extends View {
		public function show() {
		
			$this->title = "Tabella Ospiti - CAI Sovico";
			$this->scripts = array();
			
            include("templates/headSmallTemplate.php");
            
            if(parent::__get("METHOD") == "POST" ){
                include("templates/tabellaPrenotazioniPOSTTemplate.php");
            } else {
                include("templates/tabellaRiassuntivaGETTemplate.php");
            }
            
            include("templates/footSmallTemplate.php");
		}
		
	}
?>
