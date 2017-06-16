<?php
   echo "<center><a href='maandfotosbyage.php?sort=ASC'>gelijke leeftijd steeds ouder</a> | <a href='maandfotosbyage.php?sort=DESC'>steeds jonger</a> | <a href='maandfotosbydate.php?sort=ASC'>op datum oplopend</a> | <a href='maandfotosbydate.php?sort=DESC'>aflopend</a></center><br>";
   class MyDB extends SQLite3
   {
      function __construct()
      {
         $this->open('maandfotos/maandfotos.db');
      }
   }
   $sort = $_GET['sort'];
   if ($sort =="")
   { $sort = "ASC";}
   
   $db = new MyDB();
   if(!$db){
      echo $db->lastErrorMsg();
   } else {
      echo "<table>";
   }

   $sql =<<<EOF
      SELECT * from SORTEDBYAGE order by AGE $sort;
EOF;

   $ret = $db->query($sql);
   while($row = $ret->fetchArray(SQLITE3_ASSOC) ){
      echo "<tr><td>";
      echo $row['AGE'] . " Maanden</td>\n";
      echo "<td align='right'><img src='maandfotos/". $row['FOLDER1'] ."/". $row['FILE1'] ."'></td>";
      echo "<td align='center'><img src='maandfotos/". $row['FOLDER2'] ."/". $row['FILE2'] ."'></td>";
      echo "<td align='left'><img src='maandfotos/". $row['FOLDER3'] ."/". $row['FILE3'] ."'></td>";
      echo "</tr>";
   }
   echo "</table>";
   $db->close();
?>
