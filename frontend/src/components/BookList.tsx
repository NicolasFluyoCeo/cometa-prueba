// src/components/BookList.tsx
'use client'

import { useState, useEffect } from 'react'
import { useSearchParams, useRouter } from 'next/navigation'
import { Book } from '@/lib/books'
import BookCard from './BookCard'
import { getBooks } from '@/lib/books'

interface BookListProps {
  initialBooks: Book[]
  initialList: string
  initialOffset: number
  initialNumResults: number
  initialPageSize: number
}

export default function BookList({ 
  initialBooks, 
  initialList, 
  initialOffset, 
  initialNumResults, 
  initialPageSize 
}: BookListProps) {
  const [books, setBooks] = useState<Book[]>(initialBooks)
  const [list, setList] = useState(initialList)
  const [offset, setOffset] = useState(initialOffset)
  const [numResults, setNumResults] = useState(initialNumResults)
  const [pageSize, setPageSize] = useState(initialPageSize)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const searchParams = useSearchParams()
  const router = useRouter()

  useEffect(() => {
    const currentList = searchParams.get('list') || initialList
    const currentOffset = parseInt(searchParams.get('offset') || '0', 10)
    if (currentList !== list || currentOffset !== offset) {
      setList(currentList)
      setOffset(currentOffset)
      fetchBooks(currentList, currentOffset)
    }
  }, [searchParams, initialList, list, offset])

  const fetchBooks = async (currentList: string, currentOffset: number) => {
    setLoading(true)
    setError(null)
    try {
      const response = await getBooks(currentList, currentOffset)
      const newBooks = response.data.results.map(book => book.book_details[0])
      setBooks(newBooks)
      setNumResults(response.data.num_results)
      setPageSize(response.data.page_size)
    } catch (error) {
      console.error('Failed to fetch books:', error)
      setError('Failed to load books. Please try again later.')
    }
    setLoading(false)
  }

  const handlePageChange = (newOffset: number) => {
    router.push(`/?list=${list}&offset=${newOffset}`)
  }

  if (error) {
    return <div className="text-red-500">{error}</div>
  }

  const totalPages = Math.ceil(numResults / pageSize)
  const currentPage = Math.floor(offset / pageSize) + 1

  return (
    <div>
      {loading ? (
        <div className="flex justify-center items-center h-64">
          <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-gray-900"></div>
        </div>
      ) : (
        <>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {books.map((book, index) => (
              <BookCard key={`${book.primary_isbn13}-${index}`} book={book} />
            ))}
          </div>
          {totalPages > 1 && (
            <div className="mt-8 flex justify-center">
              <nav className="inline-flex rounded-md shadow">
                {Array.from({ length: totalPages }, (_, i) => i + 1).map((page) => (
                  <button
                    key={page}
                    onClick={() => handlePageChange((page - 1) * pageSize)}
                    className={`px-4 py-2 border ${
                      page === currentPage
                        ? 'bg-blue-500 text-white'
                        : 'bg-white text-gray-700 hover:bg-gray-50'
                    }`}
                  >
                    {page}
                  </button>
                ))}
              </nav>
            </div>
          )}
        </>
      )}
    </div>
  )
}