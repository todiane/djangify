import { Card, CardContent } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import Image from "next/image"
import Link from "next/link"
import { Github, ExternalLink } from "lucide-react"

interface Technology {
  id: number
  name: string
  slug: string
  icon: string
}

interface Portfolio {
  id: number
  title: string
  slug: string
  description: string
  short_description: string
  featured_image: string
  technologies: Technology[]
  project_url?: string
  github_url?: string
  is_featured: boolean
  order: number
}

interface PortfolioGridProps {
  initialItems: Portfolio[]
  technologies: Technology[]
}

export function PortfolioGrid({ initialItems, technologies }: PortfolioGridProps) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {initialItems.map((item) => (
        <Card key={item.id} className="overflow-hidden">
          <div className="aspect-video relative">
            <Image
              src={item.featured_image}
              alt={item.title}
              fill
              className="object-cover"
            />
          </div>
          <CardContent className="p-6">
            <h3 className="text-xl font-semibold mb-2">
              <Link 
                href={`/portfolio/${item.slug}`}
                className="hover:text-primary"
              >
                {item.title}
              </Link>
            </h3>
            <p className="text-muted-foreground mb-4 line-clamp-2">
              {item.short_description}
            </p>
            <div className="flex flex-wrap gap-2 mb-4">
              {item.technologies.map((tech) => (
                <span
                  key={tech.id}
                  className="text-xs bg-primary/10 text-primary px-2 py-1 rounded"
                >
                  {tech.name}
                </span>
              ))}
            </div>
            <div className="flex gap-3">
              {item.github_url && (
                <Button variant="outline" size="sm" asChild>
                  <a href={item.github_url} target="_blank" rel="noopener noreferrer">
                    <Github className="w-4 h-4 mr-2" />
                    Code
                  </a>
                </Button>
              )}
              {item.project_url && (
                <Button variant="outline" size="sm" asChild>
                  <a href={item.project_url} target="_blank" rel="noopener noreferrer">
                    <ExternalLink className="w-4 h-4 mr-2" />
                    Demo
                  </a>
                </Button>
              )}
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  )
}
