<?php
header('Content-Type: application/json');

// データベース接続情報
$servername = "db";
$username = "root";
$password = "password";
$dbname = "operation";

// データベース接続の作成
$conn = new mysqli($servername, $username, $password, $dbname);

if ($conn->connect_error) {
    die(json_encode(['success' => false, 'message' => "Connection failed: " . $conn->connect_error]));
}

$feed_id = $_GET['feed_id'] ?? '';
$entered_password = $_GET['password'] ?? '';

if (!$feed_id || !$entered_password) {
    die(json_encode(['success' => false, 'message' => 'Missing feed_id or password']));
}

// 入力されたパスワードを整数型に変換
$entered_password = intval($entered_password);

$sql = "SELECT password FROM Feed WHERE feed_id = ?";
$stmt = $conn->prepare($sql);
$stmt->bind_param("s", $feed_id);
$stmt->execute();
$result = $stmt->get_result();

if ($result->num_rows === 0) {
    die(json_encode(['success' => false, 'message' => 'Feed not found']));
}

$feed = $result->fetch_assoc();
$stored_password = intval($feed['password']); // データベースから取得したパスワードを整数型に変換

if ($entered_password === $stored_password) {
    echo json_encode(['success' => true]);
} else {
    echo json_encode(['success' => false, 'message' => 'Invalid password']);
}

$stmt->close();
$conn->close();
?>
