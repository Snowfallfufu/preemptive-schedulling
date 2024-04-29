<!DOCTYPE html>
<html>
<head>
    <title>Image Display</title>
</head>
<body>
    <h1>Uploaded Image</h1>
    <?php
    // Check if a file was uploaded
    if (isset($_FILES['image']) && $_FILES['image']['error'] === UPLOAD_ERR_OK) {
        $file = $_FILES['image'];
        
        // Check if the uploaded file is an image
        $mime_type = mime_content_type($file['tmp_name']);
        if (strpos($mime_type, 'image') !== false) {
            // Move the uploaded file to a desired directory
            $destination = 'uploads/' . basename($file['name']);
            move_uploaded_file($file['tmp_name'], $destination);
            
            // Display the uploaded image
            echo '<img src="' . $destination . '" alt="Uploaded Image">';
        } else {
            echo 'Invalid file format. Only PNG and JPEG images are allowed.';
        }
    } else {
        echo 'No image uploaded.';
    }
    ?>
</body>
</html>
