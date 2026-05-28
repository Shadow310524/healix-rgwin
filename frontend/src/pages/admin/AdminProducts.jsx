import { useState, useEffect } from 'react';
import { Package, Plus, Edit, Trash2, X, Upload, Image as ImageIcon } from 'lucide-react';
import toast from 'react-hot-toast';
import { productService, categoryService, uploadService } from '../../services/api';

const AdminProducts = () => {
  const [products, setProducts] = useState([]);
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [imageFile, setImageFile] = useState(null);
  const [imagePreview, setImagePreview] = useState(null);
  
  const [newProduct, setNewProduct] = useState({
    name: '', price: '', mrp: '', category_id: '', description: ''
  });

  useEffect(() => {
    loadData();
  }, []);

  const loadData = async () => {
    try {
      const [prodData, catData] = await Promise.all([
        productService.getProducts(),
        categoryService.getCategories()
      ]);
      setProducts(prodData);
      setCategories(catData);
    } catch (error) {
      console.error("Failed to load data", error);
      toast.error('Failed to load products');
    } finally {
      setLoading(false);
    }
  };

  const handleImageChange = (e) => {
    const file = e.target.files[0];
    if (file) {
      setImageFile(file);
      const reader = new FileReader();
      reader.onloadend = () => {
        setImagePreview(reader.result);
      };
      reader.readAsDataURL(file);
    }
  };

  const handleCreateProduct = async (e) => {
    e.preventDefault();
    if (!imageFile) {
      toast.error("Please select an image");
      return;
    }
    
    setIsSubmitting(true);
    try {
      // 1. Upload image to Cloudinary
      toast.loading("Uploading image...", { id: "upload-toast" });
      const uploadRes = await uploadService.uploadImage(imageFile);
      const imageUrl = uploadRes.url;
      toast.dismiss("upload-toast");

      // 2. Create product
      const created = await productService.createProduct({
        ...newProduct,
        image_url: imageUrl,
        category_id: parseInt(newProduct.category_id)
      });
      
      const categoryObj = categories.find(c => c.id === parseInt(newProduct.category_id));
      const productWithCat = { ...created, category: categoryObj };
      
      setProducts([...products, productWithCat]);
      toast.success('Product created successfully!');
      
      // Reset form
      setIsModalOpen(false);
      setNewProduct({ name: '', price: '', mrp: '', category_id: '', description: '' });
      setImageFile(null);
      setImagePreview(null);
    } catch (error) {
      toast.dismiss("upload-toast");
      console.error(error);
      toast.error('Failed to create product');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div>
      <div className="flex justify-between items-center mb-6">
        <h2 className="text-2xl font-bold text-[var(--color-text-main)]">Manage Products</h2>
        <button 
          onClick={() => setIsModalOpen(true)}
          className="btn-primary flex items-center gap-2"
        >
          <Plus className="h-4 w-4" /> Add Product
        </button>
      </div>

      <div className="bg-white rounded-xl shadow-sm border border-[var(--color-border)] overflow-hidden">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Product</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Category</th>
              <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">Price</th>
              <th className="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase tracking-wider">Actions</th>
            </tr>
          </thead>
          <tbody className="bg-white divide-y divide-gray-200">
            {loading ? (
              <tr>
                <td colSpan="4" className="px-6 py-8 text-center text-gray-500">
                  Loading products...
                </td>
              </tr>
            ) : products.length === 0 ? (
              <tr>
                <td colSpan="4" className="px-6 py-8 text-center text-gray-500">
                  No products found.
                </td>
              </tr>
            ) : (
              products.map(product => (
                <tr key={product.id}>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <div className="flex items-center">
                      <div className="h-10 w-10 flex-shrink-0">
                        <img className="h-10 w-10 rounded-md object-cover border border-gray-200" src={product.image_url} alt="" />
                      </div>
                      <div className="ml-4">
                        <div className="text-sm font-medium text-gray-900">{product.name}</div>
                      </div>
                    </div>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap">
                    <span className="px-2 inline-flex text-xs leading-5 font-semibold rounded-full bg-blue-100 text-blue-800">
                      {product.category?.name || 'Uncategorized'}
                    </span>
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                    {product.price}
                  </td>
                  <td className="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                    <button className="text-indigo-600 hover:text-indigo-900 mr-3">
                      <Edit className="h-4 w-4" />
                    </button>
                    <button className="text-red-600 hover:text-red-900">
                      <Trash2 className="h-4 w-4" />
                    </button>
                  </td>
                </tr>
              ))
            )}
          </tbody>
        </table>
      </div>

      {isModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/50 p-4">
          <div className="bg-white rounded-xl shadow-xl w-full max-w-2xl overflow-hidden max-h-[90vh] flex flex-col">
            <div className="flex justify-between items-center p-6 border-b border-[var(--color-border)] shrink-0">
              <h3 className="text-lg font-bold text-[var(--color-text-main)]">Add New Product</h3>
              <button onClick={() => {
                setIsModalOpen(false);
                setImagePreview(null);
                setImageFile(null);
              }} className="text-gray-400 hover:text-gray-600">
                <X className="h-5 w-5" />
              </button>
            </div>
            <form onSubmit={handleCreateProduct} className="p-6 overflow-y-auto">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <label className="block text-sm font-medium text-[var(--color-text-main)] mb-2">Product Name</label>
                  <input 
                    type="text" required className="input-field"
                    value={newProduct.name} onChange={(e) => setNewProduct({...newProduct, name: e.target.value})}
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-[var(--color-text-main)] mb-2">Category</label>
                  <select 
                    required className="input-field bg-white"
                    value={newProduct.category_id} onChange={(e) => setNewProduct({...newProduct, category_id: e.target.value})}
                  >
                    <option value="" disabled>Select a category</option>
                    {categories.map(cat => (
                      <option key={cat.id} value={cat.id}>{cat.name}</option>
                    ))}
                  </select>
                </div>
                <div>
                  <label className="block text-sm font-medium text-[var(--color-text-main)] mb-2">Price Label</label>
                  <input 
                    type="text" required className="input-field" placeholder="e.g. Enquire"
                    value={newProduct.price} onChange={(e) => setNewProduct({...newProduct, price: e.target.value})}
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-[var(--color-text-main)] mb-2">MRP (Maximum Retail Price)</label>
                  <input 
                    type="text" className="input-field" placeholder="e.g. ₹500"
                    value={newProduct.mrp} onChange={(e) => setNewProduct({...newProduct, mrp: e.target.value})}
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-[var(--color-text-main)] mb-2">Product Image</label>
                  <div className="flex items-center justify-center w-full">
                    <label className="flex flex-col items-center justify-center w-full h-32 border-2 border-dashed border-gray-300 rounded-lg cursor-pointer bg-gray-50 hover:bg-gray-100 overflow-hidden relative">
                      {imagePreview ? (
                        <img src={imagePreview} alt="Preview" className="w-full h-full object-cover" />
                      ) : (
                        <div className="flex flex-col items-center justify-center pt-5 pb-6">
                          <Upload className="w-8 h-8 mb-2 text-gray-400" />
                          <p className="text-sm text-gray-500"><span className="font-semibold">Click to upload</span></p>
                        </div>
                      )}
                      <input 
                        type="file" className="hidden" accept="image/*"
                        onChange={handleImageChange} required
                      />
                    </label>
                  </div>
                </div>
                <div className="md:col-span-2">
                  <label className="block text-sm font-medium text-[var(--color-text-main)] mb-2">Description</label>
                  <textarea 
                    rows="3" required className="input-field"
                    value={newProduct.description} onChange={(e) => setNewProduct({...newProduct, description: e.target.value})}
                  />
                </div>
              </div>
              <div className="flex justify-end gap-3 mt-8">
                <button 
                  type="button" onClick={() => setIsModalOpen(false)}
                  className="px-4 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 hover:bg-gray-50"
                >
                  Cancel
                </button>
                <button 
                  type="submit" disabled={isSubmitting}
                  className="btn-primary disabled:opacity-50"
                >
                  {isSubmitting ? 'Creating...' : 'Create Product'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default AdminProducts;
