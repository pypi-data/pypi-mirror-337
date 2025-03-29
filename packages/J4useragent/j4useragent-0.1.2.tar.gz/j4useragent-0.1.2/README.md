# J4useragent

J4useragent adalah pustaka Python untuk menghasilkan User-Agent yang realistis untuk berbagai merek dan model perangkat Android.

## Instalasi

Gunakan pip untuk menginstal paket ini:
```sh
pip install J4useragent
```

## Penggunaan

```python
from J4useragent import GenerateUseragent

# Inisialisasi objek GenerateUseragent
os = GenerateUseragent()

# Menghasilkan User-Agent chrome dari sistem
ua = os.chromeuseragent(system=True)
print(ua)

# Menghasilkan User-Agent chrome dari sistem
ua = os.chromeuseragent()
print(ua)

# Menghasilkan User-Agent Facebook dari sistem
ua = os.facebookuseragent(system=True)
print(ua)

# Menghasilkan User-Agent Facebook secara acak
ua = os.facebookuseragent()
print(ua)

# Menghasilkan User-Agent instagram app dari sistem
ua = os.instagramuseragent(system=True)
print(ua)

# Menghasilkan User-Agent Instagram app secara acak
ua = os.instagramuseragent()
print(ua)
```

## Fitur
- Menghasilkan User-Agent Chrome
- Menghasilkan User-Agent Facebook
- Menghasilkan User-Agent Instagram 
- Mendukung berbagai merek dan model perangkat
- Dapat mengambil informasi perangkat dari sistem

## Lisensi

Proyek ini dilisensikan di bawah [MIT License](LICENSE).