import { useMemo } from 'react'

export function useBookStats(books) {
  return useMemo(() => {
    const total = books.length
    const owned = books.filter(({ status }) => status === 'owned').length
    const reading = books.filter(({ status }) => status === 'reading').length
    const wishlist = books.filter(({ status }) => status === 'wishlist').length
    const finished = books.filter(({ finished }) => finished).length
    const progress = total ? Math.round((finished / total) * 100) : 0

    return { total, owned, reading, wishlist, finished, progress }
  }, [books])
}
