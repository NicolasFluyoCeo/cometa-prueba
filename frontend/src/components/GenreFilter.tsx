// src/components/GenreFilter.tsx
'use client'

import { useRouter } from 'next/navigation'
import { Genre } from '@/lib/books'
import SearchableSelect from './SearchableSelect'

interface GenreFilterProps {
  genres: Genre[]
  selectedGenre: string
}

export default function GenreFilter({ genres, selectedGenre }: GenreFilterProps) {
  const router = useRouter()

  const handleGenreChange = (newGenre: string) => {
    router.push(`/?list=${newGenre}&offset=0`)
  }

  return (
    <div className="mb-4">
      <label htmlFor="genre-select" className="block text-sm font-medium text-gray-700 mb-2">
        Select a genre:
      </label>
      <SearchableSelect
        options={genres}
        value={selectedGenre}
        onChange={handleGenreChange}
      />
    </div>
  )
}