<?php

	class JSONView extends View {
		public function show() {
		
			$this->title = "JSON Service - CAI Sovico";
			$this->scripts = array();
            echo parent::__get("JSON");
		}
		
	}
?>
