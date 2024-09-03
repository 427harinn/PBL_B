<?php
// エラー表示をオンにする
error_reporting(E_ALL);
ini_set('display_errors', 1);

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
    die(json_encode(['error' => "Connection failed: " . $conn->connect_error]));
}

// パラメータを受け取る
$date = $_GET['date'] ?? '';
$feed_name = $_GET['feed_name'] ?? '';

if (!$date || !$feed_name) {
    die(json_encode(['error' => 'Missing date or feed_name']));
}

// `feed_name` に対応する `feed_id` を取得
$sql = "SELECT feed_id FROM Feed WHERE feed_name = ?";
$stmt = $conn->prepare($sql);
if (!$stmt) {
    die(json_encode(['error' => "SQL prepare failed: " . $conn->error]));
}
$stmt->bind_param("s", $feed_name);
$stmt->execute();
$result = $stmt->get_result();

if ($result->num_rows === 0) {
    die(json_encode(['error' => 'Feed not found']));
}

$feed = $result->fetch_assoc();
$feed_id = $feed['feed_id'];

// `feed_id` と `date` に基づいて `status` テーブルを検索
$sql = "SELECT r.route_name, s.status, s.comment FROM Status s JOIN Route r ON s.route_id = r.route_id WHERE s.date = ? AND r.feed_id = ?";
$stmt = $conn->prepare($sql);
if (!$stmt) {
    die(json_encode(['error' => "SQL prepare failed: " . $conn->error]));
}
$stmt->bind_param("si", $date, $feed_id);
$stmt->execute();
$result = $stmt->get_result();

$routes = [];

if ($result->num_rows > 0) {
    while($row = $result->fetch_assoc()) {
        $routes[] = [
            'route_name' => $row['route_name'],
            'status' => $row['status'] === 1 ? '運行中' : '運休',
            'comment' => $row['comment']
        ];
    }
}

$stmt->close();
$conn->close();

// 結果をJSON形式で返す
echo json_encode($routes);
?>
