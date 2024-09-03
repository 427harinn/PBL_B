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

// クエリパラメータとして渡されたagency_nameを取得
$agency_name = $_GET['agency_name'] ?? '';

if ($agency_name) {
    // SQLクエリを実行してagency_nameに対応するfeed_nameを取得
    $sql = "SELECT feed_name FROM Feed WHERE agency_id = (SELECT agency_id FROM Agency WHERE agency_name = ?)";
    $stmt = $conn->prepare($sql);
    $stmt->bind_param("s", $agency_name);
    $stmt->execute();
    $result = $stmt->get_result();

    $feeds = [];

    if ($result->num_rows > 0) {
        while($row = $result->fetch_assoc()) {
            $feeds[] = $row['feed_name'];
        }
    }

    $stmt->close();
    $conn->close();

    // 結果をJSON形式で返す
    echo json_encode($feeds);
} else {
    echo json_encode(['error' => 'agency_name not provided']);
}
?>
