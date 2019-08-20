
 function validate(){

    // Se submitto per cancellare, salta la validazione
    if( $("#nBM-prenid").val() < 0 ){
        return true;
    }

    var now     = new Date();//(2017, 01, 01);
    var year    = now.getFullYear();

    // test regexes here http://www.regular-expressions.info/javascriptexample.html
    validators = [
         {  name:'Nome',
            type:'regex',
            required:1,
            regex:"^[\\w,\\s,àèéìòùÀÈÉÌÒÙ]+$",
            errRequired:"Inserisci il nome del cliente.",
            errNoMatch:"Inserisci un nome valido. Permessi solo lettere, numeri, spazi e virgole."
         },
         {  name:'Tel',
            type:'regex',
            required:1,
            regex:"^[+]?([0-9]|[\\s]|[-]|[(]|[)]){4,50}$",
            errRequired:"Inserisci il numero di telefono del cliente.",
            errNoMatch:"Inserisci un numero di telefono valido (min 4 max 50 caratteri). Permessi solo numeri, +, -, parentesi e spazi."
         },
         {  name:'Provincia',
            type:'regex',
            required:0,
            regex:"^[A-aZ-z\\s]+$",
            errRequired:"",
            errNoMatch:"Inserisci un nome di provincia valido. Permessi solo lettere e spazi."
         },
         {  name:'Arrivo',
            type:'regex',
            required:1,
            regex:"^(((0[1-9]|1[0-9]|2[0-9]|30)\\s(Giugno|Luglio|Agosto|Settembre))|((31)\\s(Luglio|Agosto)))\\s"+year+"$",
            errRequired:"Inserisci la data di arrivo del cliente.",
            errNoMatch:"Inserire una data di arrivo valida (compresa tra 01 Giugno "+year+" e 30 Settembre "+year+")."
         },
         {  name:'Resp',
            type:'regex',
            required:1,
            regex:"^[\\w,\\s,àèéìòùÀÈÉÌÒÙ]+$",
            errRequired:"Inserisci il tuo nome nel campo 'Responsabile della prenotazione'.",
            errNoMatch:"Inserisci un nome valido. Permessi solo lettere, numeri, spazi e virgole."
         },
         {  name:'Durata',
            type:'range',
            required:1,
            max:121,
            min:1,
            errRequired:"Inserisci la durata del soggiorno del cliente.",
            errOutOfBounds:"Inserisci un numero valido."
         },
         {  name:'Posti',
            type:'range',
            required:0,  // FIX ME
            max:16,
            min:1,
            errRequired:"Inserisci il numero di posti letto prenotati dal cliente.",
            errOutOfBounds:"Inserisci il numero di posti letto valido."
         }
    ]

    clearErrors();

    errors = 0;
    for(i=0; i < validators.length; i++){
        validator = validators[i];
        field = $("#nBM-"+ validator.name.toLowerCase());
        value = field.val().trim();

        $("#nBM-err"+validator.name).remove(); // Se c'era, lo toglie

        if(value == ""){
            if(validator.required ){
                errors =  appendError(validator.name, validator.errRequired, field);
            }
        } else {

            if(validator.type=='regex'){
                var re = new RegExp( validator.regex );
                if(!re.test( value )){
                    errors =  appendError(validator.name, validator.errNoMatch, field);
                }
            }
            if(validator.type=='range'){
                if( value<validator.min || value>validator.max ){
                    errors =  appendError(validator.name, validator.errOutOfBounds, field);
                }
            }
        }
    }

    console.log(errors);
    if(errors == 0){
        return true; // submits
    }
    return false; // does not submit
}



function appendError(name, message, field){

    if(name == 'Durata'){
        field.parent().parent().parent().addClass("has-error");
        field.parent().after('<span id="nBM-err'+name+'" class="help-block" >'+message+'</span>');
    } else {
        field.parent().parent().addClass("has-error");

        if ($("#nBM-"+name.toLowerCase()+"Lbl").length){ // if that element exists
            $("#nBM-"+name.toLowerCase()+"Lbl").text(message);
        } else {
            field.after('<span id="nBM-err'+name+'" class="help-block" >'+message+'</span>');
        }
    }


    return 1;
}



function clearErrors(){

    $(".has-error").each( function(){
        $( this ).removeClass("has-error");
    });
    $(".nBM-error").each( function(){
        $( this ).remove();
    });
}
