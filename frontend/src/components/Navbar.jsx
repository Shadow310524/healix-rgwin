import { Link } from 'react-router-dom';
import { Menu, X, Pill } from 'lucide-react';
import { useState } from 'react';

const Navbar = () => {
  const [isOpen, setIsOpen] = useState(false);

  return (
    <nav className="bg-white shadow-sm border-b border-[var(--color-border)] sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <Link to="/" className="flex items-center gap-2">
              <img src="/logo.svg" className="h-8 w-8 object-contain" alt="Healix Logo" />
              <span className="font-bold text-xl text-[var(--color-primary-dark)]">Healix</span>
            </Link>
          </div>

          <div className="hidden md:flex items-center space-x-8">
            <Link to="/" className="text-[var(--color-text-main)] hover:text-[var(--color-primary)] font-medium transition-colors">Home</Link>
            <Link to="/about" className="text-[var(--color-text-main)] hover:text-[var(--color-primary)] font-medium transition-colors">About</Link>
            <Link to="/products" className="text-[var(--color-text-main)] hover:text-[var(--color-primary)] font-medium transition-colors">Products</Link>
            <Link to="/contact" className="text-[var(--color-text-main)] hover:text-[var(--color-primary)] font-medium transition-colors">Contact</Link>
          </div>

          <div className="md:hidden flex items-center">
            <button onClick={() => setIsOpen(!isOpen)} className="text-gray-500 hover:text-[var(--color-primary)]">
              {isOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
            </button>
          </div>
        </div>
      </div>

      {/* Mobile Menu */}
      {isOpen && (
        <div className="md:hidden bg-white border-t border-[var(--color-border)]">
          <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3">
            <Link to="/" className="block px-3 py-2 text-base font-medium text-[var(--color-text-main)] hover:bg-[var(--color-primary-light)] hover:text-[var(--color-primary)] rounded-md">Home</Link>
            <Link to="/about" className="block px-3 py-2 text-base font-medium text-[var(--color-text-main)] hover:bg-[var(--color-primary-light)] hover:text-[var(--color-primary)] rounded-md">About</Link>
            <Link to="/products" className="block px-3 py-2 text-base font-medium text-[var(--color-text-main)] hover:bg-[var(--color-primary-light)] hover:text-[var(--color-primary)] rounded-md">Products</Link>
            <Link to="/contact" className="block px-3 py-2 text-base font-medium text-[var(--color-text-main)] hover:bg-[var(--color-primary-light)] hover:text-[var(--color-primary)] rounded-md">Contact</Link>
          </div>
        </div>
      )}
    </nav>
  );
};

export default Navbar;
