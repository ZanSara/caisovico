
<?
// Server-side PHP for the AJAX calls

$gestione = $_GET['gestione'];

if ($gestione == 0){
    $json = json_encode(
        array(
            "nome" => "Nome",
            "tel" => "Telefono",
            "prenid" => "ID",
            "arrivo" => "Arrivo",
            "durata" => "X notti",
            "posti" => "X",
            "resp" => "Responsabile",
            "note" => "Note"
    ));
}else{
    $json = json_encode(
        array(
            "nome" => "Nome",
            "tel" => "Telefono",
            "prenid" => "ID",
            "arrivo" => "Arrivo",
            "durata" => "X notti",
            "posti" => "X",
            "resp" => "Responsabile",
            "note" => "Note"
    ));
    };
    echo($json);
?>
