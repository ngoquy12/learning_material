$deck = "d:\Rikkei Education\Create_Slide\workspace-bai-giang-du-an\Vong_Lap_JavaScript_Bai_Giang.pptx"
$outDir = "d:\Rikkei Education\Create_Slide\workspace-bai-giang-du-an\build\slide_images"
New-Item -ItemType Directory -Force -Path $outDir | Out-Null

try {
    $ppt = New-Object -ComObject PowerPoint.Application
    $pres = $ppt.Presentations.Open($deck, 2, 0, 0)
    $idx = 1
    foreach ($slide in $pres.Slides) {
        $imgPath = Join-Path $outDir "slide_$idx.png"
        $slide.Export($imgPath, "PNG", 1920, 1080)
        $idx++
    }
    $pres.Close()
    $ppt.Quit()
    Write-Host "SUCCESS: Exported $($idx - 1) slides to $outDir"
} catch {
    Write-Host "ERROR: $_"
}
