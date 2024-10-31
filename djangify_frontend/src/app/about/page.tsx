// src/app/about/page.tsx
import { Card, CardContent } from "@/components/ui/card";

export default function AboutPage() {
  return (
    <div className="container mx-auto px-4 py-12">
      <div className="max-w-3xl mx-auto">
        <h1 className="text-4xl font-bold mb-6">About Me</h1>

        <Card className="mb-8">
          <CardContent className="p-6">
            <h2 className="text-2xl font-semibold mb-4">Hi, I'm [Your Name]</h2>
            <p className="text-gray-600 mb-4">
              I'm a full-stack developer specializing in Django and React. With a passion for creating
              elegant solutions to complex problems, I enjoy building modern web applications that
              deliver great user experiences.
            </p>
            <p className="text-gray-600">
              When I'm not coding, you can find me exploring new technologies, contributing to open-source
              projects, or writing technical articles on my blog.
            </p>
          </CardContent>
        </Card>

        <div className="grid md:grid-cols-2 gap-6">
          <Card>
            <CardContent className="p-6">
              <h3 className="text-xl font-semibold mb-3">Skills</h3>
              <ul className="space-y-2 text-gray-600">
                <li>• Python & Django</li>
                <li>• React & Next.js</li>
                <li>• TypeScript</li>
                <li>• PostgreSQL</li>
                <li>• REST APIs</li>
              </ul>
            </CardContent>
          </Card>

          <Card>
            <CardContent className="p-6">
              <h3 className="text-xl font-semibold mb-3">Experience</h3>
              <ul className="space-y-2 text-gray-600">
                <li>• Full-Stack Development</li>
                <li>• Frontend Architecture</li>
                <li>• Backend Development</li>
                <li>• Database Design</li>
                <li>• API Development</li>
              </ul>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  );
}
