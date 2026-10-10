$docxPath = "C:\Users\Murilo\.gemini\antigravity\scratch\baozi-store\Atividade_Pratica_BaoziStore_Murilo_4425054.docx"
$pdfPath = "C:\Users\Murilo\.gemini\antigravity\scratch\baozi-store\Atividade_Pratica_BaoziStore_Murilo_4425054.pdf"

$word = New-Object -ComObject Word.Application
$word.Visible = $false
try {
    $doc = $word.Documents.Open($docxPath)
    $wdFormatPDF = 17
    $doc.SaveAs([ref]$pdfPath, [ref]$wdFormatPDF)
    $doc.Close()
    Write-Output "PDF Gerado com Sucesso em: $pdfPath"
} finally {
    $word.Quit()
}

