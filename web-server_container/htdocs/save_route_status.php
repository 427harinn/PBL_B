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

// フロントエンドから送信されたデータを受け取る
$data = json_decode(file_get_contents("php://input"), true);
$date = $data['date'];
$routes = $data['routes'];

// 各ルートの情報を`Status`テーブルに保存
$executed_sql_queries = []; // 実行されたSQLクエリを保存する配列

foreach ($routes as $route) {
    $status = $route['status'] === 'normal' ? 1 : 0;
    $route_id = $route['route_id'];
    $comment = $route['note'];

    // SQLクエリを作成
    $sql = "INSERT INTO Status (status, date, route_id, comment) VALUES (?, ?, ?, ?)
            ON DUPLICATE KEY UPDATE status = VALUES(status), comment = VALUES(comment)";
    
    // SQLステートメントの準備
    $stmt = $conn->prepare($sql);
    if ($stmt === false) {
        die(json_encode(['success' => false, 'message' => "SQL prepare failed: " . $conn->error]));
    }

    // パラメータをバインド
    $stmt->bind_param("isis", $status, $date, $route_id, $comment);

    // 実行されるSQLクエリを可視化するためにSQLステートメントを保存する
    $prepared_sql = sprintf(
        "INSERT INTO Status (status, date, route_id, comment) VALUES (%d, '%s', %d, '%s')
         ON DUPLICATE KEY UPDATE status = %d, comment = '%s'",
        $status, $date, $route_id, $conn->real_escape_string($comment), $status, $conn->real_escape_string($comment)
    );
    
    $executed_sql_queries[] = $prepared_sql; // 実行されたSQLを配列に保存

    // SQLステートメントを実行
    $stmt->execute();
    $stmt->close();
}

$conn->close();

// 成功のレスポンスとともに実行されたSQLクエリを返す
echo json_encode(['success' => true, 'executed_sql' => $executed_sql_queries]);
?>
