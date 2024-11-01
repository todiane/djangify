// src/components/portfolio/ProjectLightbox.tsx
'use client';

import { useState } from 'react';
import { Dialog, DialogContent } from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { ChevronLeft, ChevronRight, X } from "lucide-react";
import Image from 'next/image';

interface ProjectImage {
  id: number;
  image: string;
  caption: string;
}

interface ProjectLightboxProps {
  images: ProjectImage[];
  initialIndex?: number;
  onClose: () => void;
  isOpen: boolean;
}

export function ProjectLightbox({
  images,
  initialIndex = 0,
  onClose,
  isOpen
}: ProjectLightboxProps) {
  const [currentIndex, setCurrentIndex] = useState(initialIndex);

  const handlePrevious = () => {
    setCurrentIndex((prev) => (prev === 0 ? images.length - 1 : prev - 1));
  };

  const handleNext = () => {
    setCurrentIndex((prev) => (prev === images.length - 1 ? 0 : prev + 1));
  };

  // Handle keyboard navigation
  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'ArrowLeft') handlePrevious();
    if (e.key === 'ArrowRight') handleNext();
    if (e.key === 'Escape') onClose();
  };

  if (!isOpen) return null;

  return (
    <Dialog open={isOpen} onOpenChange={onClose}>
      <DialogContent
        className="max-w-[90vw] h-[90vh] p-0"
        onKeyDown={handleKeyDown}
      >
        <div className="relative h-full flex items-center justify-center">
          {/* Close button */}
          <Button
            variant="ghost"
            size="icon"
            className="absolute top-2 right-2 z-50"
            onClick={onClose}
          >
            <X className="h-4 w-4" />
          </Button>

          {/* Navigation buttons */}
          {images.length > 1 && (
            <>
              <Button
                variant="ghost"
                size="icon"
                className="absolute left-2 z-50"
                onClick={handlePrevious}
              >
                <ChevronLeft className="h-4 w-4" />
              </Button>
              <Button
                variant="ghost"
                size="icon"
                className="absolute right-2 z-50"
                onClick={handleNext}
              >
                <ChevronRight className="h-4 w-4" />
              </Button>
            </>
          )}

          {/* Image */}
          <div className="relative w-full h-full">
            <Image
              src={images[currentIndex].image}
              alt={images[currentIndex].caption}
              fill
              className="object-contain"
            />
          </div>

          {/* Caption */}
          {images[currentIndex].caption && (
            <div className="absolute bottom-0 left-0 right-0 bg-black/50 text-white p-4">
              <p className="text-center">{images[currentIndex].caption}</p>
            </div>
          )}
        </div>
      </DialogContent>
    </Dialog>
  );
}
