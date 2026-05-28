import { useParams, Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { ArrowLeft, MessageSquare, Shield, Activity } from 'lucide-react';
import { useState, useEffect } from 'react';
import { productService } from '../services/api';

const ProductDetails = () => {
  const { id } = useParams();
  const [product, setProduct] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchProduct = async () => {
      try {
        const products = await productService.getProducts();
        const found = products.find(p => p.id === parseInt(id));
        setProduct(found);
      } catch (error) {
        console.error("Error fetching product details", error);
      } finally {
        setLoading(false);
      }
    };
    fetchProduct();
  }, [id]);

  if (loading) {
    return (
      <div className="py-20 text-center">Loading product details...</div>
    );
  }

  if (!product) {
    return (
      <div className="py-20 text-center">
        <h2 className="text-2xl font-bold mb-4">Product not found</h2>
        <Link to="/products" className="text-[var(--color-primary)] hover:underline">
          Return to Products
        </Link>
      </div>
    );
  }

  // Parse strings into arrays if they exist
  const benefits = product.benefits ? product.benefits.split(',').map(b => b.trim()) : [];
  const ingredients = product.ingredients ? product.ingredients.split(',').map(i => i.trim()) : [];

  return (
    <div className="py-12 bg-white min-h-screen">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <Link to="/products" className="inline-flex items-center text-[var(--color-text-muted)] hover:text-[var(--color-primary)] mb-8 transition-colors">
          <ArrowLeft className="h-4 w-4 mr-2" /> Back to Products
        </Link>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-12">
          <motion.div
            initial={{ opacity: 0, x: -30 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5 }}
          >
            <div className="rounded-2xl overflow-hidden shadow-lg border border-[var(--color-border)] bg-gray-50 h-96 md:h-[500px]">
              <img src={product.image_url} alt={product.name} className="w-full h-full object-cover" />
            </div>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, x: 30 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.5, delay: 0.2 }}
            className="flex flex-col justify-center"
          >
            <span className="inline-block px-3 py-1 bg-[var(--color-primary-light)] text-[var(--color-primary)] rounded-full text-sm font-semibold mb-4 w-fit uppercase tracking-wider">
              {product.category?.name || 'Uncategorized'}
            </span>
            <h1 className="text-4xl font-bold text-[var(--color-text-main)] mb-2">{product.name}</h1>
            <p className="text-3xl font-bold text-[var(--color-primary)] mb-6">
              {product.price}
              {product.mrp && <span className="text-xl text-gray-400 line-through ml-3">{product.mrp}</span>}
            </p>
            
            <p className="text-lg text-[var(--color-text-muted)] mb-8 leading-relaxed">
              {product.description}
            </p>

            <div className="grid grid-cols-2 gap-4 mb-8">
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-full bg-[var(--color-primary-light)] flex items-center justify-center text-[var(--color-primary)]">
                  <Shield className="h-5 w-5" />
                </div>
                <span className="text-sm font-medium text-[var(--color-text-main)]">Clinically Tested</span>
              </div>
              <div className="flex items-center gap-3">
                <div className="w-10 h-10 rounded-full bg-[var(--color-primary-light)] flex items-center justify-center text-[var(--color-primary)]">
                  <Activity className="h-5 w-5" />
                </div>
                <span className="text-sm font-medium text-[var(--color-text-main)]">High Efficacy</span>
              </div>
            </div>

            <div className="mb-8">
              <h3 className="text-lg font-bold text-[var(--color-text-main)] mb-3">Key Benefits</h3>
              <ul className="list-disc pl-5 space-y-2 text-[var(--color-text-muted)]">
                {benefits.map((benefit, idx) => (
                  <li key={idx}>{benefit}</li>
                ))}
              </ul>
            </div>

            <div className="mb-8">
              <h3 className="text-lg font-bold text-[var(--color-text-main)] mb-3">Active Ingredients</h3>
              <div className="flex flex-wrap gap-2">
                {ingredients.map((ingredient, idx) => (
                  <span key={idx} className="px-3 py-1 bg-gray-100 text-gray-700 rounded-full text-sm">
                    {ingredient}
                  </span>
                ))}
              </div>
            </div>

            <Link to={`/contact?product=${encodeURIComponent(product.name)}`} className="btn-primary flex items-center justify-center gap-2 w-full md:w-auto py-3 text-lg">
              <MessageSquare className="h-5 w-5" /> Enquire Now
            </Link>
          </motion.div>
        </div>
      </div>
    </div>
  );
};

export default ProductDetails;
