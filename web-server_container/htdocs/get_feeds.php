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

$agency_name = $_GET['agency_name'] ?? '';

$sql = "
SELECT f.feed_id, f.feed_name 
FROM Feed f
JOIN Agency a ON f.agency_id = a.agency_id
WHERE a.agency_name = ?";

$stmt = $conn->prepare($sql);
$stmt->bind_param("s", $agency_name);
$stmt->execute();
$result = $stmt->get_result();

$feeds = [];

if ($result->num_rows > 0) {
    while ($row = $result->fetch_assoc()) {
        $feeds[] = $row;
    }
}

$stmt->close();
$conn->close();

echo json_encode($feeds);
?>
