<?php
session_start();
switch ($_SERVER['HTTP_ORIGIN']) {
    case 'http://localhost:8000/answer/': case 'https://localhost:8000/answer/':
    header('Access-Control-Allow-Origin: '.$_SERVER['HTTP_ORIGIN']);
    header('Access-Control-Allow-Methods: GET, PUT, POST, DELETE, OPTIONS');
    header('Access-Control-Max-Age: 1000');
    header('Access-Control-Allow-Headers: Content-Type, Authorization, X-Requested-With');
    break;
}
include('includes/config.php');
function getRealIpAddr()
{
    if (!empty($_SERVER['HTTP_CLIENT_IP']))   //check ip from share internet
    {
      $ip=$_SERVER['HTTP_CLIENT_IP'];
    }
    elseif (!empty($_SERVER['HTTP_X_FORWARDED_FOR']))   //to check ip is pass from proxy
    {
      $ip=$_SERVER['HTTP_X_FORWARDED_FOR'];
    }
    else
    {
      $ip=$_SERVER['REMOTE_ADDR'];
    }
    return $ip;
}
function getScore($string){
	$score = 0;
	if(preg_match("/(--|%2D%2D|\\/*|*\\/)/", $string)){
		$score++;
	}
	if(preg_match("/('|%27|\\x22|%22)/", $string)){
		$score++;
	}
	if(preg_match("/(;|%3B)/", $string)){
		$score++;
	}
	if(preg_match("/(\\('|%28|\\|%29|@|%40)/", $string)){
		$score++;
	}
	if(preg_match("/(=|%3D)/", $string)){
		$score++;
	}
	return $score;
}
?>

<!doctype html>
<html lang="en" class="no-js">

<head>
	<meta charset="UTF-8">
	<meta http-equiv="X-UA-Compatible" content="IE=edge">
	<meta name="viewport" content="width=device-width, initial-scale=1, minimum-scale=1, maximum-scale=1">
	<meta name="description" content="">
	<meta name="author" content="">

	<title>Car Rental Portal | Admin Login</title>
	<link rel="stylesheet" href="css/font-awesome.min.css">
	<link rel="stylesheet" href="css/bootstrap.min.css">
	<link rel="stylesheet" href="css/dataTables.bootstrap.min.css">
	<link rel="stylesheet" href="css/bootstrap-social.css">
	<link rel="stylesheet" href="css/bootstrap-select.css">
	<link rel="stylesheet" href="css/fileinput.min.css">
	<link rel="stylesheet" href="css/awesome-bootstrap-checkbox.css">
	<link rel="stylesheet" href="css/style.css">
</head>

<body>
	
	<div class="login-page bk-img" style="background-image: url(img/login-bg.jpg);">
		<div class="form-content">
			<div class="container">
				<div class="row">
					<div class="col-md-6 col-md-offset-3">
						<h1 class="text-center text-bold text-light mt-4x">Sign in</h1>
						<div class="well row pt-2x pb-3x bk-light">
							<div class="col-md-8 col-md-offset-2">
								<form id="cname" method="post">

									<label for="" class="text-uppercase text-sm">Your Username </label>
									<input type="text" placeholder="Username" name="username" class="form-control mb">

									<label for="" class="text-uppercase text-sm">Password</label>
									<input type="password" placeholder="Password" name="password" class="form-control mb">

						
									<button class="btn btn-primary btn-block" name="login" type="submit">LOGIN</button>

								</form>
							</div>
						</div>
						<div class="text-center text-light">
							<a href="#" class="text-light">Forgot password?</a>
						</div>
						<?php
							if(isset($_POST['login']))
							{
								$email=$_POST['username'];
								$password=$_POST['password'];
								$_SESSION['user'] = $_POST['username'];
								$_SESSION['pass'] = $_POST['password'];
								$_SESSION['ip'] = getRealIpAddr();
								$_SESSION['port'] = $_SERVER['REMOTE_PORT'];
								$_SESSION['login'] = true;
								$_SESSION['user_score'] = getScore($_SESSION['user']);
								$_SESSION['pass_score'] = getScore($_SESSION['pass']);
								$str = preg_split("/(\s|=|@|'|,|--|\\)|\\(|;)/", strtolower($_SESSION['user']));
								$str_p = preg_split("/(\s|=|@|'|,|--|\\)|\\(|;)/", strtolower($_SESSION['pass']));
								for($i=0;$i<count($str);$i++){
									$temp = md5($str[$i]);
									$str[$i] = $temp;
								}
								$_SESSION['user_hash'] = implode(' ', $str);
								for($i=0;$i<count($str_p);$i++){
									$temp = md5($str_p[$i]);
									$str_p[$i] = $temp;
								}
								$_SESSION['pass_hash'] = implode(' ', $str_p);
							}
							else{
								$_SESSION['login'] = false;
							}
						?>
					</div>
				</div>
			</div>
		</div>
	</div>
	
	<!-- Loading Scripts -->
	<script src="js/jquery.min.js"></script>
	<script src="js/bootstrap-select.min.js"></script>
	<script src="js/bootstrap.min.js"></script>
	<script src="js/jquery.dataTables.min.js"></script>
	<script src="js/dataTables.bootstrap.min.js"></script>
	<script src="js/Chart.min.js"></script>
	<script src="js/fileinput.js"></script>
	<script src="js/chartData.js"></script>
	<script src="js/main.js"></script>

	<script type="text/javascript">
		data = {};
		data['ip'] = "<?php echo $_SESSION['ip'] ?>";
		data['port'] = "<?php echo $_SESSION['port'] ?>";
		data['user'] = "<?php echo $_SESSION['user_hash'] ?>";
		data['user_score'] = "<?php echo $_SESSION['user_score'] ?>";
		data['pass'] = "<?php echo $_SESSION['pass_hash'] ?>";
		data['pass_score'] = "<?php echo $_SESSION['pass_score'] ?>";	
		console.log(data);
		if(<?php echo $_SESSION['login'] ?> == 1){
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
			    		<?php 	
				    		$sql ="SELECT UserName, Password FROM admin WHERE UserName='{$_SESSION['user']}' and Password=md5('{$_SESSION['pass']}')";
							$result = mysqli_query($dbh,$sql);
							$ret = mysqli_num_rows($result);
							if($ret)
							{
								$_SESSION['alogin']=$_SESSION['user'];
								echo "document.location = 'dashboard.php';";
							} else{
							  echo "alert('Invalid Details');";
							}
			    		?>
			    	}
			    	else{
			    		alert('Attacked');	
			    	}
			    },
			    error: function (responseData) {
			        alert('POST failed.');
			    }	
			});
		};
	</script>

</body>

</html>