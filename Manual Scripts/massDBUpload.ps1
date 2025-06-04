function ProcessImage {
    param (
        [string]$image,
        [string]$DestDir,
        [string]$DbPath

    )

    # Create destination directory if it doesn't exist
    if (!(Test-Path -Path $DestDir)) {
        New-Item -ItemType Directory -Path $DestDir | Out-Null
    }

    $imageInfo = Get-Item -Path $image
    
    $destPath = Join-Path -Path $DestDir -ChildPath $imageInfo.Name
    Copy-Item -Path $imageInfo.FullName -Destination $destPath -Force

    # Update SQLite database
    try {
        $imagePath = 'uploaded_images/' + $imageInfo.Name

        $name = $imageInfo.BaseName.Substring($imageInfo.BaseName.IndexOf(" ") + 1).Split("_")[0]
        $range = $imageInfo.Name.Split(" ")[0]
        $publisher = $imageInfo.DirectoryName | Split-Path -Parent | Split-Path -Leaf
        $insertQuery = "INSERT INTO image_upload_image (image, name, publisher, range, upload_date) VALUES ('$imagePath', '$name', '$publisher', '$range', CURRENT_TIMESTAMP)"
        Invoke-SqliteQuery -DataSource $DbPath -Query $insertQuery
    }
    catch {
        Write-Error "Failed to update database: $($_.Exception.Message)"
    }
}


foreach ($dir in $prodirs) {
    $files = Get-ChildItem -Path $dir -Filter '*.jpg'
    foreach ($file in $files) {
        $destDir = 'C:\Users\ricky.burgess\OneDrive - Xodus Group\## Work - Code Repo\Repo - PowerShell\STL Processing\Website\stlCollection\media\uploaded_images'
        ProcessImage -image $file.FullName -DestDir $destDir -DbPath 'C:\Users\ricky.burgess\OneDrive - Xodus Group\## Work - Code Repo\Repo - PowerShell\STL Processing\Website\stlCollection\db.sqlite3'
        Write-Host "Processed image: $($file.FullName)"
    }
}


$dir = 'D:\temp\stl'

$files = Get-ChildItem -Path $dir -Filter 'Raticus *.jpg'

foreach ($file in $files) {
    $destDir = 'C:\Users\ricky.burgess\OneDrive - Xodus Group\## Work - Code Repo\Repo - PowerShell\STL Processing\Website\stl-collection-v2\media\uploaded_images'
    ProcessImage -image $file.FullName -DestDir $destDir -DbPath 'C:\Users\ricky.burgess\OneDrive - Xodus Group\## Work - Code Repo\Repo - PowerShell\STL Processing\Website\stl-collection-v2\db.sqlite3'
    Write-Host "Processed image: $($file.FullName)"
}