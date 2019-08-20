
var baseURL = "/caiprenota";

// AJAX retrieving booking data for newBookingModal
function getBookingData(prenid, gestione){

    var decoded = 0;
    $.get( baseURL+'/dati', {
            prenid: prenid,
            gestione : gestione
        }).done(function(gotData) {
            
            try{
                var decoded = JSON.parse(gotData);
            }catch (Exception) {
                renderError(Exception, gotData);
                return;
            };
            
            renderDecodedData(decoded);

    }).fail(function() {
        renderError("Errore AJAX", "Errore AJAX", "Errore AJAX")
    });

}


// AJAX retrieving booking data for FindModal
function findBookings(args){
    
    var decoded = 0;
    $.get( baseURL+'/find', args).done(function(gotData) {
            
            //console.log(args);
            try{
                //console.log(gotData);
                var decoded = JSON.parse(gotData);
            }catch (Exception) {
                renderError(Exception, gotData);
                return;
            };
            renderFindData(decoded);

    }).fail(function() {
        renderError("Errore AJAX", "Errore AJAX", "Errore AJAX");
    });
}



