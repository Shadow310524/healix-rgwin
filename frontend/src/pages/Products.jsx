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
    <div className="py-12 bg-[var(--color-surface)] min-h-screen">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex flex-col md:flex-row justify-between items-center mb-12">
          <div>
            <h1 className="text-3xl font-bold text-[var(--color-text-main)] mb-2">Our Products</h1>
            <p className="text-[var(--color-text-muted)]">Explore the Healix range of healthcare solutions.</p>
          </div>
          
          <div className="mt-6 md:mt-0 flex gap-4 w-full md:w-auto">
            <div className="relative w-full md:w-64">
              <input 
                type="text" 
                placeholder="Search products..." 
                className="input-field pl-10"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
              />
              <Search className="absolute left-3 top-2.5 h-5 w-5 text-gray-400" />
            </div>
            <button className="btn-secondary flex items-center gap-2">
              <Filter className="h-4 w-4" /> Filter
            </button>
          </div>
        </div>

        <div className="flex gap-2 overflow-x-auto mb-8 pb-2">
          {categories.map(cat => (
            <button 
              key={cat} 
              onClick={() => setSelectedCategory(cat)}
              className={`px-4 py-2 rounded-full whitespace-nowrap ${selectedCategory === cat ? 'bg-[var(--color-primary)] text-white' : 'bg-gray-100 text-gray-700 hover:bg-gray-200'}`}
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
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, margin: "-20px" }}
              transition={{ duration: 0.5, delay: idx * 0.05 }}
              className="flex flex-col sm:flex-row h-full overflow-hidden bg-white border-y border-slate-200 sm:border sm:rounded-sm shadow-sm hover:shadow-md transition-shadow duration-300 group"
            >
              <div className="w-full sm:w-2/5 h-64 sm:h-auto overflow-hidden relative p-8 bg-slate-50/50 border-b sm:border-b-0 sm:border-r border-slate-200 flex items-center justify-center">
                <img 
                  src={product.image_url} 
                  alt={product.name} 
                  className="max-w-full max-h-full object-contain mix-blend-multiply transition-transform duration-500 group-hover:scale-105" 
                />
              </div>
              <div className="flex-grow p-8 flex flex-col justify-between bg-white w-full sm:w-3/5">
                <div>
                  <span className="text-[10px] font-bold text-[#0A2540] uppercase tracking-[0.15em] border-b-2 border-[#0A2540] pb-1 inline-block">{product.category?.name || 'Uncategorized'}</span>
                  <h3 className="text-3xl font-extrabold text-[#0A2540] mt-5 mb-4 leading-tight tracking-tight">{product.name}</h3>
                  
                  {product.ingredients && product.ingredients.length > 0 && (
                    <div className="mt-8">
                      <div className="text-[10px] font-bold text-slate-500 uppercase tracking-widest mb-2 flex items-center gap-2">
                        <svg className="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19.428 15.428a2 2 0 00-1.022-.547l-2.387-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z"></path></svg>
                        Active Composition
                      </div>
                      <div className="text-sm font-semibold text-slate-800 p-4 bg-slate-50 border border-slate-200 rounded-sm">
                        {product.ingredients[0]}
                      </div>
                    </div>
                  )}
                </div>
                <div className="mt-8 pt-6 border-t border-slate-100 flex items-center justify-start">
                  <Link to={`/products/${product.id}`} className="flex items-center gap-2 px-6 py-3 bg-[#0A2540] text-white font-bold text-xs uppercase tracking-widest rounded-sm hover:bg-blue-800 transition-colors duration-200">
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
