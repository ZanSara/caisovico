

// ******************* MODAL LAYOUT MANAGEMENT **********************************

// Called by the footer button NuovaPrenotazione and
// by any non empty cell in the calendar
function openNewBookingModal(fillme, prenid, gestione){
    
    $("#newBookingModal").modal("show");

    if(fillme) {
        nBM_showLoading();
        getBookingData(prenid, gestione);
    }else{
        nBM_showClean();
    }

}

// Called right before the AJAX in newBookingModal
function nBM_showLoading(){
    $("#nBM-dataTitle").hide();
    $("#nBM-ModificaBtn").hide();
    $("#nBM-ChiudiTopBtn").hide();
    $("#nBM-mainForm").hide();
    $("#nBM-errorBox").hide();
    $("#nBM-SalvaBtn").hide();
    $("#nBM-EliminaBtn").hide();
    
    $("#nBM-loadingTitle").show();
    $("#nBM-spinningWheel").show();
    //$(".message").hide();
    //$(".message").text("");
}

// Called by the getBookingData() once it got data to render into newBookingModal
function renderDecodedData(decoded){

    // Hide the wheel and title
    $("#nBM-loadingTitle").hide();
    $("#nBM-spinningWheel").hide();
    
    // Renders the differences between Gestori and Clienti
    if(decoded.gestione == 1) {
        $("#nBM-dataTitle").text("Gestione");
        $("#nBM-gestioneChk").prop("checked", "checked" );
        $("#nBM-linePosti").hide();
    }else{
       $("#nBM-dataTitle").text("Prenotazione");
        $("#nBM-gestioneChk").prop("checked", "" );
    }
    if (decoded.posti == 0){
        $("#nBM-postiLbl").text("");
        $("#nBM-posti").val("");
    } else {
        $("#nBM-posti").val(decoded.posti);
        $("#nBM-postiLbl").text(decoded.posti);
    } 
    
    $("#nBM-dataTitle").append(" № "+ decoded.prenid);
    $("#nBM-dataTitle").show();
    
    // Show modal elements
    $("#nBM-mainForm").show();
    $("#nBM-ModificaBtn").show();
    $("#nBM-ChiudiTopBtn").show();
    $("#nBM-SalvaBtn").show();
    $("#nBM-EliminaBtn").hide();
    
    // Fill the form
    $("#nBM-nome").val(decoded.nome);
    $("#nBM-tel").val(decoded.tel);
    $("#nBM-provincia").val(decoded.provincia);
    $("#nBM-arrivo").val(decoded.arrivo);
    $("#nBM-arrivoLbl").text(decoded.arrivo);
    $("#nBM-durata").val(decoded.durata);
        // Posti is being set near Gestione-dependend fields
    $("#nBM-resp").val(decoded.resp);
    $("#nBM-note").val(decoded.note);
    $("#nBM-prenid").val(decoded.prenid);
    
    // Hide the button sets
    $('#nBM-arrivoBtn').hide();
    $('#nBM-postiBtn').hide();
    
    // Set the hidden checks
    console.log("unchecking nBM-newChk...");
    $("#nBM-newChk").prop("checked", false );
    $("#nBM-newChk").prop("disabled", "disabled");
    
    // Locks the modal fields
    $("#newBookingModal input").prop("readonly", true);
    $("#newBookingModal textarea").prop("readonly", true);
    $("#nBM-gestioneChk").prop("disabled", true);
    $("#nBM-arrivoBtn").hide();
    $("#nBM-postiBtn").hide();
    
}

// Called by the Modifica button.
// Enables the form, that otherwise opens fully disabled.
function nBM_enableEditing(){
    
    // Enable fields
    $("#newBookingModal input").prop("readonly", false);
    $("#newBookingModal textarea").prop("readonly", false);
    $("#nBM-gestioneChk").prop("disabled", "");
    $("#nBM-arrivoBtn").show();
    $("#nBM-postiBtn").show();
        
    // show top buttons
    $("#nBM-ChiudiTopBtn").show();
    $("#nBM-ModificaBtn").hide();

    // Enable and show Salva and Elimina
    $("#nBM-SalvaBtn").prop("disabled", false);
    $("#nBM-EliminaBtn").prop("disabled", false);
    $("#nBM-SalvaBtn").show();
    $("#nBM-EliminaBtn").show();
    
    //$("#nBM-").prop("checked", "");

}


// Called when a user clicks the Nuova Prenotazione button in the footer.
function nBM_showClean(){
    $("#nBM-loadingTitle").hide();
    $("#nBM-spinningWheel").hide();
    $("#nBM-loadingFooter").hide();
    
    $("#nBM-ModificaBtn").hide();
    $("#nBM-ChiudiTopBtn").hide();
    
    $("#nBM-errorTitle").hide();
    $("#nBM-errorBox").hide();
    
    $("#nBM-dataTitle").text("Nuova Prenotazione");
    $("#nBM-dataTitle").show();
    $("#nBM-mainForm").show();
    $("#nBM-SalvaBtn").show();
    
    $("#nBM-EliminaBtn").hide();

    // Set the booking as a new booking (WARNING)
    console.log("checking nBM-newChk in nBM-showClean!");
    $("#nBM-newChk").prop("checked", true );
    
    // Enable fields
    $("#newBookingModal input").prop("readonly", false);
    $("#newBookingModal textarea").prop("readonly", false);
    $("#nBM-gestioneChk").prop("disabled", "");
    $("#nBM-SalvaBtn").prop("disabled", "");
    $("#nBM-arrivoBtn").show();
    $("#nBM-postiBtn").show();
    
}


// Called when the Gestione checkbox of NewBookingModal is clicked
// Hides linePosti and changes the modal title
function toggleGestione(){
    if($("#nBM-gestioneChk").prop("readonly") == false){
        $("#nBM-linePosti").toggle();
        
        var text = $("#nBM-dataTitle").text(function(index,text){
            if($("#nBM-gestioneChk").prop("checked") == true){
                return text.replace("Prenotazione", "Gestione");
            }
            return text.replace("Gestione", "Prenotazione");
        });
        $("#nBM-dataTitle").text(text.text() );
    }
}


// Opens the Error Alert and shows the error.
function renderError(Exception, gotData, msg){
    // By now, it just uses the hiden elements into the newBooking modal.
    // Merge it with the PHP error rendering and the other modal"s errors!

    // need to close all modals before running??
    
    /*$('.modal').on('show.bs.modal', function () { 
        $('.modal').not($(this)).each(function () { 
            $(this).modal('hide'); 
        });
    }); */
    
    
    
    $("#nBM-dataTitle").hide();
    $("#nBM-loadingTitle").hide();
    
    $("#nBM-mainForm").hide();
    $("#nBM-spinningWheel").hide();
    
    $("#nBM-ModificaBtn").hide();
    $("#nBM-ChiudiTopBtn").hide();
    $("#nBM-SalvaBtn").hide();
    $("#nBM-EliminaBtn").hide();
    
    $("#nBM-errorTitle").show();
    $("#nBM-errorBox").show();

    $("#nBM-errorAlert").html("<h4>ERRORE INTERNO durante il caricamento: "+ msg +".</h4><p>Contatta il webmaster.<p>");// + gotData); // + " ## " + Exception);
}


// MERGE WITH PREVIOUS
function renderFindError(Exception, gotData){
    $(".loading").hide();
    $(".loadingTitle").hide();
    $(".modal-dataTitle").show();
    $(".modal-errfooter").show();
    $("#finderror-alert").show();
    $("#finderror-alert").html("<h4>ERRORE INTERNO.</h4><p>Contatta il webmaster (Codice FRE).<p>");// + gotData); // + " ## " + Exception);
    $(".modal-dataTitle").text("ERRORE");
}




function prepareDelete(){
    if (confirm("Sei sicuro di voler cancellare questa prenotazione?")) {
        //$("#moddel").prop("checked", "checked");
        //$("#modnew").prop("checked", "");
        prenid = "-" + $("#nBM-prenid").val();
        $("#nBM-prenid").val(prenid);
        $("#nBM-form").submit();
    }
}



// ******************* DATE MANAGEMENT STUFF **********************************

// Return's today's date in a readable format
function getToday(){
    var today = new Date();
    var day = today.getDate();
    var mm = today.getMonth()+1; // January is 0!
    var year = today.getFullYear();

    if(day<10) {
        day='0'+day
    } 
    var month = convertMonth(mm);
    return day+" "+month+" "+year;
}

// Convert the month number into month name
function convertMonth(mm){
    switch(mm){
        case 6:
            return 'Giugno';
        case 7:
            return 'Luglio';
        case 8:
            return 'Agosto';
        case 9:
            return 'Settembre';
        default:
            return 'FuoriStagione';
    }
    return "Errore";
}

// Convert the month name into month number
function decodeMonth(mm){
    switch(mm){
        case 'Giugno':
            return 6;
        case 'Luglio':
            return 7;
        case 'Agosto':
            return 8;
        case 'Settembre':
            return 9;
        default:
            return 0;
    }
    return 0;
}


// ******************* BUTTONS MANAGEMENT STUFF ******************************

// Utilities that manages the Date buttons on the modal
function setDay(day){
    if (day<10){
        d = "0"+day;
    } else {
        d = day
    }
    return setDateLabel(d, 0);
}
function setMonth(month){
    return setDateLabel(convertMonth(month), 1);
}

// Merges the common code of updating the Date label
function setDateLabel(value, position){

    var oldDate = $("#nBM-arrivoLbl").text();
    var splittedDate = oldDate.split(" ");
    
    if (splittedDate.length > 3){
        newText = "Giorno Mese " + new Date().getFullYear();
        $("#nBM-arrivoLbl").text(newText);
        splittedDate = newText.split(" ");;
    }
    
    splittedDate[position] = value;
    
    var newDate = splittedDate.join(" ");
    $("#nBM-arrivoLbl").text(newDate);
    $("#nBM-arrivo").val(newDate);
}

// Set Posti label
function setPosti(posti){
    $("#nBM-postiLbl").text(posti);
    $("#nBM-posti").val(posti);
}

