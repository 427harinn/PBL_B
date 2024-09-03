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

// SQLクエリを実行してagency_nameを取得
$sql = "SELECT agency_name FROM Agency";
$result = $conn->query($sql);

$agencies = [];

if ($result->num_rows > 0) {
    while($row = $result->fetch_assoc()) {
        $agencies[] = $row['agency_name'];
    }
} else {
    $agencies = [];
}

$conn->close();

// 結果をJSON形式で返す
echo json_encode($agencies);
?>
