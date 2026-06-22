import { Link } from 'react-router-dom';

const Footer = () => {
  return (
    <footer className="bg-[var(--color-text-main)] text-white pt-12 pb-8">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div className="col-span-1 md:col-span-1">
            <div className="flex items-center gap-2 mb-4">
              <img src="/logo.svg" className="h-8 w-8 object-contain brightness-0 invert" alt="Healix Logo" />
              <span className="font-bold text-xl">Healix</span>
            </div>
            <p className="text-gray-400 text-sm">
              Empowering women's health through innovative pharmaceutical solutions by RG WIN HEALTHCARE.
            </p>
          </div>
          <div>
            <h3 className="text-lg font-semibold mb-4 text-[var(--color-primary-light)]">Quick Links</h3>
            <ul className="space-y-2 text-sm text-gray-300">
              <li><Link to="/" className="hover:text-white transition-colors">Home</Link></li>
              <li><Link to="/about" className="hover:text-white transition-colors">About Us</Link></li>
              <li><Link to="/products" className="hover:text-white transition-colors">Products</Link></li>
              <li><Link to="/contact" className="hover:text-white transition-colors">Contact</Link></li>
            </ul>
          </div>
          <div>
            <h3 className="text-lg font-semibold mb-4 text-[var(--color-primary-light)]">Legal</h3>
            <ul className="space-y-2 text-sm text-gray-300">
              <li><Link to="/privacy" className="hover:text-white transition-colors">Privacy Policy</Link></li>
              <li><Link to="/terms" className="hover:text-white transition-colors">Terms of Service</Link></li>
            </ul>
          </div>
          <div>
            <h3 className="text-lg font-semibold mb-4 text-[var(--color-primary-light)]">Contact</h3>
            <ul className="space-y-2 text-sm text-gray-300">
              <li>rgwinhealthcare@gmail.com</li>
              <li>+91 8248703790</li>
              <li>431, Bannerghatta Main Road, Hulimavu, Bangalore</li>
            </ul>
          </div>
        </div>
        <div className="border-t border-gray-700 mt-8 pt-8 text-center text-sm text-gray-400">
          <p>&copy; {new Date().getFullYear()} RG WIN HEALTHCARE. All rights reserved.</p>
        </div>
      </div>
    </footer>
  );
};

export default Footer;
