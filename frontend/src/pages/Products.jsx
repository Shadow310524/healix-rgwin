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
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-8">
          {filteredProducts.map((product, idx) => (
            <motion.div 
              key={product.id}
              initial={{ opacity: 0, y: 50 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: true, margin: "-50px" }}
              transition={{ duration: 0.5, delay: idx * 0.1 }}
              whileHover={{ y: -5, scale: 1.02 }}
              className="card flex flex-col h-full border border-gray-100 hover:shadow-2xl transition-all duration-300 group"
            >
              <div className="h-56 rounded-t-lg overflow-hidden mb-4 bg-gray-100 relative">
                <div className="absolute inset-0 bg-black/5 group-hover:bg-transparent transition-colors z-10"></div>
                <img 
                  src={product.image_url} 
                  alt={product.name} 
                  className="w-full h-full object-cover transform group-hover:scale-110 transition-transform duration-700" 
                />
              </div>
              <div className="flex-grow p-5 pt-0">
                <span className="text-xs font-bold text-[var(--color-primary)] uppercase tracking-wider">{product.category?.name || 'Uncategorized'}</span>
                <h3 className="text-xl font-bold text-[var(--color-text-main)] mt-2 mb-2 group-hover:text-[var(--color-primary)] transition-colors">{product.name}</h3>
                <p className="text-sm text-[var(--color-text-muted)] mb-4 line-clamp-3 leading-relaxed">{product.description}</p>
              </div>
              <div className="flex items-center justify-between p-5 pt-0 mt-auto border-t border-gray-100">
                <span className="text-xl font-bold text-[var(--color-text-main)] mt-4">{product.price}</span>
                <Link to={`/products/${product.id}`} className="mt-4 p-2 bg-[var(--color-primary-light)] text-[var(--color-primary)] rounded-full hover:bg-[var(--color-primary)] hover:text-white transform group-hover:translate-x-1 transition-all">
                  <ArrowRight className="h-5 w-5" />
                </Link>
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
