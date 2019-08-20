<html><head>
  <meta content="text/html; charset=ISO-8859-1" http-equiv="content-type"><title>CAI Sovico Informazioni</title></head><body>
<table style="text-align: left; width: 800px; margin-left: auto; margin-right: auto; height: 300px; color: rgb(0, 102, 0); font-family: Helvetica,Arial,sans-serif;" border="0" cellpadding="0" cellspacing="0">

  <tbody>
    <tr>
      <td colspan="1" rowspan="1" style="vertical-align: top; height: 200px; width: 601px;"><a href="../index.html"><img style="border: 0px solid ; width: 800px; height: 200px;" alt="Page Banner go to Home" src="../foto/pagebanner.jpg"></a> </td>
    </tr><tr>
      <td style="vertical-align: center;text-align: center"><big><big><b>RISULTATI DEI TRASFERIMENTI</b></big></big><br>
      </td>
    </tr>

 </tbody>
</table>

<table style="text-align: left; text-align: center; width: 800px ; height:100px ; margin-left: auto; margin-right: auto; color: rgb(0, 102, 0); font-family: Arial;" border="1" cellpadding="0" cellspacing="0">
<tbody>


<?php

if(strlen($_POST['postit1'])==0){echo"<tr><td>Post-It 1 = Nessuna variazione</td></tr>";}
else{ echo "<tr><td>Post-It 1 =<b> $_POST[postit1]</b></tr></td>";
$nomefile=fopen("..//bacheca/filepostit1.txt" , "w");
fwrite ($nomefile,$_POST['postit1']);
fclose($nomefile);
 }
 
if(strlen($_POST['postit2'])==0){echo"<tr><td>Post-It 2 = Nessuna variazione</td></tr>";}
else{ echo "<tr><td>Post-It 2 =<b> $_POST[postit2]</b></td></tr>";
$nomefile=fopen("..//bacheca/filepostit2.txt" , "w");
fwrite ($nomefile,$_POST['postit2']);
fclose($nomefile);
 } 
 
 if(strlen($_POST['titolo'])==0){echo"<tr><td>Titolo Manifesto = Nessuna variazione</td></tr>";}
else{ echo "<tr><td>Titolo Manifesto =<b> $_POST[titolo]</b></td></tr>";
$nomefile=fopen("..//bacheca/filetitolo.txt" , "w");
fwrite ($nomefile,$_POST['titolo']);
fclose($nomefile);
 } 
 
 if(strlen($_POST['manifesto'])==0){echo"<tr><td>Testo Manifesto = Nessuna variazione</td></tr>";}
else{ echo "<tr><td>Testo Manifesto = <br>$_POST[manifesto]</td></tr>";
$nomefile=fopen("..//bacheca/filemanifesto.txt" , "w");
fwrite ($nomefile,$_POST['manifesto']);
fclose($nomefile);
 } 



//-------------------------------  ELABORA FOTO 1  ----------------------------------
//echo "nome loc create: {$_FILES['foto1']['name']}<br>";  
//echo "nome type: {$_FILES['foto1']['type']}<br>"; 
//echo "none temp name: {$_FILES['foto1']['tmp_name']}<br>";
//echo "errori ??: {$_FILES['foto1']['error']}<br>";
//echo "dimensione in byte: {$_FILES['foto1']['size']}<br>";

list($width, $height, $type, $attr) = getimagesize($_FILES['foto1']['tmp_name']);

    // Controllo se esiste un file in UpLoad
  if ($_FILES['foto1']['name'] == "" )  {
          echo "<tr><td>Nessun file in immagine 1 da trasferire</tr></td>";
 	}
    // Controllo che il file non superi i 4 MB
  elseif ($_FILES['foto1']['size'] > 4194304) {
          echo "<tr><td>File troppo grande, non deve superare 4MB !!</tr></td>";
        }
    // Controllo che il file sia in uno dei formato JPG
  elseif ($type!=2) {
          echo "<tr><td>Formato errato, il file deve essere in JPG !!</tr></td>";
        }
    // lo copia in una nuova posizione
  elseif (copy($_FILES['foto1']['tmp_name'], "..//bacheca/fotomanifesto1.jpg"))  {
          echo "<tr><td>Invio del file <b>   {$_FILES['foto1']['name']} </b> In foto 1   Riuscito</tr></td>";
             // cancella il file temporaneo
             unlink(($_FILES['foto1']['tmp_name']));
        } 
   else {
         echo "<tr><td>Invio del file immagine 1 fallito</tr></td>";
        }


//-------------------------------  ELABORA FOTO 2  ----------------------------------
//echo "nome loc create: {$_FILES['foto2']['name']}<br>";  
//echo "nome type: {$_FILES['foto2']['type']}<br>"; 
//echo "none temp name: {$_FILES['foto2']['tmp_name']}<br>";
//echo "errori ??: {$_FILES['foto2']['error']}<br>";
//echo "dimensione in byte: {$_FILES['foto2']['size']}<br>";

list($width, $height, $type, $attr) = getimagesize($_FILES['foto2']['tmp_name']);

    // Controllo se esiste un file in UpLoad
  if ($_FILES['foto2']['name'] == "" )  {
          echo "<tr><td>Nessun file in immagine 2 da trasferire</tr></td>";
 	}
    // Controllo che il file non superi i 4 MB
  elseif ($_FILES['foto2']['size'] > 4194304) {
          echo "<tr><td>File 2 troppo grande, non deve superare 4MB !!</tr></td>";
        }
    // Controllo che il file sia in uno dei formato JPG
  elseif ($type!=2) {
          echo "<tr><td>Formato errato, il file 2 deve essere in JPG !!</tr></td>";
        }
    // lo copia in una nuova posizione
  elseif (copy($_FILES['foto2']['tmp_name'], "..//bacheca/fotomanifesto2.jpg"))  {
          echo "<tr><td>Invio del file <b>   {$_FILES['foto2']['name']} </b> In foto 2   Riuscito</tr></td>";
             // cancella il file temporaneo
             unlink(($_FILES['foto2']['tmp_name']));
        } 
   else {
         echo "<tr><td>Invio del file immagine 2 fallito</tr></td>";
        }


//-------------------------------  ELABORA FOTO 3  ----------------------------------
//echo "nome loc create: {$_FILES['foto3']['name']}<br>";  
//echo "nome type: {$_FILES['foto3']['type']}<br>"; 
//echo "none temp name: {$_FILES['foto3']['tmp_name']}<br>";
//echo "errori ??: {$_FILES['foto3']['error']}<br>";
//echo "dimensione in byte: {$_FILES['foto3']['size']}<br>";

list($width, $height, $type, $attr) = getimagesize($_FILES['foto3']['tmp_name']);


    // Controllo se esiste un file in UpLoad
  if ($_FILES['foto3']['name'] == "" )  {
          echo "<tr><td>Nessun file in immagine 3 da trasferire</tr></td>";
 	}
    // Controllo che il file non superi i 4 MB
  elseif ($_FILES['foto3']['size'] > 4194304) {
          echo "<tr><td>File 3 troppo grande, non deve superare 4MB !!</tr></td>";
        }
    // Controllo che il file sia in uno dei formato JPG
  elseif ($type!=2) {
          echo "<tr><td>Formato errato, il file deve essere in JPG !!</tr></td>";
        }
    // lo copia in una nuova posizione
  elseif (copy($_FILES['foto3']['tmp_name'], "..//bacheca/fotomanifesto3.jpg"))  {
          echo "<tr><td>Invio del file <b>   {$_FILES['foto3']['name']} </b> In foto 3   Riuscito</tr></td>";
             // cancella il file temporaneo
             unlink(($_FILES['foto3']['tmp_name']));
        } 
   else {
         echo "<tr><td>Invio del file immagine 3 fallito</tr></td>";
        }


//-------------------------------  ELABORA FOTO 4  ----------------------------------
//echo "nome loc create: {$_FILES['foto4']['name']}<br>";  
//echo "nome type: {$_FILES['foto4']['type']}<br>"; 
//echo "none temp name: {$_FILES['foto4']['tmp_name']}<br>";
//echo "errori ??: {$_FILES['foto4']['error']}<br>";
//echo "dimensione in byte: {$_FILES['foto4']['size']}<br>";

list($width, $height, $type, $attr) = getimagesize($_FILES['foto4']['tmp_name']);


    // Controllo se esiste un file in UpLoad
  if ($_FILES['foto4']['name'] == "" )  {
          echo "<tr><td>Nessun file in immagine 4 da trasferire</tr></td>";
 	}
    // Controllo che il file non superi i 4 MB
  elseif ($_FILES['foto4']['size'] > 4194304) {
          echo "<tr><td>File 4 troppo grande, non deve superare 4MB !!</tr></td>";
        }
    // Controllo che il file sia in uno dei formato JPG
  elseif ($type!=2) {
          echo "<tr><td>Formato errato, il file deve essere in JPG !!</tr></td>";
        }
    // lo copia in una nuova posizione
  elseif (copy($_FILES['foto4']['tmp_name'], "..//bacheca/fotomanifesto4.jpg"))  {
          echo "<tr><td>Invio del file <b>   {$_FILES['foto4']['name']} </b> In foto 4   Riuscito</tr></td>";
             // cancella il file temporaneo
             unlink(($_FILES['foto4']['tmp_name']));
        } 
   else {
         echo "<tr><td>Invio del file immagine 4 fallito</tr></td>";
        }

//-------------------------------  ELABORA FOTO 5  ----------------------------------
//echo "nome loc create: {$_FILES['foto5']['name']}<br>";  
//echo "nome type: {$_FILES['foto5']['type']}<br>"; 
//echo "none temp name: {$_FILES['foto5']['tmp_name']}<br>";
//echo "errori ??: {$_FILES['foto5']['error']}<br>";
//echo "dimensione in byte: {$_FILES['foto5']['size']}<br>";

list($width, $height, $type, $attr) = getimagesize($_FILES['foto5']['tmp_name']);


    // Controllo se esiste un file in UpLoad
  if ($_FILES['foto5']['name'] == "" )  {
          echo "<tr><td>Nessun file in immagine 5 da trasferire</tr></td>";
 	}
    // Controllo che il file non superi i 4 MB
  elseif ($_FILES['foto5']['size'] > 4194304) {
          echo "<tr><td>File 5 troppo grande, non deve superare 4MB !!</tr></td>";
        }
    // Controllo che il file sia in uno dei formato JPG
  elseif ($type!=2) {
          echo "<tr><td>Formato errato, il file deve essere in JPG !!</tr></td>";
        }
    // lo copia in una nuova posizione
  elseif (copy($_FILES['foto5']['tmp_name'], "..//bacheca/fotomanifesto5.jpg"))  {
          echo "<tr><td>Invio del file <b>   {$_FILES['foto5']['name']} </b> In foto 5   Riuscito</tr></td>";
             // cancella il file temporaneo
             unlink(($_FILES['foto5']['tmp_name']));
        } 
   else {
         echo "<tr><td>Invio del file immagine 5 fallito</tr></td>";
        }


 if(strlen($_POST['titololocandina'])==0){echo"<tr><td>Titolo Locandina = Nessuna variazione</td></tr>";}
else{ echo "<tr><td>Titolo Locandina = <br>$_POST[titololocandina]</td></tr>";
$nomefile=fopen("..//bacheca/titololocandina.txt" , "w");
fwrite ($nomefile,$_POST['titololocandina']);
fclose($nomefile);
 } 

//-------------------------------  ELABORA FILE LOCANDINA  ----------------------------------
//echo "nome loc create: {$_FILES['locandina']['name']}<br>";  
//echo "nome type: {$_FILES['locandina']['type']}<br>"; 
//echo "none temp name: {$_FILES['locandina']['tmp_name']}<br>";
//echo "errori ??: {$_FILES['locandina']['error']}<br>";
//echo "dimensione in byte: {$_FILES['locandina']['size']}<br>";

list($width, $height, $type, $attr) = getimagesize($_FILES['locandina']['tmp_name']);


    // Controllo se esiste un file in UpLoad
  if ($_FILES['locandina']['name'] == "" )  {
          echo "<tr><td>Nessun file in file locandina da trasferire</tr></td>";
 	}
    // Controllo che il file non superi i 4 MB
  elseif ($_FILES['locandina']['size'] > 4194304) {
          echo "<tr><td>File 5 troppo grande, non deve superare 4MB !!</tr></td>";
        }
    // Controllo che il file sia in uno dei formato PDF
//  elseif ($type!=2) {
//          echo "<tr><td>Formato errato, il file deve essere in PDF? !!</tr></td>";
//        }
    // lo copia in una nuova posizione
  elseif (copy($_FILES['locandina']['tmp_name'], "..//bacheca/locandina.pdf"))  {
          echo "<tr><td>Invio del file <b>   {$_FILES['locandina']['name']} </b> In File Locandina   Riuscito</tr></td>";
             // cancella il file temporaneo
             unlink(($_FILES['locandina']['tmp_name']));
        } 
   else {
         echo "<tr><td>Invio del file immagine 5 fallito</tr></td>";
        }


// echo "fine file"

?>

</tbody>
</table>
