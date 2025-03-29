# QMazeCipher

QMazeCipher, kuantum bilgisayarlara dayanıklı, kaotik sistem tabanlı bir şifreleme algoritmasıdır. Logistic map ve dinamik hash tabanlı blok permütasyonu ile geleneksel frekans analizlerini boşar. Python ile yazılmıştır ve her türlü metni güvenli bir şekilde şifrelemek için uygundur.

## Özellikler
- Logistic Map ile kaotik karışıklık
- SHA3-256 tabanlı blok şifreleme
- Nonce (tuzlama) ile non-deterministik çıktı
- PKCS7 benzeri padding sistemi
- Base64 destekli çıktı

## Kurulum
```
pip install qmaze_cipher
```

## Kullanım
```python
from qmaze_cipher import QMazeCipher

cipher = QMazeCipher("gizli_anahtar")

sifreli = cipher.encrypt("Bu bir testtir.")
cozulen = cipher.decrypt(sifreli)

print(cozulen)  # Bu bir testtir.
```

## Testler
```bash
pytest tests/
```

## Lisans
MIT License