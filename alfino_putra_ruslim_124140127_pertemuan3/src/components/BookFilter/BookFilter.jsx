import PropTypes from 'prop-types'
import { STATUS_OPTIONS } from '../../context/BookContext'
import './BookFilter.css'

export default function BookFilter({ search, status, onSearchChange, onStatusChange }) {
  return <div className="book-filter"><label className="search-box"><span aria-hidden="true">⌕</span><span className="sr-only">Cari buku</span><input type="search" value={search} onChange={(event) => onSearchChange(event.target.value)} placeholder="Cari judul atau penulis..." /></label><div className="filter-tabs" role="group" aria-label="Filter status buku"><button type="button" className={status === 'all' ? 'active' : ''} onClick={() => onStatusChange('all')}>Semua</button>{STATUS_OPTIONS.map(({ value, label }) => <button key={value} type="button" className={status === value ? 'active' : ''} onClick={() => onStatusChange(value)}>{label}</button>)}</div></div>
}

BookFilter.propTypes = { search: PropTypes.string.isRequired, status: PropTypes.string.isRequired, onSearchChange: PropTypes.func.isRequired, onStatusChange: PropTypes.func.isRequired }
