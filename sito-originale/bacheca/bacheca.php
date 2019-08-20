<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html><head>

  
  <meta content="text/html; charset=ISO-8859-1" http-equiv="content-type"><title>CAI Sovico Informazioni</title></head><body>
<table style="text-align: left; width: 800px; margin-left: auto; margin-right: auto; height: 409px; color: rgb(0, 102, 0); font-family: Helvetica,Arial,sans-serif;" border="0" cellpadding="0" cellspacing="0">

  <tbody>
    <tr>
      <td colspan="2" rowspan="1" style="vertical-align: top; height: 200px; width: 601px;"><a href="../index.html"><img style="border: 0px solid ; width: 800px; height: 200px;" alt="Page Banner go to Home" src="../foto/pagebanner.jpg"></a> </td>
    </tr>
    <tr>
      <td style="vertical-align: top; height: 202px; width: 200px;"><img src="../foto/ico-bacheca.jpg" style="width: 200px; height: 200px;" alt="La bacheca del CAI"> <br>
      </td>
      <td style="vertical-align: top; height: 202px; width: 600px; text-align: center;"><big><big><big><br>
Ultime Notizie<br>
Prossime Iniziative<br>
      <br>
      </td>
    </tr>
  </tbody>
</table>


<table style="text-align: left; width: 800px; height: 600px; margin-left: auto; margin-right: auto; color: rgb(0, 0, 0); font-family: Helvetica,Arial,sans-serif;" background="bachecavuota.jpg" border="0" cellpadding="0" cellspacing="0">

  <tbody>
<tr>
      <td colspan="7" rowspan="1" style="height: 145px; width: 787px;"></td>
</tr>
<tr>
      <td style="height: 55px; width: 99px;"></td>
      <td style="height: 55px; width: 157px;"></td>
      <td style="height: 55px; width: 50px;"></td>
      <td colspan="1" rowspan="2" style="font-family: Comic Sans MS ;text-align: center; height: 55px; width: 141px; color: rgb(0, 0, 255);"><big><i>
                <?php
            	$handle = fopen("filepostit1.txt" ,"rb");		$contiene = fread($handle,filesize("filepostit1.txt"));	fclose($handle);
            	$contiene = str_replace("\r","<br>",$contiene);  echo $contiene;
				?>
		</big></big></i></td>
      <td style="height: 55px; width: 32px;"></td>
      <td style="text-align: center; height: 55px; width: 256px;"><big><big>
                <?php
            	$handle = fopen("filetitolo.txt" ,"rb");		$contiene = fread($handle,filesize("filetitolo.txt"));	fclose($handle);
            	echo $contiene;
				?>
	   </big></td>
	  <td style="height: 55px; width: 52px;"></td>
</tr>
<tr>
      <td style="height: 77px; width: 99px;"></td>
      <td style="height: 77px; width: 157px; text-align: center;"><a href="archiviocom.pdf"><img style="border: 0px solid ; width: 150px; height: 70px;" alt="Clicca per le comunicazioni ai soci" src="cliccaarchivio.jpg"></a><br></td>
      <td style="height: 77px; width: 50px;"></td>
      <td style="height: 77px; width: 32px;"></td>
      <td colspan="1" rowspan="3" style="text-align: justify;height: 92px; width: 256px;">
                <?php
            	$handle = fopen("filemanifesto.txt" ,"rb");		$contiene = fread($handle,filesize("filemanifesto.txt"));	fclose($handle);
            	$contiene = str_replace("\r","<br>",$contiene);  echo $contiene;
				?>
</td>
      <td style="height: 77px; width: 52px;"></td>
</tr>
<tr>
      <td style="height: 94px; width: 99px;"></td>
      <td style="height: 94px; width: 157px;"></td>
      <td style="height: 94px; width: 50px;"></td>
      <td style="height: 94px; width: 141px;"></td>
      <td style="height: 94px; width: 32px;"></td>
      <td style="height: 94px; width: 52px;"></td>
</tr>
<tr>
      <td style="height: 92px; width: 99px;"></td>
      <td colspan="1" rowspan="2" style="font-family: Comic Sans MS ;text-align: center; height: 92px; width: 141px;"><a Style="text-decoration: none ; color: rgb(0,0,0);" href="locandina.pdf"><big><i>

               <?php
            	$handle = fopen("titololocandina.txt" ,"rb");		$contiene = fread($handle,filesize("titololocandina.txt"));	fclose($handle);
            	$contiene = str_replace("\r","<br>",$contiene);  echo $contiene;
				?> 
	  </big></i></td></td> 
      <td style="height: 92px; width: 50px;"></td>
      <td colspan="1" rowspan="2" style="font-family: Comic Sans MS ;text-align: center; height: 92px; width: 141px; color: rgb(0, 0, 255);"><big><i>  
                <?php
            	$handle = fopen("filepostit2.txt" ,"rb");		$contiene = fread($handle,filesize("filepostit2.txt"));	fclose($handle);
            	$contiene = str_replace("\r","<br>",$contiene);  echo $contiene;
				?>
	  </big></i></td> 
      <td style="height: 92px; width: 32px;"></td>
      <td style="height: 92px; width: 52px;"></td>
</tr>
<tr>
      <td style="height: 39px; width: 99px; "></td>
      <td style="height: 39px; width: 50px;"></td>
      <td style="height: 39px; width: 32px;"></td>
      <td colspan="1" rowspan="2" style="text-align: center; vertical-align: top; height: 39px; width: 256px;">
					<a href="manifestone.php"><img border="0" style="width: 100px; height: 72px;" alt="Foto 1 manifesto" src="fotomanifesto1.jpg"></a>&nbsp;&nbsp;&nbsp;&nbsp; 
					<a href="manifestone.php"><img border="0" style="width: 100px; height: 70px;" alt="Foto 2 manifesto" src="fotomanifesto2.jpg"></a></td>
      <td style="height: 39px; width: 52px; "></td>
</tr>
<tr>
      <td style="height: 98px; width: 99px;"></td>
      <td style="height: 98px; width: 157px;"></td>
      <td style="height: 98px; width: 50px;"></td>
      <td style="height: 98px; width: 141px;"></td>
      <td style="height: 98px; width: 32px;"></td>
      <td style="height: 98px; width: 52px;"></td>

</tr>
</tbody>
</table>


</body></html>
