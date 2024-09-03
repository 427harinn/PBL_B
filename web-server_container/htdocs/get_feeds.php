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

// agency_nameを受け取る
$agency_name = $_GET['agency_name'];

// agency_nameに対応するagency_idを取得
$sql = "SELECT agency_id FROM Agency WHERE agency_name = ?";
$stmt = $conn->prepare($sql);
$stmt->bind_param("s", $agency_name);
$stmt->execute();
$result = $stmt->get_result();
$agency = $result->fetch_assoc();
$agency_id = $agency['agency_id'];

$stmt->close();

// SQLクエリを実行してagency_idに関連するフィードを取得
$sql = "SELECT feed_id, feed_name FROM Feed WHERE agency_id = ?";
$stmt = $conn->prepare($sql);
$stmt->bind_param("i", $agency_id);
$stmt->execute();
$result = $stmt->get_result();

$feeds = [];

if ($result->num_rows > 0) {
    while($row = $result->fetch_assoc()) {
        $feeds[] = $row;
    }
}

$stmt->close();
$conn->close();

// 結果をJSON形式で返す
echo json_encode($feeds);
?>
