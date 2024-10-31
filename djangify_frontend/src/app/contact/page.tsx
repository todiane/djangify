// src/app/contact/page.tsx
import { ContactForm } from "../../components/contact/ContactForm";
import { Card } from "@/components/ui/card";
import { Mail, Phone, MapPin } from "lucide-react";

export default function ContactPage() {
  return (
    <div className="container mx-auto px-4 py-12">
      <div className="max-w-5xl mx-auto">
        <div className="grid lg:grid-cols-2 gap-8">
          {/* Contact Information */}
          <div className="space-y-6">
            <div>
              <h1 className="text-4xl font-bold tracking-tight">Get in Touch</h1>
              <p className="text-muted-foreground mt-2">
                Have a question or want to work together? Drop me a message.
              </p>
            </div>

            <div className="space-y-4">
              <Card className="p-4">
                <div className="flex items-center space-x-3">
                  <Mail className="h-5 w-5 text-primary" />
                  <span>contact@example.com</span>
                </div>
              </Card>

              <Card className="p-4">
                <div className="flex items-center space-x-3">
                  <Phone className="h-5 w-5 text-primary" />
                  <span>+1 (555) 123-4567</span>
                </div>
              </Card>

              <Card className="p-4">
                <div className="flex items-center space-x-3">
                  <MapPin className="h-5 w-5 text-primary" />
                  <span>123 Web Dev Street, Digital City, 12345</span>
                </div>
              </Card>
            </div>
          </div>

          {/* Contact Form */}
          <div>
            <ContactForm />
          </div>
        </div>
      </div>
    </div>
  );
}
