param(
    [Parameter(Mandatory=$true)][string]$DeckPath,
    [Parameter(Mandatory=$true)][string]$OutDir
)

New-Item -ItemType Directory -Force -Path $OutDir | Out-Null

try {
    $ppt = New-Object -ComObject PowerPoint.Application
    $pres = $ppt.Presentations.Open($DeckPath, 2, 0, 0)
    $idx = 1
    foreach ($slide in $pres.Slides) {
        $imgPath = Join-Path $OutDir "slide_$idx.png"
        $slide.Export($imgPath, "PNG", 1920, 1080)
        $idx++
    }
    $pres.Close()
    $ppt.Quit()
    Write-Host "SUCCESS: Exported $($idx - 1) slides to $OutDir"
} catch {
    Write-Host "ERROR: $_"
    exit 1
}
