// security/diffie-hellman.js
// Реализация протокола Диффи-Хеллмана для безопасного обмена ключами

const crypto = require('crypto');

// Параметры DH (безопасные значения)
// p - большое простое число, g - генератор
const DH_PARAMS = {
  // 2048-битное простое число (RFC 3526 Group 14)
  p: BigInt('0xFFFFFFFFFFFFFFFFC90FDAA22168C234C4C6628B80DC1CD129024E088A67CC74020BBEA63B139B22514A08798E3404DDEF9519B3CD3A431B302B0A6DF25F14374FE1356D6D51C245E485B576625E7EC6F44C42E9A637ED6B0BFF5CB6F406B7EDEE386BFB5A899FA5AE9F24117C4B1FE649286651ECE45B3DC2007CB8A163BF0598DA48361C55D39A69163FA8FD24CF5F83655D23DCA3AD961C62F356208552BB9ED529077096966D670C354E4ABC9804F1746C08CA18217C32905E462E36CE3BE39E772C180E86039B2783A2EC07A28FB5C55DF06F4C52C9DE2BCBF6955817183995497CEA956AE515D2261898FA051015728E5A8AACAA68FFFFFFFFFFFFFFFF'),
  g: BigInt(2)
};

// Хранилище временных ключей сервера для обмена (sessionId -> serverPrivateKey)
const dhKeyStore = new Map();

// Время жизни ключа обмена (5 минут)
const KEY_EXPIRY = 5 * 60 * 1000;

/**
 * Модульное возведение в степень (a^b mod m)
 * Используем быстрый алгоритм возведения в степень
 */
function modPow(base, exponent, modulus) {
  if (modulus === BigInt(1)) return BigInt(0);
  
  let result = BigInt(1);
  base = base % modulus;
  
  while (exponent > BigInt(0)) {
    if (exponent % BigInt(2) === BigInt(1)) {
      result = (result * base) % modulus;
    }
    exponent = exponent / BigInt(2);
    base = (base * base) % modulus;
  }
  
  return result;
}

/**
 * Генерация случайного секретного ключа
 */
function generatePrivateKey() {
  // Генерируем 256-битное случайное число
  const randomBytes = crypto.randomBytes(32);
  return BigInt('0x' + randomBytes.toString('hex'));
}

/**
 * Вычисление публичного ключа: A = g^a mod p
 */
function computePublicKey(privateKey) {
  return modPow(DH_PARAMS.g, privateKey, DH_PARAMS.p);
}

/**
 * Вычисление общего секрета: K = B^a mod p
 */
function computeSharedSecret(otherPublicKey, privateKey) {
  return modPow(otherPublicKey, privateKey, DH_PARAMS.p);
}

/**
 * Преобразование общего секрета в ключ шифрования AES-256
 */
function deriveEncryptionKey(sharedSecret) {
  const secretHex = sharedSecret.toString(16).padStart(512, '0');
  const secretBuffer = Buffer.from(secretHex, 'hex');
  // Используем SHA-256 для получения 256-битного ключа
  return crypto.createHash('sha256').update(secretBuffer).digest();
}

/**
 * Инициализация обмена ключами на сервере
 * Возвращает публичный ключ сервера и идентификатор сессии обмена
 */
function initKeyExchange() {
  const exchangeId = crypto.randomBytes(16).toString('hex');
  const serverPrivateKey = generatePrivateKey();
  const serverPublicKey = computePublicKey(serverPrivateKey);
  
  // Сохраняем приватный ключ сервера
  dhKeyStore.set(exchangeId, {
    privateKey: serverPrivateKey,
    createdAt: Date.now()
  });
  
  // Автоматическая очистка через 5 минут
  setTimeout(() => {
    dhKeyStore.delete(exchangeId);
  }, KEY_EXPIRY);
  
  return {
    exchangeId,
    serverPublicKey: serverPublicKey.toString(16),
    p: DH_PARAMS.p.toString(16),
    g: DH_PARAMS.g.toString()
  };
}

/**
 * Завершение обмена ключами - вычисление общего секрета
 */
function completeKeyExchange(exchangeId, clientPublicKeyHex) {
  const keyData = dhKeyStore.get(exchangeId);
  
  if (!keyData) {
    throw new Error('Сессия обмена ключами не найдена или истекла');
  }
  
  // Проверяем срок действия
  if (Date.now() - keyData.createdAt > KEY_EXPIRY) {
    dhKeyStore.delete(exchangeId);
    throw new Error('Сессия обмена ключами истекла');
  }
  
  const clientPublicKey = BigInt('0x' + clientPublicKeyHex);
  const sharedSecret = computeSharedSecret(clientPublicKey, keyData.privateKey);
  const encryptionKey = deriveEncryptionKey(sharedSecret);
  
  // Удаляем использованный ключ
  dhKeyStore.delete(exchangeId);
  
  return encryptionKey;
}

/**
 * Расшифровка данных с использованием AES-256-GCM
 */
function decryptData(encryptedDataHex, ivHex, authTagHex, key) {
  const iv = Buffer.from(ivHex, 'hex');
  const authTag = Buffer.from(authTagHex, 'hex');
  const encryptedData = Buffer.from(encryptedDataHex, 'hex');
  
  const decipher = crypto.createDecipheriv('aes-256-gcm', key, iv);
  decipher.setAuthTag(authTag);
  
  let decrypted = decipher.update(encryptedData, null, 'utf8');
  decrypted += decipher.final('utf8');
  
  return decrypted;
}

/**
 * Шифрование данных с использованием AES-256-GCM (для ответов)
 */
function encryptData(data, key) {
  const iv = crypto.randomBytes(12);
  const cipher = crypto.createCipheriv('aes-256-gcm', key, iv);
  
  let encrypted = cipher.update(data, 'utf8', 'hex');
  encrypted += cipher.final('hex');
  
  const authTag = cipher.getAuthTag();
  
  return {
    encrypted,
    iv: iv.toString('hex'),
    authTag: authTag.toString('hex')
  };
}

module.exports = {
  initKeyExchange,
  completeKeyExchange,
  decryptData,
  encryptData,
  DH_PARAMS
};

