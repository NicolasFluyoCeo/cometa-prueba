import { Book } from '@/lib/books'

export default function BookCard({ book }: { book: Book }) {
  return (
    <div className="border rounded-lg p-4 shadow-md">
      <h2 className="text-xl font-semibold mb-2">{book.title}</h2>
      <p className="text-gray-600 mb-2">{book.author}</p>
      <p className="text-sm mb-2">{book.description}</p>
      <p className="text-sm"><strong>Publisher:</strong> {book.publisher}</p>
      <p className="text-sm"><strong>ISBN-13:</strong> {book.primary_isbn13}</p>
      <a
        href={`https://www.amazon.com/dp/${book.primary_isbn10}`}
        target="_blank"
        rel="noopener noreferrer"
        className="mt-4 inline-block bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 transition-colors"
      >
        Find on Amazon
      </a>
    </div>
  )
}