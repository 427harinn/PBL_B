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

// フロントエンドから送信されたデータを取得
$date = $_GET['date'] ?? '';
$city = $_GET['city'] ?? '';
$municipality = $_GET['municipality'] ?? '';

// SQLクエリを実行して路線情報を取得
$sql = "SELECT route_name, status, note 
        FROM Status 
        JOIN Route ON Status.route_id = Route.route_id 
        JOIN Agency ON Route.agency_id = Agency.agency_id 
        WHERE Agency.agency_name = ? AND Status.date = ?";

$stmt = $conn->prepare($sql);
$stmt->bind_param("ss", $city, $date);
$stmt->execute();
$result = $stmt->get_result();

$routes = [];

if ($result->num_rows > 0) {
    while($row = $result->fetch_assoc()) {
        $routes[] = [
            'route_name' => $row['route_name'],
            'status' => $row['status'] == 1 ? '運行中' : '運休',
            'note' => $row['note']
        ];
    }
}

$stmt->close();
$conn->close();

// 結果をJSON形式で返す
echo json_encode($routes);
?>
