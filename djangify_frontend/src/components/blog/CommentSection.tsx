'use client';

import { useState, FormEvent } from "react";
import { blogApi } from "@/lib/api/blog";
import type { Comment } from "@/lib/api/blog";


interface CommentFormData {
  name: string;
  email: string;
  content: string;
}

interface CommentSectionProps {
  postId: number;
  postSlug: string;
  initialComments: Comment[];
}

export function CommentSection({ postId, postSlug, initialComments }: CommentSectionProps) {
  const [comments, setComments] = useState<Comment[]>(initialComments);
  const [newComment, setNewComment] = useState<CommentFormData>({
    name: '',
    email: '',
    content: ''
  });
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState(false);

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setIsSubmitting(true);
    setError(null);
    setSuccess(false);

    try {
      const response = await blogApi.createComment(postSlug, newComment);
      setComments(prev => [...prev, response]);
      setNewComment({ name: '', email: '', content: '' });
      setSuccess(true);
    } catch (err) {
      setError('Failed to post comment. Please try again.');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <section className="space-y-8">
      {/* Rest of the component remains the same */}
    </section>
  );
}
