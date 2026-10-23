import { fireEvent, render, renderHook, screen } from '@testing-library/react'
import { MemoryRouter } from 'react-router-dom'
import { beforeEach, describe, expect, it, vi } from 'vitest'
import BookCard from '../components/BookCard/BookCard'
import BookFilter from '../components/BookFilter/BookFilter'
import BookForm from '../components/BookForm/BookForm'
import { BookProvider } from '../context/BookContext'
import { useBookStats } from '../hooks/useBookStats'

const sampleBook = { id: 'book-1', title: 'Laut Bercerita', author: 'Leila S. Chudori', status: 'reading', notes: 'Baca sebelum tidur', finished: false }
const renderWithProvider = (ui) => render(<BookProvider>{ui}</BookProvider>)

beforeEach(() => {
  localStorage.clear()
  vi.restoreAllMocks()
})

describe('useBookStats', () => {
  it('menghitung total buku dan progres selesai', () => {
    const { result } = renderHook(() => useBookStats([sampleBook, { ...sampleBook, id: 'book-2', status: 'owned', finished: true }]))
    expect(result.current.total).toBe(2)
    expect(result.current.reading).toBe(1)
    expect(result.current.finished).toBe(1)
    expect(result.current.progress).toBe(50)
  })
})

describe('BookFilter', () => {
  it('memanggil callback ketika pengguna mencari buku', () => {
    const onSearchChange = vi.fn()
    render(<BookFilter search="" status="all" onSearchChange={onSearchChange} onStatusChange={vi.fn()} />)
    fireEvent.change(screen.getByRole('searchbox'), { target: { value: 'Leila' } })
    expect(onSearchChange).toHaveBeenCalledWith('Leila')
  })

  it('memanggil callback saat filter status dipilih', () => {
    const onStatusChange = vi.fn()
    render(<BookFilter search="" status="all" onSearchChange={vi.fn()} onStatusChange={onStatusChange} />)
    fireEvent.click(screen.getByRole('button', { name: 'Sedang baca' }))
    expect(onStatusChange).toHaveBeenCalledWith('reading')
  })
})

describe('BookForm', () => {
  it('menampilkan error ketika judul dan penulis kosong', () => {
    renderWithProvider(<BookForm />)
    fireEvent.click(screen.getByRole('button', { name: 'Simpan buku' }))
    expect(screen.getByText('Judul buku wajib diisi.')).toBeInTheDocument()
    expect(screen.getByText('Nama penulis wajib diisi.')).toBeInTheDocument()
  })

  it('menyimpan buku baru setelah form valid', () => {
    renderWithProvider(<BookForm />)
    fireEvent.change(screen.getByLabelText('Judul buku *'), { target: { value: sampleBook.title } })
    fireEvent.change(screen.getByLabelText('Penulis *'), { target: { value: sampleBook.author } })
    fireEvent.click(screen.getByRole('button', { name: 'Simpan buku' }))
    const saved = JSON.parse(localStorage.getItem('sudut-baca-books'))
    expect(saved).toHaveLength(1)
    expect(saved[0].title).toBe(sampleBook.title)
  })
})

describe('BookCard', () => {
  it('menampilkan metadata buku dan aksi edit', () => {
    renderWithProvider(<BookCard book={sampleBook} onEdit={vi.fn()} />)
    expect(screen.getByRole('heading', { name: sampleBook.title })).toBeInTheDocument()
    expect(screen.getByText(`oleh ${sampleBook.author}`)).toBeInTheDocument()
    expect(screen.getByRole('button', { name: `Edit ${sampleBook.title}` })).toBeInTheDocument()
  })

  it('mengubah status selesai saat tombol checklist ditekan', () => {
    localStorage.setItem('sudut-baca-books', JSON.stringify([sampleBook]))
    renderWithProvider(<BookCard book={sampleBook} onEdit={vi.fn()} />)
    fireEvent.click(screen.getByRole('button', { name: 'Tandai selesai' }))
    expect(JSON.parse(localStorage.getItem('sudut-baca-books'))[0].finished).toBe(true)
  })
})

function RouterHarness() {
  return <MemoryRouter initialEntries={['/']}><BookProvider><BookForm /></BookProvider></MemoryRouter>
}

it('dapat merender form di dalam router dan context', () => {
  render(<RouterHarness />)
  expect(screen.getByRole('heading', { name: 'Catat buku baru' })).toBeInTheDocument()
})
