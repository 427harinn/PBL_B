<?php
$servername = "localhost";
$username = "your_username";  // MySQLユーザー名
$password = "your_password";  // MySQLパスワード
$dbname = "bus_info";         // 使用するデータベース名

// データベース接続の作成
$conn = new mysqli($servername, $username, $password, $dbname);

// 接続をチェック
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}

// フロントエンドから送信されたパラメータを受け取る
$date = $_GET['date'];
$city = $_GET['city'];
$municipality = $_GET['municipality'];

// SQLクエリを作成（フィルター条件に応じて調整）
$sql = "
SELECT 
    r.route_name,
    s.status,
    s.note
FROM 
    Route r
JOIN 
    Status s ON r.route_id = s.route_id
JOIN 
    Feed f ON r.feed_id = f.feed_id
JOIN 
    Agency a ON f.agency_id = a.agency_id
WHERE 
    a.agency_name = ? AND f.feed_name = ? AND s.date = ?";

$stmt = $conn->prepare($sql);
$stmt->bind_param("sss", $city, $municipality, $date);
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
header('Content-Type: application/json');
echo json_encode($routes);
?>
