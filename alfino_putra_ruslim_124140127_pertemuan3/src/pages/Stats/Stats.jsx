import { Link } from 'react-router-dom'
import { useBooks } from '../../context/BookContext'
import { useBookStats } from '../../hooks/useBookStats'
import './Stats.css'

export default function Stats() {
  const { books } = useBooks()
  const stats = useBookStats(books)
  const progressRows = [{ label: 'Sudah punya', value: stats.owned, color: 'blue' }, { label: 'Sedang baca', value: stats.reading, color: 'teal' }, { label: 'Ingin beli', value: stats.wishlist, color: 'orange' }]
  return <section className="stats-page"><div className="stats-page-heading"><div><span className="eyebrow">03 · RINGKASAN</span><h1>Seberapa jauh<br /><em>koleksimu berjalan?</em></h1><p>Ringkasan kecil untuk melihat kebiasaan membaca dan rencana bukumu.</p></div><Link className="back-link" to="/">← Kembali ke koleksi</Link></div><div className="big-stat"><div><span>Total semua buku</span><strong>{stats.total}</strong><small>judul tersimpan</small></div><div className="progress-ring" style={{ '--progress': `${stats.progress * 3.6}deg` }}><span>{stats.progress}%</span><small>selesai</small></div></div><div className="stats-detail"><div className="breakdown"><span className="eyebrow">STATUS BUKU</span><h2>Komposisi koleksi</h2>{progressRows.map(({ label, value, color }) => <div className="progress-row" key={label}><div><span>{label}</span><strong>{value}</strong></div><div className="progress-track"><span className={`progress-fill ${color}`} style={{ width: `${stats.total ? (value / stats.total) * 100 : 0}%` }} /></div></div>)}</div><div className="stats-note"><span className="note-mark">✦</span><h3>Ruang untuk kebiasaan baru</h3><p>Koleksi bukan soal banyaknya buku, tapi tentang ide yang sempat kamu temui dan bawa pulang.</p><Link to="/" className="button button-primary">Tambah buku baru</Link></div></div></section>
}
