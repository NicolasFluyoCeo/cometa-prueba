// src/components/SearchableSelect.tsx
'use client'

import { useState, useEffect, useRef } from 'react'
import { Genre } from '@/lib/books'

interface SearchableSelectProps {
    options: Genre[]
    value: string
    onChange: (value: string) => void
}

export default function SearchableSelect({ options, value, onChange }: SearchableSelectProps) {
    const [isOpen, setIsOpen] = useState(false)
    const [search, setSearch] = useState('')
    const wrapperRef = useRef<HTMLDivElement>(null)

    useEffect(() => {
        function handleClickOutside(event: MouseEvent) {
            if (wrapperRef.current && !wrapperRef.current.contains(event.target as Node)) {
                setIsOpen(false)
            }
        }
        document.addEventListener('mousedown', handleClickOutside)
        return () => {
            document.removeEventListener('mousedown', handleClickOutside)
        }
    }, [wrapperRef])

    const filteredOptions = options.filter(option =>
        option.display_name.toLowerCase().includes(search.toLowerCase())
    )

    return (
        <div ref={wrapperRef} className="relative">
            <button
                onClick={() => setIsOpen(!isOpen)}
                className="w-full px-4 py-2 text-left bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-1 focus:ring-blue-500"
            >
                {options.find(option => option.code === value)?.display_name || 'Select a genre'}
            </button>
            {isOpen && (
                <div className="absolute z-10 w-full mt-1 bg-white border border-gray-300 rounded-md shadow-lg ">
                    <input
                        type="text"
                        placeholder="Search genres..."
                        value={search}
                        onChange={(e) => setSearch(e.target.value)}
                        className="w-full px-4 py-2 border-b border-gray-300 focus:outline-none focus:ring-1 focus:ring-blue-500"
                    />
                    <ul className="max-h-60 overflow-auto text-black">
                        {filteredOptions.map((option) => (
                            <li
                                key={option.code}
                                onClick={() => {
                                    onChange(option.code)
                                    setIsOpen(false)
                                    setSearch('')
                                }}
                                className="px-4 py-2 hover:bg-gray-100 cursor-pointer text-black"
                            >
                                {option.display_name}
                            </li>
                        ))}
                    </ul>
                </div>
            )}
        </div>
    )
}