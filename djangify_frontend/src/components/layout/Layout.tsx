import React from 'react';
import { Button } from "@/components/ui/button";
import {
  Search,
  Home,
  Briefcase,
  BookOpen,
  User,
  Mail,
  Github,
  Linkedin
} from 'lucide-react';

import { ReactNode } from 'react';

const Layout = ({ children }: { children: ReactNode }) => {
  return (
    <div className="flex flex-col min-h-screen">
      <div className="flex flex-1">
        {/* Fixed Sidebar */}
        <aside className="w-64 bg-white border-r fixed h-[calc(100vh-64px)] flex flex-col">
          {/* Logo/Brand */}
          <div className="p-6 border-b">
            <div className="flex items-center space-x-2">
              <div className="w-8 h-8 bg-[#005b5e] rounded flex items-center justify-center">
                <span className="text-white font-bold">D</span>
              </div>
              <span className="text-lg font-semibold text-[#403f3f]">Djangify</span>
            </div>
          </div>

          {/* Navigation */}
          <nav className="flex-1 p-4">
            <div className="mb-8">
              <div className="relative">
                <input
                  type="text"
                  placeholder="Search..."
                  className="w-full px-4 py-2 pl-10 border rounded-md focus:outline-none focus:ring-2 focus:ring-[#005b5e] focus:border-transparent text-sm"
                />
                <Search className="absolute left-3 top-2.5 h-4 w-4 text-gray-400" />
              </div>
            </div>

            <div className="space-y-2">
              <a href="/" className="flex items-center px-4 py-2 text-[#403f3f] hover:bg-gray-50 rounded-md transition-colors">
                <Home className="w-5 h-5 mr-3" />
                <span>Home</span>
              </a>
              <a href="/projects" className="flex items-center px-4 py-2 text-[#403f3f] hover:bg-gray-50 rounded-md transition-colors">
                <Briefcase className="w-5 h-5 mr-3" />
                <span>Projects</span>
              </a>
              <a href="/blog" className="flex items-center px-4 py-2 text-[#403f3f] hover:bg-gray-50 rounded-md transition-colors">
                <BookOpen className="w-5 h-5 mr-3" />
                <span>Blog</span>
              </a>
              <a href="/about" className="flex items-center px-4 py-2 text-[#403f3f] hover:bg-gray-50 rounded-md transition-colors">
                <User className="w-5 h-5 mr-3" />
                <span>About</span>
              </a>
              <a href="/contact" className="flex items-center px-4 py-2 text-[#403f3f] hover:bg-gray-50 rounded-md transition-colors">
                <Mail className="w-5 h-5 mr-3" />
                <span>Contact</span>
              </a>
            </div>
          </nav>
        </aside>

        {/* Main Content */}
        <main className="ml-64 flex-1">
          <div className="min-h-[calc(100vh-64px)]">
            {children}
          </div>
        </main>
      </div>

      {/* Footer - Full Width */}
      <footer className="h-16 border-t bg-white mt-auto">
        <div className="h-full max-w-[1920px] mx-auto px-4 lg:px-8 flex items-center justify-between">
          {/* Logo/Brand */}
          <div className="flex items-center space-x-2">
            <div className="w-8 h-8 bg-[#005b5e] rounded flex items-center justify-center">
              <span className="text-white font-bold">D</span>
            </div>
            <span className="text-lg font-semibold text-[#403f3f]">Djangify</span>
          </div>

          {/* Navigation & Social Links */}
          <div className="flex items-center space-x-8">
            {/* Footer Navigation */}
            <nav className="hidden md:flex items-center space-x-6">
              <a href="/blog" className="text-sm text-[#737373] hover:text-[#403f3f] transition-colors">
                Blog
              </a>
              <a href="/projects" className="text-sm text-[#737373] hover:text-[#403f3f] transition-colors">
                Projects
              </a>
              <a href="/about" className="text-sm text-[#737373] hover:text-[#403f3f] transition-colors">
                About
              </a>
              <a href="/contact" className="text-sm text-[#737373] hover:text-[#403f3f] transition-colors">
                Contact
              </a>
            </nav>
          </div>
        </div>
      </footer>
    </div>
  );
};

export default Layout;
