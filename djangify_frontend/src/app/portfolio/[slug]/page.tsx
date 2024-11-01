'use client';

import { useEffect, useState } from 'react';
import Image from 'next/image';
import { notFound } from 'next/navigation';
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Card, CardContent } from "@/components/ui/card";
import { Github, ExternalLink } from 'lucide-react';
import { PortfolioLightbox } from "@/components/portfolio/PortfolioLightbox";
import { portfolioApi } from '@/lib/api/portfolio';
import type { Portfolio } from '@/lib/api/portfolio';
import { LoadingPortfolio } from "@/components/ui/LoadingPortfolio";

interface PortfolioItemPageProps {
  params: {
    slug: string;
  };
}

export default function PortfolioItemPage({ params }: PortfolioItemPageProps) {
  const [item, setItem] = useState<Portfolio | null>(null);
  const [loading, setLoading] = useState(true);
  const [lightboxOpen, setLightboxOpen] = useState(false);
  const [lightboxIndex, setLightboxIndex] = useState(0);

  useEffect(() => {
    const fetchPortfolioItem = async () => {
      try {
        const itemData = await portfolioApi.getPortfolioItem(params.slug);
        setItem(itemData);
      } catch {
        notFound();
      } finally {
        setLoading(false);
      }
    };
    fetchPortfolioItem();
  }, [params.slug]);

  if (loading) {
    return <LoadingPortfolio />;
  }

  if (!item) {
    return notFound();
  }

  return (
    <div className="max-w-4xl mx-auto px-4 py-12">
      <div className="space-y-8">
        {/* Portfolio Item Header */}
        <div className="space-y-4">
          <h1 className="text-4xl font-bold">{item.title}</h1>
          <div className="flex flex-wrap gap-2">
            {item.technologies.map((tech) => (
              <Badge key={tech.slug} variant="secondary">
                {tech.name}
              </Badge>
            ))}
          </div>
          <div className="flex gap-4">
            {item.github_url && (
              <Button asChild variant="outline">
                <a href={item.github_url} target="_blank" rel="noopener noreferrer">
                  <Github className="mr-2 h-4 w-4" /> View Source
                </a>
              </Button>
            )}
            {item.project_url && (
              <Button asChild>
                <a href={item.project_url} target="_blank" rel="noopener noreferrer">
                  <ExternalLink className="mr-2 h-4 w-4" /> Live Demo
                </a>
              </Button>
            )}
          </div>
        </div>

        {/* Featured Image */}
        <div className="aspect-video relative rounded-lg overflow-hidden">
          <Image
            src={item.featured_image}
            alt={item.title}
            fill
            className="object-cover"
            priority
          />
        </div>

        {/* Portfolio Images Grid */}
        {item.images.length > 0 && (
          <div className="grid grid-cols-2 md:grid-cols-3 gap-4">
            {item.images.map((image, index) => (
              <Card
                key={image.id}
                className="overflow-hidden cursor-pointer transition-transform hover:scale-[1.02]"
                onClick={() => {
                  setLightboxIndex(index);
                  setLightboxOpen(true);
                }}
              >
                <div className="aspect-video relative">
                  <Image
                    src={image.image}
                    alt={image.caption}
                    fill
                    className="object-cover"
                  />
                </div>
                <CardContent className="p-2">
                  <p className="text-sm text-muted-foreground">{image.caption}</p>
                </CardContent>
              </Card>
            ))}
          </div>
        )}

        {/* Description */}
        <div className="prose max-w-none">
          <div dangerouslySetInnerHTML={{ __html: item.description }} />
        </div>

        {/* Lightbox */}
        <PortfolioLightbox
          images={item.images}
          initialIndex={lightboxIndex}
          isOpen={lightboxOpen}
          onClose={() => setLightboxOpen(false)}
        />
      </div>
    </div>
  );
}
