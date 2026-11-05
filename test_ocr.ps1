Add-Type -AssemblyName System.Drawing
[Windows.Globalization.Language, Windows.Foundation, ContentType = WindowsRuntime] | Out-Null
[Windows.Media.Ocr.OcrEngine, Windows.Foundation, ContentType = WindowsRuntime] | Out-Null
[Windows.Graphics.Imaging.BitmapDecoder, Windows.Foundation, ContentType = WindowsRuntime] | Out-Null

$engine = [Windows.Media.Ocr.OcrEngine]::TryCreateFromUserProfileLanguages()
if ($engine -eq $null) {
    $lang = [Windows.Globalization.Language]::new("en-US")
    $engine = [Windows.Media.Ocr.OcrEngine]::TryCreateFromLanguage($lang)
}
Write-Host "OCR Engine initialized: $($engine.RecognizerLanguage.LanguageTag)"

Get-ChildItem assets/extracted_logos/image*.png | ForEach-Object {
    $file = $_
    try {
        $asyncOp = [Windows.Storage.StorageFile]::GetFileFromPathAsync($file.FullName)
        $storageFile = $asyncOp.GetAwaiter().GetResult()
        $streamOp = $storageFile.OpenAsync([Windows.Storage.FileAccessMode]::Read)
        $stream = $streamOp.GetAwaiter().GetResult()
        $decoderOp = [Windows.Graphics.Imaging.BitmapDecoder]::CreateAsync($stream)
        $decoder = $decoderOp.GetAwaiter().GetResult()
        $bitmapOp = $decoder.GetSoftwareBitmapAsync()
        $bitmap = $bitmapOp.GetAwaiter().GetResult()
        $ocrOp = $engine.RecognizeAsync($bitmap)
        $result = $ocrOp.GetAwaiter().GetResult()
        if ($result.Text.Length -gt 0) {
            Write-Host "$($file.Name): $($result.Text)"
        }
    } catch {
    }
}
