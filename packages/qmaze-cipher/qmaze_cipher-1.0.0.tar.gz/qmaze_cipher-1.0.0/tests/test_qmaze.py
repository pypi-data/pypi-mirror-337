import pytest
from qmaze_cipher import QMazeCipher

@pytest.fixture
def cipher():
    return QMazeCipher("TestKey42")

@pytest.fixture
def plaintext():
    return "Bu bir test mesajıdır."

def test_encrypt_decrypt(cipher, plaintext):
    encrypted = cipher.encrypt(plaintext)
    decrypted = cipher.decrypt(encrypted)
    assert decrypted == plaintext

def test_non_determinism(cipher, plaintext):
    encrypted1 = cipher.encrypt(plaintext)
    encrypted2 = cipher.encrypt(plaintext)
    assert encrypted1 != encrypted2

def test_wrong_key(cipher, plaintext):
    encrypted = cipher.encrypt(plaintext)
    wrong_cipher = QMazeCipher("WrongKey")
    with pytest.raises(ValueError):
        wrong_cipher.decrypt(encrypted)

def test_unicode(cipher):
    text = "Şifreleme örneği 🚀"
    encrypted = cipher.encrypt(text)
    decrypted = cipher.decrypt(encrypted)
    assert decrypted == text

def test_long(cipher):
    text = "Lorem ipsum dolor sit amet, consectetur adipiscing elit. " * 10
    encrypted = cipher.encrypt(text)
    decrypted = cipher.decrypt(encrypted)
    assert decrypted == text

def test_empty(cipher):
    encrypted = cipher.encrypt("")
    decrypted = cipher.decrypt(encrypted)
    assert decrypted == ""
