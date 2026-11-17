# pythonweb

A small command-line web scanner written in Python. It gathers basic information about a website, inspects forms and security headers, checks common paths and subdomains, and performs active checks for potential web vulnerabilities. It can also generate an HTML scan report.

> **Authorized use only:** Run this tool only against websites and systems you own or have explicit permission to assess. Active scanning sends requests that may affect a site. Findings are preliminary and should be verified safely by an authorized security professional.

## Requirements

- Python 3
- `requests`, `urllib3`, and `beautifulsoup4`

Install the dependencies:

```bash
python -m pip install requests urllib3 beautifulsoup4
```

## Run

From the repository directory:

```bash
python jlfs.py
```

When prompted, enter the URL of an authorized target, including `https://` where appropriate. The report is saved as an HTML file in the current directory.

## Notes

The script looks for wordlists and test data in `wordlists/common_dirs.txt`, `wordlists/common_subs.txt`, and `payloads/` (`sqli.txt`, `xss.txt`, and `lfi.txt`). These files are not included in the repository, so corresponding scan features may not work until the files are supplied. The script currently disables TLS certificate verification for its HTTP requests; use caution and do not rely on it for secure production workflows.

---

# Tetun

Programa ki'ik ida ba linha-komandu ne'ebé hakerek iha Python atu analiza website. Programa ne'e halibur informasaun bázika kona-ba website, haree formuláriu no HTTP security headers, buka dalan no subdomíniu komún, no halo teste ativu atu buka vulnerabilidade web ne'ebé posível. Programa bele mos kria relatóriu HTML.

> **Uza de'it ho autorizasaun:** Uza ferramenta ne'e de'it ba website no sistema ne'ebé ita-nia ka ita hetan lisensa atu analiza. Teste ativu haruka pedidu ba website no bele afeta nia servisu. Rezultadu sira mak indikasaun inisiál; profisionál seguransa ne'ebé hetan autorizasaun tenke verifika ho kuidadu.

## Presiza

- Python 3
- `requests`, `urllib3`, no `beautifulsoup4`

Instala dependénsia sira:

```bash
python -m pip install requests urllib3 beautifulsoup4
```

## Hala'o

Husi pasta repositóriu nian:

```bash
python jlfs.py
```

Bainhira husu, hatama URL ba alvu ne'ebé ita iha autorizasaun atu testa, inklui `https://` bainhira apropriadu. Relatóriu HTML sei rai iha pasta atual.

## Nota

Script buka lista liafuan no dadus teste iha `wordlists/common_dirs.txt`, `wordlists/common_subs.txt` no `payloads/` (`sqli.txt`, `xss.txt` no `lfi.txt`). Arquivu sira ne'e seidauk iha repositóriu, nune'e funsaun scan ne'ebé depende ba sira bele la funsiona to'o ita prepara arquivu sira. Agora daudaun script la verifica sertifikadu TLS ba pedidu HTTP; uza ho kuidadu no labele depende ba ne'e iha prosesu produsaun ne'ebé presiza seguransa.

---

# Português

Um pequeno scanner web de linha de comando escrito em Python. Ele recolhe informações básicas sobre um site, analisa formulários e cabeçalhos de segurança HTTP, verifica caminhos e subdomínios comuns e realiza testes ativos para identificar possíveis vulnerabilidades web. Também pode gerar um relatório HTML.

> **Utilize apenas com autorização:** Execute esta ferramenta somente em sites e sistemas que lhe pertençam ou para os quais tenha autorização explícita. A análise ativa envia pedidos que podem afetar o site. Os resultados são preliminares e devem ser verificados com segurança por um profissional autorizado.

## Requisitos

- Python 3
- `requests`, `urllib3` e `beautifulsoup4`

Instale as dependências:

```bash
python -m pip install requests urllib3 beautifulsoup4
```

## Execução

No diretório do repositório:

```bash
python jlfs.py
```

Quando solicitado, introduza o URL de um alvo autorizado, incluindo `https://` quando apropriado. O relatório é guardado como ficheiro HTML no diretório atual.

## Observações

O script procura listas de palavras e dados de teste em `wordlists/common_dirs.txt`, `wordlists/common_subs.txt` e `payloads/` (`sqli.txt`, `xss.txt` e `lfi.txt`). Estes ficheiros não estão incluídos no repositório; por isso, as funcionalidades de análise correspondentes podem não funcionar até que os ficheiros sejam fornecidos. Atualmente, o script desativa a verificação de certificados TLS nos pedidos HTTP; tenha cuidado e não dependa dele em fluxos de produção que exijam segurança.

---

# Bahasa Indonesia

Pemindai web sederhana berbasis baris perintah yang ditulis dengan Python. Program ini mengumpulkan informasi dasar tentang situs web, memeriksa formulir dan header keamanan HTTP, memeriksa jalur serta subdomain umum, dan menjalankan pemeriksaan aktif untuk menemukan potensi kerentanan web. Program ini juga dapat membuat laporan HTML.

> **Hanya gunakan dengan izin:** Jalankan alat ini hanya pada situs dan sistem milik Anda atau yang secara eksplisit telah memberi Anda izin untuk diuji. Pemindaian aktif mengirimkan permintaan yang dapat memengaruhi situs. Temuan bersifat awal dan harus diverifikasi dengan aman oleh profesional keamanan yang berwenang.

## Persyaratan

- Python 3
- `requests`, `urllib3`, dan `beautifulsoup4`

Pasang dependensi:

```bash
python -m pip install requests urllib3 beautifulsoup4
```

## Menjalankan

Dari direktori repositori:

```bash
python jlfs.py
```

Saat diminta, masukkan URL target yang telah Anda izinkan untuk diuji, termasuk `https://` jika sesuai. Laporan akan disimpan sebagai file HTML di direktori saat ini.

## Catatan

Skrip mencari wordlist dan data pengujian di `wordlists/common_dirs.txt`, `wordlists/common_subs.txt`, dan `payloads/` (`sqli.txt`, `xss.txt`, dan `lfi.txt`). Berkas-berkas tersebut belum disertakan dalam repositori, sehingga fitur pemindaian terkait mungkin tidak berfungsi sampai berkas tersedia. Saat ini skrip menonaktifkan verifikasi sertifikat TLS untuk permintaan HTTP; gunakan dengan hati-hati dan jangan mengandalkannya untuk alur kerja produksi yang membutuhkan keamanan.
