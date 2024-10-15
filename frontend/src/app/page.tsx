import { Suspense } from 'react'
import BookList from '@/components/BookList'
import GenreFilter from '@/components/GenreFilter'
import { getBooks, getGenres } from '@/lib/books'

export default async function Home({
  searchParams,
}: {
  searchParams: { list?: string; offset?: string }
}) {
  const list = searchParams.list || 'combined-print-fiction'
  const offset = parseInt(searchParams.offset || '0', 10)
  const [booksResponse, genres] = await Promise.all([
    getBooks(list, offset),
    getGenres()
  ])

  const initialBooks = booksResponse.data.results.map(book => book.book_details[0])

  return (
    <div className="container mx-auto px-4 py-8">
      <h1 className="text-3xl font-bold mb-4">NYT Recommended Books</h1>
      <Suspense fallback={<div>Loading genres...</div>}>
        <GenreFilter genres={genres} selectedGenre={list} />
      </Suspense>
      <Suspense fallback={<div>Loading books...</div>}>
        <BookList
          initialBooks={initialBooks}
          initialList={list}
          initialOffset={offset}
          initialNumResults={booksResponse.data.num_results}
          initialPageSize={booksResponse.data.page_size}
        />
      </Suspense>
    </div>
  )
}