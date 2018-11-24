<?php session_start();
switch ($_SERVER['HTTP_ORIGIN']) {
    case 'http://localhost:8000/answer/': case 'https://localhost:8000/answer/':
    header('Access-Control-Allow-Origin: '.$_SERVER['HTTP_ORIGIN']);
    header('Access-Control-Allow-Methods: GET, PUT, POST, DELETE, OPTIONS');
    header('Access-Control-Max-Age: 1000');
    header('Access-Control-Allow-Headers: Content-Type, Authorization, X-Requested-With');
    break;
}
?>
<!doctype html>
<html lang="en" class="no-js">
<body>
	<script src="http://ajax.googleapis.com/ajax/libs/jquery/1.7.1/jquery.min.js" type="text/javascript"></script>
	<script type="text/javascript">
		data = {};
		data['user'] = "<?php echo $_SESSION['user'] ?>";
		data['pass'] = "<?php echo $_SESSION['pass'] ?>";
		console.log(data);
		$.ajax({
		    type: 'POST',
		    url: 'http://localhost:8000/answer/',
		    crossDomain: true,
		    data: JSON.stringify(data, null, '\t'),
		    dataType: 'json',
		    contentType: 'application/json;charset=UTF-8',
		    success: function(responseData) {

		    	console.log(responseData);
		    	if(responseData.attack=="false"){
		    		document.location = 'login-extend.php';
		    	}
		    	else{
		    		alert('Attacked');	
		    	}
		    },
		    error: function (responseData) {
		        alert('POST failed.');
		    }
		});
	</script>
</body>
</html>

