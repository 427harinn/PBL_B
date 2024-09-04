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

// POSTデータを受け取る
$data = json_decode(file_get_contents("php://input"), true);
$currentPassword = intval($data['currentPassword']);
$newPassword = intval($data['newPassword']);
$feed_name = $data['feed_name'];

// `feed_name` に対応する `feed_id` を取得
$sql = "SELECT feed_id, password FROM Feed WHERE feed_name = ?";
$stmt = $conn->prepare($sql);
if (!$stmt) {
    die(json_encode(['success' => false, 'message' => "SQL prepare failed: " . $conn->error]));
}
$stmt->bind_param("s", $feed_name);
$stmt->execute();
$result = $stmt->get_result();

if ($result->num_rows === 0) {
    die(json_encode(['success' => false, 'message' => 'Feed not found']));
}

$feed = $result->fetch_assoc();
$feed_id = $feed['feed_id'];
$storedPassword = intval($feed['password']); // データベースから取得したパスワードをintに変換

// 現在のパスワードが一致するか確認
if ($currentPassword !== $storedPassword) {
    die(json_encode(['success' => false, 'message' => '現在のパスワードが間違っています。']));
}

// 新しいパスワードを更新
$sql = "UPDATE Feed SET password = ? WHERE feed_id = ?";
$stmt = $conn->prepare($sql);
if (!$stmt) {
    die(json_encode(['success' => false, 'message' => "SQL prepare failed: " . $conn->error]));
}
$stmt->bind_param("ii", $newPassword, $feed_id); // intとしてバインド
$success = $stmt->execute();

if ($success) {
    echo json_encode(['success' => true]);
} else {
    echo json_encode(['success' => false, 'message' => 'パスワードの変更に失敗しました。']);
}

$stmt->close();
$conn->close();
?>
