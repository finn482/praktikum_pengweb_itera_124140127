import { useEffect, useState } from 'react'
import PropTypes from 'prop-types'
import { STATUS_OPTIONS, useBooks } from '../../context/BookContext'
import './BookForm.css'

const emptyForm = { title: '', author: '', status: 'owned', notes: '' }

export default function BookForm({ book, onDone }) {
  const { addBook, updateBook } = useBooks()
  const [form, setForm] = useState(emptyForm)
  const [errors, setErrors] = useState({})

  useEffect(() => {
    // Sinkronkan field ketika parent mengganti buku yang sedang diedit.
    // oxlint-disable-next-line react(set-state-in-effect)
    setForm(book ? { title: book.title, author: book.author, status: book.status, notes: book.notes || '' } : emptyForm)
    setErrors({})
  }, [book])

  const handleChange = ({ target }) => {
    setForm((current) => ({ ...current, [target.name]: target.value }))
    if (errors[target.name]) setErrors((current) => ({ ...current, [target.name]: '' }))
  }

  const validate = () => {
    const nextErrors = {}
    if (!form.title.trim()) nextErrors.title = 'Judul buku wajib diisi.'
    if (!form.author.trim()) nextErrors.author = 'Nama penulis wajib diisi.'
    return nextErrors
  }

  const handleSubmit = (event) => {
    event.preventDefault()
    const nextErrors = validate()
    if (Object.keys(nextErrors).length) {
      setErrors(nextErrors)
      return
    }
    const cleanBook = { ...form, title: form.title.trim(), author: form.author.trim(), notes: form.notes.trim() }
    if (book) updateBook(book.id, cleanBook)
    else addBook(cleanBook)
    setForm(emptyForm)
    onDone?.()
  }

  return (
    <form className="book-form" onSubmit={handleSubmit} noValidate>
      <div className="form-heading">
        <div><span className="eyebrow">{book ? 'PERBARUI KOLEKSI' : 'TAMBAH KE KOLEKSI'}</span><h2>{book ? 'Edit detail buku' : 'Catat buku baru'}</h2></div>
        <span className="form-step">01</span>
      </div>
      <div className="field full-field">
        <label htmlFor="title">Judul buku <span>*</span></label>
        <input id="title" name="title" value={form.title} onChange={handleChange} placeholder="Contoh: Filosofi Teras" aria-invalid={Boolean(errors.title)} />
        {errors.title && <small className="error-text">{errors.title}</small>}
      </div>
      <div className="field-row">
        <div className="field"><label htmlFor="author">Penulis <span>*</span></label><input id="author" name="author" value={form.author} onChange={handleChange} placeholder="Nama penulis" aria-invalid={Boolean(errors.author)} />{errors.author && <small className="error-text">{errors.author}</small>}</div>
        <div className="field"><label htmlFor="status">Status</label><select id="status" name="status" value={form.status} onChange={handleChange}>{STATUS_OPTIONS.map(({ value, label }) => <option key={value} value={value}>{label}</option>)}</select></div>
      </div>
      <div className="field"><label htmlFor="notes">Catatan <span className="optional">(opsional)</span></label><textarea id="notes" name="notes" value={form.notes} onChange={handleChange} rows="3" placeholder="Tulis catatan singkat..." /></div>
      <div className="form-actions"><button className="button button-primary" type="submit">{book ? 'Simpan perubahan' : 'Simpan buku'}</button>{book && <button className="button button-ghost" type="button" onClick={onDone}>Batal</button>}</div>
    </form>
  )
}

BookForm.propTypes = { book: PropTypes.shape({ id: PropTypes.string, title: PropTypes.string, author: PropTypes.string, status: PropTypes.string, notes: PropTypes.string }), onDone: PropTypes.func }
BookForm.defaultProps = { book: null, onDone: undefined }
