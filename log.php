<html>
    <head>
        <meta charset="utf-8">
        <meta http-equiv="refresh" content = "5"> 
    </head>
    <body>
        <?php
            $fp = file("out.log");
            if ($fp) {
                for($i = count($fp) - 1;$i >= 0; $i --) 
                echo $fp[$i]."<br>";
            }
        ?>
    </body>
</html>

