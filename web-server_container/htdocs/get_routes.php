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
    die(json_encode(['error' => "Connection failed: " . $conn->connect_error]));
}

// フロントエンドから送信された feed_id を取得
$feed_id = $_GET['feed_id'] ?? '';

if (!$feed_id) {
    die(json_encode(['error' => 'Missing feed_id']));
}

// SQLクエリを実行して選択された feed_id に関連するルート情報を取得
$sql = "SELECT route_id, route_name FROM Route WHERE feed_id = ?";
$stmt = $conn->prepare($sql);
$stmt->bind_param("s", $feed_id);
$stmt->execute();
$result = $stmt->get_result();

$routes = [];

if ($result->num_rows > 0) {
    while($row = $result->fetch_assoc()) {
        $routes[] = $row;
    }
}

$stmt->close();
$conn->close();

// 結果をJSON形式で返す
echo json_encode($routes);
?>
