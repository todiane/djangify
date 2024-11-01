// src/lib/api.ts
import axios from 'axios';

const api = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000/api/v1',
  headers: {
    'Content-Type': 'application/json',
  },
});

export async function getPostBySlug(slug: string) {
  try {
    const response = await fetch(`${process.env.NEXT_PUBLIC_API_URL}/blog/posts/${slug}/`)
    if (!response.ok) throw new Error('Post not found')
    return response.json()
  } catch (error) {
    console.error('Error fetching post:', error)
    return null
  }
}


export default api;
