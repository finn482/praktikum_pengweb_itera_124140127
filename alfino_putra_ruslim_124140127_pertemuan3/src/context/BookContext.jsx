/* oxlint-disable react/only-export-components */
import PropTypes from 'prop-types'
import { createContext, useCallback, useContext, useMemo } from 'react'
import { useLocalStorage } from '../hooks/useLocalStorage'

export { STATUS_OPTIONS } from './bookConstants'

const BookContext = createContext(null)
const STORAGE_KEY = 'sudut-baca-books'


const makeId = () => `${Date.now()}-${Math.random().toString(16).slice(2)}`

export function BookProvider({ children }) {
  const [books, setBooks] = useLocalStorage(STORAGE_KEY, [])

  const addBook = useCallback((book) => {
    setBooks((currentBooks) => [...currentBooks, { ...book, id: makeId(), finished: false, createdAt: new Date().toISOString() }])
  }, [setBooks])

  const updateBook = useCallback((id, changes) => {
    setBooks((currentBooks) => currentBooks.map((book) => (book.id === id ? { ...book, ...changes } : book)))
  }, [setBooks])

  const removeBook = useCallback((id) => {
    setBooks((currentBooks) => currentBooks.filter((book) => book.id !== id))
  }, [setBooks])

  const toggleFinished = useCallback((id) => {
    setBooks((currentBooks) => currentBooks.map((book) => (book.id === id ? { ...book, finished: !book.finished } : book)))
  }, [setBooks])

  const value = useMemo(() => ({ books, addBook, updateBook, removeBook, toggleFinished }), [books, addBook, updateBook, removeBook, toggleFinished])
  return <BookContext.Provider value={value}>{children}</BookContext.Provider>
}

BookProvider.propTypes = { children: PropTypes.node.isRequired }

export function useBooks() {
  const context = useContext(BookContext)
  if (!context) throw new Error('useBooks harus digunakan di dalam BookProvider')
  return context
}
