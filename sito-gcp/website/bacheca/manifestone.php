<!DOCTYPE html PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html><head>

  <meta content="text/html; charset=ISO-8859-1" http-equiv="content-type"><title>CAI Sovico Bacheca - Il Manifesto in Grande</title></head><body>
<table style="text-align: left; width: 800px; margin-left: auto; margin-right: auto; height: 203px;" border="0" cellpadding="0" cellspacing="0">

  <tbody>
    <tr>
      <td colspan="2" rowspan="1" style="vertical-align: top; height: 200px; width: 800px;"><a href="../index.html"><img style="border: 0px solid ; width: 800px; height: 200px;" alt="Page Banner go to Home" src="../foto/pagebanner.jpg"></a></td>
    </tr>
    <tr>
      <td colspan="1" rowspan="2" style="vertical-align: top; height: 200px; width: 200px;"><img src="../foto/ico-bacheca.jpg" style="width: 200px; height: 200px;" alt="Bacheca del CAI"></td>
      <td style="vertical-align: top; height: 50px; width: 600px; text-align: right;"><a href="bacheca.php"><img style="border: 0px solid ; width: 62px; height: 47px;" alt="Back" src="../foto/freccia_blu_back.jpg"></a>&nbsp; <br>
      </td>
    </tr>
    <tr>
      <td style="vertical-align: top; width: 600px; height: 150px; text-align: center; color: rgb(0, 102, 0);font-family: Helvetica,Arial,sans-serif;">
      <big><big><big>Manifesto<br><br><br>
	  <span style="color: rgb(0, 0, 0); font-family: Helvetica,Arial,sans-serif;"></span>
				
				<?php
            	$handle = fopen("filetitolo.txt" ,"rb");		$contiene = fread($handle,filesize("filetitolo.txt"));	fclose($handle);
            	echo $contiene;
				?>
	  
	  </big></big></big><br>
     </td> 
    </tr>
  </tbody>
</table>
<br>
<table style="text-align: left; width: 800px;font-family: Helvetica,Arial,sans-serif; margin-left: auto; margin-right: auto; " border="0" cellpadding="0" cellspacing="0">
<tbody>
  <tr>
    <td style="vertical-align: top;  width: 800px; height: 80px;">
				
				<?php
            	$handle = fopen("filemanifesto.txt" ,"rb");		$contiene = fread($handle,filesize("filemanifesto.txt"));	fclose($handle);
            	echo $contiene;
				?>
  
	</td>  
  </tr>
  <tr>
      <td style="vertical-align: top;  width: 800px;">
			<!--                     parte per caricare la pagina del slide show -->

			<div align="center"><iframe src="slidezp-manifesto.htm" width="815" height="645" name="frames" frameborder="0" marginheight="0" marginwidth="0" scrolling="No"></iframe></div>

			<!--                               fine introduzione --><!-- origonale riga sopra w615 h490 -->

	  </td>
  </tr>
</tbody>
</table>
