<?php
if ($only){
		
		echo $name;
		$searchData = preg_split("/\s+/", $name);
		print_r($searchData);
	//$NewString1 = preg_split("/[\s,]+/", "Welcome to Wibibi.Have a good day.");

		$sql = "SELECT * FROM wei_yeardata WHERE";
	//	$include_words = array_values(preg_grep("/^[^-].*/", explode(" ", $wei_names))); 
	//	$include_events = array_values(preg_grep("/^[^-].*/", explode(" ", $events))); 
		
		//$sql = $sql." ".multiSearch($wei_names, "wei_name");
		if($searchData)
		{
			$sql = $sql." AND ".multiSearch($events, "searchData");
		}		

		echo 
	//	$sql = $sql."".timesearch($SearchTimeMin,$SearchTimeMax);
	//	$result = mysql_query($sql, $link);				
	//	$goback = "ClickData.php?".searchmodelocate($SearchMode)."&name=$name&only=true".timelocate($SearchTimeMin,$SearchTimeMax);
	

	}else if ($sim){
		echo ">> get in if";
		$sql = 'SELECT * FROM IISR.wei_yeardata WHERE (text REGEXP ">[^\<]*'.$name.'[^\>]*</W>")'.timesearch($SearchTimeMin,$SearchTimeMax);
		$result = mysql_query($sql, $con);
		$goback = "search.php?".searchmodelocate($SearchMode)."&name=$name&sim=true".timelocate($SearchTimeMin,$SearchTimeMax);	
	}else{;}

function multiSearch($searchText, $mode)
	{
		$sql = "";

		$finalData = preg_split("/\s+/", $searchText);
		for($i=0; $i<count($finalData); ++$i)
		{
			if($mode == "wei_name")
			{
				$sql = $sql." text LIKE '%>$include_words[$i]</W>%'";
			}
			elseif ($mode == "searchData") 
			{
				echo $finalData[$i];
				$sql = $sql.' text  REGEXP \'>[^\<]*'.$finalData[$i].'[^\>]*\'';					
			}

			if($i+1 < count($include_words))
			{
				$sql = $sql." AND";
			}
		}
				
		$except_words = array_values(preg_grep("/^-.*/", explode(" ", $searchText)));
		if(count($include_words) > 0 && count($except_words) > 0)
		{
			$sql = $sql." AND";
		}
		for($i=0; $i<count($except_words); ++$i)
		{
			$except_word = str_replace("-", "", $except_words[$i]);
			if($mode == "wei_name")
			{
				$sql = $sql." text NOT LIKE '%>$except_word</W>%'";
			}
			elseif ($mode == "event") 
			{
				$sql = $sql.' text  NOT REGEXP \'>[^\<]*'.$except_word.'[^\>]*\'';
			}

			if($i+1 < count($except_words))
			{
				$sql = $sql." AND";
			}
		}

		return $sql;
	}

?>
