import { useEffect, useState } from 'react'

/** Menjaga sinkronisasi state React dengan localStorage. */
export function useLocalStorage(key, initialValue) {
  const [storedValue, setStoredValue] = useState(() => {
    try {
      const item = window.localStorage.getItem(key)
      return item ? JSON.parse(item) : initialValue
    } catch (error) {
      console.warn(`Gagal membaca ${key} dari localStorage`, error)
      return initialValue
    }
  })

  useEffect(() => {
    try {
      window.localStorage.setItem(key, JSON.stringify(storedValue))
    } catch (error) {
      console.warn(`Gagal menyimpan ${key} ke localStorage`, error)
    }
  }, [key, storedValue])

  return [storedValue, setStoredValue]
}
