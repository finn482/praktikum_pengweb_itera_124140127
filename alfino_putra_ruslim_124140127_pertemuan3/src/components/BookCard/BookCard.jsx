import PropTypes from 'prop-types'
import { useBooks } from '../../context/BookContext'
import './BookCard.css'

const statusLabels = { owned: 'Sudah punya', reading: 'Sedang baca', wishlist: 'Ingin beli' }

export default function BookCard({ book, onEdit }) {
  const { removeBook, toggleFinished } = useBooks()

  const handleDelete = () => {
    if (window.confirm(`Hapus buku “${book.title}” dari koleksi?`)) removeBook(book.id)
  }

  return (
    <article className={`book-card ${book.finished ? 'is-finished' : ''}`}>
      <div className="book-cover" aria-hidden="true"><span>{book.title.slice(0, 1).toUpperCase()}</span></div>
      <div className="book-info">
        <div className="book-card-top"><span className={`status status-${book.status}`}>{statusLabels[book.status]}</span>{book.finished && <span className="finished-badge">Selesai</span>}</div>
        <h3>{book.title}</h3><p className="book-author">oleh {book.author}</p>
        {book.notes && <p className="book-notes">“{book.notes}”</p>}
        <div className="book-actions"><button type="button" className="text-action" onClick={() => toggleFinished(book.id)}>{book.finished ? 'Tandai belum selesai' : 'Tandai selesai'}</button><div><button type="button" className="small-action" onClick={() => onEdit(book)} aria-label={`Edit ${book.title}`}>Edit</button><button type="button" className="small-action danger" onClick={handleDelete} aria-label={`Hapus ${book.title}`}>Hapus</button></div></div>
      </div>
    </article>
  )
}

BookCard.propTypes = { book: PropTypes.shape({ id: PropTypes.string.isRequired, title: PropTypes.string.isRequired, author: PropTypes.string.isRequired, status: PropTypes.oneOf(['owned', 'reading', 'wishlist']).isRequired, notes: PropTypes.string, finished: PropTypes.bool }).isRequired, onEdit: PropTypes.func.isRequired }
