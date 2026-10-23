import PropTypes from 'prop-types'
import BookCard from '../BookCard/BookCard'
import './BookList.css'

export default function BookList({ books, onEdit }) {
  if (!books.length) return <div className="empty-state"><span className="empty-book" aria-hidden="true">□</span><h3>Belum ada buku yang cocok</h3><p>Coba ubah filter atau tambahkan buku baru ke koleksimu.</p></div>
  return <div className="book-list">{books.map((book) => <BookCard key={book.id} book={book} onEdit={onEdit} />)}</div>
}

BookList.propTypes = { books: PropTypes.arrayOf(PropTypes.shape({ id: PropTypes.string.isRequired, title: PropTypes.string.isRequired, author: PropTypes.string.isRequired, status: PropTypes.string.isRequired, notes: PropTypes.string, finished: PropTypes.bool })).isRequired, onEdit: PropTypes.func.isRequired }
