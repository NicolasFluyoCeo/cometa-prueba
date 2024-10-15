const API_BASE_URL = 'http://localhost:8000';

export interface Book {
  title: string;
  description: string;
  contributor: string;
  author: string;
  contributor_note: string;
  price: number;
  age_group: string;
  publisher: string;
  primary_isbn13: string;
  primary_isbn10: string;
}

export interface Genre {
  code: string;
  display_name: string;
}

interface ApiResponse {
  error: boolean;
  message: string;
  data: {
    num_results: number;
    results: Book[];
    page_size: number;
  };
}

export async function getBooks(list: string = 'combined-print-fiction', offset: number = 0): Promise<ApiResponse> {
  try {
    const response = await fetch(`${API_BASE_URL}/books?list=${list}&offset=${offset}`, {
      headers: {
        'accept': 'application/json'
      }
    });

    if (!response.ok) {
      throw new Error('Network response was not ok');
    }

    const data: ApiResponse = await response.json();

    if (data.error) {
      throw new Error(data.message);
    }

    return data;
  } catch (error) {
    console.error('Error fetching books:', error);
    throw error;
  }
}
export async function getGenres(): Promise<Genre[]> {
  try {
    const response = await fetch(`${API_BASE_URL}/genres`, {
      headers: {
        'accept': 'application/json'
      }
    });

    if (!response.ok) {
      throw new Error('Network response was not ok');
    }

    const data = await response.json();

    if (data.error) {
      throw new Error(data.message);
    }

    return data.data;
  } catch (error) {
    console.error('Error fetching genres:', error);
    throw error;
  }
}