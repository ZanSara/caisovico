<?php

	class CalendarView extends View {
		public function show() {
			$this->title = "Prenotazioni - CAI Sovico";
			$this->scripts = array();
			
            include("templates/headTemplate.php");
			include("templates/bannerTemplate.php");
			
			// In case of Exception raised at processing time, EXCEPTION is set
			if(parent::__get("EXCEPTION") != "Missing parameter" ){
			    echo '<script> 
			                $().ready(function() { 
			                    $("#ErrorModal").modal("show"); 
			                });
			          </script>';
			}
		    include("templates/errorAlert.php"); // Required also for JS errors. Must always be there.
		    
			if(parent::__get("LastPrenID") != 0 ){
			    echo '<script> 
			                $().ready(function() { 
			                    $("#BookingIDModal").modal("show"); 
			                });
			          </script>';
			    include("templates/bookingIDAlert.php");
			}
			
			if(parent::__get("NextRow") != 0 ){
			    echo "<script> 
			                $().ready(function() { 
			                    document.getElementById('".parent::__get('NextRow')."').scrollIntoView(true); 
			                });
			          </script>";
			}
			
			include("templates/aboutModal.php");
			include("templates/advancedModal.php");
			include("templates/findModal.php");
			include("templates/newBookingModal.php");
			
		    include("templates/calendarTemplate.php");
		    include("templates/footTemplate.php");
		}
	}
?>
