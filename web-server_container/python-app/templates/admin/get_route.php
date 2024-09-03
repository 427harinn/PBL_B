<?php
phpinfo();
?>

<?php
header('Content-Type: application/json');

// データベース接続設定
$servername = "localhost";
$username = "root";
$password = "password";
$dbname = "operation";

$conn = new mysqli($servername, $username, $password, $dbname);

// 接続をチェック
if ($conn->connect_error) {
    die(json_encode(['error' => "Connection failed: " . $conn->connect_error]));
}

$feed_id = $_GET['feed_id'] ?? '';

$sql = "
SELECT r.route_id, r.route_name 
FROM Route r
WHERE r.feed_id = ?";

$stmt = $conn->prepare($sql);
$stmt->bind_param("s", $feed_id);
$stmt->execute();
$result = $stmt->get_result();

$routes = [];

if ($result->num_rows > 0) {
    while ($row = $result->fetch_assoc()) {
        $routes[] = $row;
    }
}

$stmt->close();
$conn->close();

echo json_encode($routes);
?>
