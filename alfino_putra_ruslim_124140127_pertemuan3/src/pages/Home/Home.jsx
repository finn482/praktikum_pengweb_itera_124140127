import { useMemo, useState } from 'react'
import { Link } from 'react-router-dom'
import BookFilter from '../../components/BookFilter/BookFilter'
import BookForm from '../../components/BookForm/BookForm'
import BookList from '../../components/BookList/BookList'
import { useBooks } from '../../context/BookContext'
import { useBookStats } from '../../hooks/useBookStats'
import './Home.css'

export default function Home() {
  const { books } = useBooks()
  const stats = useBookStats(books)
  const [search, setSearch] = useState('')
  const [status, setStatus] = useState('all')
  const [editingBook, setEditingBook] = useState(null)
  const filteredBooks = useMemo(() => books.filter((book) => {
    const term = search.toLowerCase()
    const matchesSearch = `${book.title} ${book.author}`.toLowerCase().includes(term)
    return matchesSearch && (status === 'all' || book.status === status)
  }), [books, search, status])

  return <>
    <section className="home-hero"><div><span className="eyebrow">KOLEKSI PRIBADI · PERTEMUAN 3</span><h1>Ruang baca,<br /><em>ruang tumbuh.</em></h1><p>Catat buku yang sudah kamu punya, sedang kamu baca, atau ingin kamu beli nanti.</p></div><div className="hero-mark" aria-hidden="true"><span>“</span><small>every book<br />opens a new<br />door</small></div></section>
    <section className="quick-stats"><div><span>Total koleksi</span><strong>{stats.total}</strong></div><div><span>Sedang dibaca</span><strong>{stats.reading}</strong></div><div><span>Wishlist</span><strong>{stats.wishlist}</strong></div><Link to="/stats" className="stats-link">Lihat ringkasan <span>→</span></Link></section>
    <section className="workspace-grid"><div className="collection-panel"><div className="section-header"><div><span className="eyebrow">02 · KOLEKSI BUKU</span><h2>Buku-bukumu</h2></div><span className="result-count">{filteredBooks.length} buku</span></div><BookFilter search={search} status={status} onSearchChange={setSearch} onStatusChange={setStatus} /><BookList books={filteredBooks} onEdit={setEditingBook} /></div><div className="form-column"><BookForm book={editingBook} onDone={() => setEditingBook(null)} /></div></section>
  </>
}
