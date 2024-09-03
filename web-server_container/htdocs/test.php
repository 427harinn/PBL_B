<?php
$servername = "localhost";
$username = "root";
$password = "password"; // あなたのMySQLパスワードに置き換えてください

// mysqliを使ってデータベースに接続します
$conn = new mysqli($servername, $username, $password);

// 接続が成功したか確認します
if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
} else {
    echo "Successfully connected to MySQL using mysqli!";
}

$conn->close();
?>
