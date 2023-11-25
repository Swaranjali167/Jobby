<?php
session_start();
if (!isset($_SESSION['user'])) {
    header('Location: login.php');
    exit();
}

include "connectDB.php";

// Fetch job details from the database
$sql = "SELECT * FROM job_web";
$result = $conn->query($sql);

// Check if there are any rows in the result
if ($result->num_rows > 0) {
    // Fetch all rows as an associative array
    $jobDetails = $result->fetch_all(MYSQLI_ASSOC);
} else {
    $jobDetails = array(); // If no rows found, initialize as an empty array
}

$conn->close();
?>
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="utf-8">
    <meta name="author" content="Group-36, Fall 2023">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <title>JOBIFY - Home</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta2/dist/css/bootstrap.min.css" rel="stylesheet"
        integrity="sha384-BmbxuPwQa2lc/FVzBcNJ7UAyJxM6wuqIj61tLrc4wSX0szH/Ev+nYRRuWlolflfl" crossorigin="anonymous">
    
    <style>
        .container {
            padding-top: 10px;
        }
        table {
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
            box-shadow: 0 0 20px rgba(0, 0, 0, 0.1);
            background-color: #fff;
            border-radius: 8px;
            overflow: hidden;
        }

        .tl,
        td {
            border: 1px solid #ddd;
            padding: 12px;
            text-align: left;
        }

        .tl {
            background-color: #f2f2f2;
        }

        .acls {
            text-decoration: none;
            color: #3498db;
            font-weight: bold;
        }

        a:hover {
            color: #1e70bf;
        }
        .bg-img {
            background-image: url("./css/background.jpeg");
            background-position: center;
        }
    </style>
</head>
<?php
include "header.php";
?>
<body>
    <div class="bg-img">
        <div class="container">

            <?php if (!empty($jobDetails)): ?>
                <table class="table">
                    <thead>
                        <tr>
                            <th class="tl">Title</th>
                            <th class="tl">Link</th>
                            <th class="tl">Company Name</th>
                            <th class="tl">Posted Date</th>
                            <th class="tl">Match Percentage</th>
                            <th class="tl">Skills</th>
                        </tr>
                    </thead>
                    <tbody>
                        <?php foreach ($jobDetails as $row): ?>
                            <tr>
                                <?php foreach ($row as $key => $value): ?>
                                    <?php if ($key === 'job_url'): ?>
                                        <td><a class="acls" href="<?= $value ?>" target="_blank">Apply Now</a></td>
                                    <?php else: ?>
                                        <td>
                                            <?= $value ?>
                                        </td>
                                    <?php endif; ?>
                                <?php endforeach; ?>
                            </tr>
                        <?php endforeach; ?>
                    </tbody>
                </table>
            <?php else: ?>
                <p>No job details available.</p>
            <?php endif; ?>

            <p><a class="acls" href="home.php">Home</a></p>
        </div>
    </div>
</body>

</html>