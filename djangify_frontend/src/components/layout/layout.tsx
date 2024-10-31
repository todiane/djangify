import React, { useState, ReactNode } from 'react';
import { Button } from '@/components/ui/button';
import { Card } from '@/components/ui/card';
import {
  Menu, X, Home, Briefcase, BookOpen, User, Mail,
  Search, Settings, PenSquare, Github, Linkedin
} from 'lucide-react';

interface LayoutProps {
  children: ReactNode;
  isAdmin?: boolean;
}

const Layout = ({ children, isAdmin = false }: LayoutProps) => {
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);
  const [isSearchOpen, setIsSearchOpen] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  const [currentPath, setCurrentPath] = useState('/');

  const publicNavItems = [
    { label: 'Home', icon: Home, href: '#' },
    { label: 'Projects', icon: Briefcase, href: '#/projects' },
    { label: 'Blog', icon: BookOpen, href: '#/blog' },
    { label: 'About', icon: User, href: '#/about' },
    { label: 'Contact', icon: Mail, href: '#/contact' }
  ];

  const adminNavItems = [
    { label: 'New Post', icon: PenSquare, href: '#/admin/new-post' },
    { label: 'Settings', icon: Settings, href: '#/admin/settings' }
  ];

  const navigationItems = isAdmin
    ? [...publicNavItems, ...adminNavItems]
    : publicNavItems;

  const footerLinks = [
    { label: 'Blog', href: '#/blog' },
    { label: 'Projects', href: '#/projects' },
    { label: 'About', href: '#/about' },
    { label: 'Contact', href: '#/contact' },
  ];

  return (
    <div className="flex flex-col min-h-screen bg-white">
      {/* Rest of the component remains the same */}
      {/* Top Navigation Bar */}
      <div className="fixed top-0 right-0 left-0 h-16 bg-white border-b z-50 flex items-center justify-between px-4 lg:pl-56">
        <Button
          variant="ghost"
          onClick={() => setIsSidebarOpen(!isSidebarOpen)}
          className="lg:hidden p-2"
        >
          {isSidebarOpen ? <X size={24} /> : <Menu size={24} />}
        </Button>

        <div className="flex-1 max-w-xl mx-4 relative">
          <div className="relative">
            <input
              type="text"
              placeholder="Search..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              onFocus={() => setIsSearchOpen(true)}
              className="w-full px-4 py-2 border rounded-md pl-10 focus:outline-none focus:ring-2 focus:ring-[#005b5e] focus:border-transparent"
            />
            <Search className="absolute left-3 top-2.5 h-4 w-4 text-gray-400" />
          </div>
        </div>

        <div className="flex items-center space-x-4">
          <span className="text-[#403f3f] font-semibold">Your Name</span>
          <img
            src="/api/placeholder/40/40"
            alt="Profile"
            className="w-10 h-10 rounded-full"
          />
        </div>
      </div>

      {/* Sidebar */}
      <aside
        className={`
          fixed top-0 left-0 h-[calc(100vh-64px)] bg-white border-r z-40 transition-all duration-300
          lg:w-56 lg:translate-x-0 pt-16 lg:pt-0
          ${isSidebarOpen ? 'w-56 translate-x-0' : 'w-56 -translate-x-full'}
          ${!isSidebarOpen && 'lg:w-16'}
        `}
      >
        <nav className="mt-6">
          {navigationItems.map((item) => (
            <a
              key={item.href}
              href={item.href}
              className={`
                flex items-center px-4 py-3 text-[#403f3f] hover:bg-gray-50
                hover:text-[#737373] transition-colors duration-200
                ${currentPath === item.href ? 'bg-gray-50 text-[#005b5e]' : ''}
              `}
            >
              <item.icon className="w-5 h-5" />
              <span className={`ml-3 transition-opacity duration-300 ${!isSidebarOpen && 'lg:hidden'}`}>
                {item.label}
              </span>
            </a>
          ))}
        </nav>
      </aside>

      {/* Main content */}
      <main className={`
        flex-1 transition-all duration-300 pt-16 pb-16
        ${isSidebarOpen ? 'lg:ml-56' : 'lg:ml-16'}
      `}>
        <div className="max-w-6xl mx-auto px-4 py-8">
          {children}
        </div>
      </main>

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
              {footerLinks.map((link) => (
                <a
                  key={link.href}
                  href={link.href}
                  className="text-sm text-[#737373] hover:text-[#403f3f] transition-colors"
                >
                  {link.label}
                </a>
              ))}
            </nav>

            {/* Social Links */}
            <div className="flex items-center space-x-4">
              <a href="#" className="text-[#737373] hover:text-[#403f3f] transition-colors">
                <Github className="w-5 h-5" />
              </a>
              <a href="#" className="text-[#737373] hover:text-[#403f3f] transition-colors">
                <Linkedin className="w-5 h-5" />
              </a>
            </div>
          </div>
        </div>
      </footer>

      {/* Click outside search to close */}
      {isSearchOpen && (
        <div
          className="fixed inset-0 z-40"
          onClick={() => setIsSearchOpen(false)}
        />
      )}
    </div>
  );
};

export default Layout;
