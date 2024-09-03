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

$data = json_decode(file_get_contents('php://input'), true);
$selected_date = $data['date'];
$routes = $data['routes'];

foreach ($routes as $route) {
    $stmt = $conn->prepare("
        INSERT INTO Status (status, date, route_id, note)
        VALUES (?, ?, ?, ?)
        ON DUPLICATE KEY UPDATE
        status = VALUES(status),
        note = VALUES(note)
    ");
    $stmt->bind_param("ssis", $route['status'], $selected_date, $route['route_id'], $route['note']);
    $stmt->execute();
}

$stmt->close();
$conn->close();

echo json_encode(["success" => true]);
?>
