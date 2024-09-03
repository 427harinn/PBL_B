<?php
header('Content-Type: application/json');

// データベース接続情報
$servername = "db";
$username = "root";
$password = "password";
$dbname = "operation";

// データベース接続の作成
$conn = new mysqli($servername, $username, $password, $dbname);

// 接続をチェック
if ($conn->connect_error) {
    die(json_encode(['success' => false, 'message' => "Connection failed: " . $conn->connect_error]));
}

// フロントエンドから送信されたfeed_idとpasswordを取得
$feed_id = $_GET['feed_id'] ?? '';
$password = $_GET['password'] ?? '';

if (!$feed_id || !$password) {
    die(json_encode(['success' => false, 'message' => 'Missing parameters']));
}

// SQLクエリを実行して、パスワードを検証
$sql = "SELECT password FROM Feed WHERE feed_id = ?";
$stmt = $conn->prepare($sql);
$stmt->bind_param("s", $feed_id);
$stmt->execute();
$result = $stmt->get_result();

if ($result->num_rows > 0) {
    $row = $result->fetch_assoc();
    if ($row['password'] === $password) {
        echo json_encode(['success' => true]);
    } else {
        echo json_encode(['success' => false, 'message' => 'Invalid password']);
    }
} else {
    echo json_encode(['success' => false, 'message' => 'Feed not found']);
}

$stmt->close();
$conn->close();
?>
