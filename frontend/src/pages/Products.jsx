import { motion } from 'framer-motion';
import { useState, useEffect } from 'react';
import { Search, Filter, ArrowRight } from 'lucide-react';
import { Link } from 'react-router-dom';
import { productService } from '../services/api';

const Products = () => {
  const [searchTerm, setSearchTerm] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('All');
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        const data = await productService.getProducts();
        setProducts(data);
      } catch (error) {
        console.error("Error fetching products:", error);
      } finally {
        setLoading(false);
      }
    };
    fetchProducts();
  }, []);

  const categories = ['All', ...new Set(products.map(p => p.category?.name || 'Uncategorized'))];

  const filteredProducts = products.filter(product => {
    const matchesSearch = product.name.toLowerCase().includes(searchTerm.toLowerCase());
    const catName = product.category?.name || 'Uncategorized';
    const matchesCategory = selectedCategory === 'All' || catName === selectedCategory;
    return matchesSearch && matchesCategory;
  });

  return (
    <div className="bg-gradient-to-br from-[#F0F4FF] via-[#E8F0FE] to-[#DCE6FA] min-h-screen py-12 relative overflow-hidden">
      {/* Decorative background blurs to enhance glass effect */}
      <div className="absolute top-0 left-0 w-96 h-96 bg-blue-400/10 rounded-full mix-blend-multiply filter blur-3xl opacity-70 animate-blob"></div>
      <div className="absolute top-0 right-0 w-96 h-96 bg-teal-400/10 rounded-full mix-blend-multiply filter blur-3xl opacity-70 animate-blob animation-delay-2000"></div>
      <div className="absolute -bottom-8 left-20 w-96 h-96 bg-indigo-400/10 rounded-full mix-blend-multiply filter blur-3xl opacity-70 animate-blob animation-delay-4000"></div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
        <div className="mb-12">
          <h1 className="text-4xl font-extrabold text-[#0A2540] tracking-tight mb-4">Our Products</h1>
          <p className="text-slate-600 text-lg">Explore the Healix range of premium healthcare solutions.</p>
        </div>

        <div className="mb-8 max-w-md">
          <div className="relative">
            <input
              type="text"
              placeholder="Search products..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-10 pr-4 py-3 bg-white/70 backdrop-blur-md border border-white/80 rounded-xl focus:outline-none focus:ring-2 focus:ring-[#0A2540]/20 shadow-[0_4px_16px_rgba(31,38,135,0.05)] transition-shadow"
            />
            <Search className="absolute left-3 top-3.5 text-slate-400 h-5 w-5" />
          </div>
        </div>

        <div className="flex gap-2 overflow-x-auto mb-8 pb-2">
          {categories.map(cat => (
            <button 
              key={cat} 
              onClick={() => setSelectedCategory(cat)}
              className={`px-5 py-2.5 rounded-full whitespace-nowrap font-medium transition-all duration-300 ${selectedCategory === cat ? 'bg-[#0A2540] text-white shadow-lg' : 'bg-white/60 backdrop-blur-md text-slate-700 hover:bg-white border border-white/50 shadow-sm'}`}
            >
              {cat}
            </button>
          ))}
        </div>

        {loading ? (
          <div className="text-center py-20 text-[var(--color-text-muted)]">Loading products...</div>
        ) : (
          <div className="grid grid-cols-1 xl:grid-cols-2 gap-8">
          {filteredProducts.map((product, idx) => (
            <motion.div 
              key={product.id}
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, margin: "-20px" }}
              transition={{ duration: 0.6, delay: idx * 0.05, ease: "easeOut" }}
              className="flex flex-col sm:flex-row h-full overflow-hidden bg-white/60 backdrop-blur-2xl border border-white sm:rounded-2xl shadow-[0_8px_32px_rgba(31,38,135,0.08)] hover:shadow-[0_16px_48px_rgba(31,38,135,0.15)] hover:bg-white/80 transition-all duration-500 group"
            >
              <div className="w-full sm:w-2/5 h-64 sm:h-auto overflow-hidden relative p-8 bg-gradient-to-br from-white/40 to-transparent border-b sm:border-b-0 sm:border-r border-white flex items-center justify-center">
                <img 
                  src={product.image_url} 
                  alt={product.name} 
                  className="max-w-full max-h-full object-contain mix-blend-multiply drop-shadow-[0_20px_20px_rgba(0,0,0,0.15)] transition-transform duration-500 group-hover:scale-105 group-hover:drop-shadow-[0_30px_30px_rgba(0,0,0,0.25)]" 
                />
              </div>
              <div className="flex-grow p-8 flex flex-col justify-between bg-transparent w-full sm:w-3/5">
                <div>
                  <span className="text-[10px] font-bold text-[#0A2540] uppercase tracking-[0.15em] border-b-2 border-[#0A2540] pb-1 inline-block opacity-80">{product.category?.name || 'Uncategorized'}</span>
                  <h3 className="text-3xl font-extrabold text-[#0A2540] mt-5 mb-4 leading-tight tracking-tight">{product.name}</h3>
                  
                  {product.ingredients && product.ingredients.length > 0 && (
                    <div className="mt-8">
                      <div className="text-[10px] font-bold text-slate-500 uppercase tracking-widest mb-2 flex items-center gap-2">
                        <svg className="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"></path></svg>
                        Active Composition
                      </div>
                      <div className="text-sm font-semibold text-slate-800 p-4 bg-white/50 backdrop-blur-md border border-white/80 rounded-xl shadow-[inset_0_2px_4px_rgba(255,255,255,0.6)]">
                        {product.ingredients[0]}
                      </div>
                    </div>
                  )}
                </div>
                <div className="mt-8 pt-6 border-t border-white/60 flex items-center justify-start">
                  <Link to={`/products/${product.id}`} className="flex items-center gap-2 px-6 py-3 bg-[#0A2540] text-white font-bold text-xs uppercase tracking-widest rounded-lg shadow-lg hover:shadow-xl hover:bg-[#113255] hover:-translate-y-0.5 transition-all duration-300">
                    <span>View Clinical Profile</span>
                    <ArrowRight className="h-4 w-4" />
                  </Link>
                </div>
              </div>
            </motion.div>
          ))}
        </div>
        )}
        
        {filteredProducts.length === 0 && (
          <div className="text-center py-20 text-[var(--color-text-muted)]">
            No products found matching your search.
          </div>
        )}
      </div>
    </div>
  );
};

export default Products;
