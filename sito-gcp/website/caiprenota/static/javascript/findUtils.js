
function collectAndFind(){
    
    $('#FM_dataTitle').hide();
    $('#FM_warning').hide();
    
    $('#FM_formBox').hide();
    $('#FM_formFooter').hide();
    
    $('#FM_spinningWheel').show();
    $('#FM_loadingTitle').show();
    //$('.message').hide();
    //$('.message').text('');
    
    args = prepareFindArgs();
    findBookings(args);
}


function prepareFindArgs(){
    return {
            id: $('#FM_id').val(),
            nome : $('#FM_nome').val(),
            tel : $('#FM_tel').val(),
            giorno_inizio : $('#FM_arrivo').val(),
            provincia : $('#FM_prov').val(),
            durata : $('#FM_durata').val(),
            posti : $('#FM_posti').val(),
            responsabile : $('#FM_resp').val(),
            note : $('#FM_note').val(),
        };
}



function renderFindData(decoded){

    console.log("rendering!");
    $('#FM_spinningWheel').hide();
    $('#FM_loadingTitle').hide();
    
    nresults = 0;
    // Approfitta del loop per contare i valori
    $.each( decoded, function( key, value ) {
        nresults++;
        $('#FM_resultsTable').append(
        "<tr>"+
           "<td>"+value.id+"</td>"+
           "<td>"+value.nome+"</td>"+
           "<td>"+value.tel+"</td>"+
           "<td>"+value.giorno_inizio+"</td>"+
           "<td>"+value.durata+"</td>"+
           "<td>"+value.posti+"</td>"+
           "<td> <button id='btn-mostra-"+value.id+"' class='btn btn-success' >Mostra</button> </td>"+
        "<tr>"
        );
        $("#btn-mostra-" + value.id).click(function(){
            
            // Converte la data in achor
            exploded = value.giorno_inizio.split(" ");
            exploded[1] = "0"+decodeMonth(exploded[1]);
            anchor = exploded[0]+"-"+exploded[1];
            // Scrolla alla linea giusta
            var row = document.getElementById(anchor);
            row.scrollIntoView(true);
            // Mette il bordo
            $(".P"+value.id).css("border", "4px solid white");
            // chiude il modal
            $('#FindModal').modal('hide');
        });
        
    });
    $('#FM_NumResults').text(nresults);
    
    if(nresults==0){
        $('#FM_resultsTable').hide();
    } else {
        $('#FM_resultsTable').show();
    }
    
    $('#FM_dataTitle').text("Risultati");
    $('#FM_dataTitle').show();
    $('#FM_resultsBox').show();
    $('#FM_resultsFooter').show();

}


function resetFindModal(){
    //$("#findmessage-alert").hide();
    $("#FM_errorAlert").hide();
    $("#FM_effFooter").hide();
    
    $('#FM_spinningWheel').hide();
    $('#FM_loadingTitle').hide();
    
    $("#FM_id").val(""),
    $("#FM_nome").val(""),
    $("#FM_tel").val(""),
    $("#FM_arrivo").val(""),
    $("#FM_prov").val(""),
    $("#FM_durata").val(""),
    $("#FM_posti").val(""),
    $("#FM_resp").val(""),
    $("#FM_note").val(""),
    
    $("#FM_dataTitle").show();
    $("#FM_dataTitle").text("Cerca");
    $("#FM_warning").show();
    $("#FM_formBox").show();
    $("#FM_formFooter").show();
    $("#FM_resultsBox").hide();
    $("#FM_resultsTable").hide();
    $("#FM_resultsFooter").hide();
    
    
    $("#FM_resultsTable tr").remove();
    $("#FM_resultsTable tr").append(
        // l'header della tabella
        "<tr><th>Numero</th><th>Nome</th><th>Telefono</th><th>Arrivo</th><th>Durata</th><th>Posti</th><th></th><tr>"
    );
    
    
}

