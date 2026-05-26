import { useState, useEffect } from 'react';
import api from '../../services/api';

const AdminDashboard = () => {
  const [productCount, setProductCount] = useState(0);
  const [categoryCount, setCategoryCount] = useState(0);
  const [enquiryCount, setEnquiryCount] = useState(0);

  useEffect(() => {
    const fetchStats = async () => {
      try {
        const [productsRes, categoriesRes, enquiriesRes] = await Promise.all([
          api.get('/products/'),
          api.get('/categories/'),
          api.get('/enquiries/')
        ]);
        
        setProductCount(productsRes.data.length);
        setCategoryCount(categoriesRes.data.length);
        setEnquiryCount(enquiriesRes.data.length);
      } catch (error) {
        console.error("Error fetching dashboard stats:", error);
      }
    };
    fetchStats();
  }, []);

  return (
    <div>
      <h2 className="text-2xl font-bold text-[var(--color-text-main)] mb-6">Dashboard Overview</h2>
      
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <div className="bg-white p-6 rounded-xl shadow-sm border border-[var(--color-border)]">
          <h3 className="text-sm font-medium text-[var(--color-text-muted)] mb-1">Total Products</h3>
          <p className="text-3xl font-bold text-[var(--color-primary)]">{productCount}</p>
        </div>
        <div className="bg-white p-6 rounded-xl shadow-sm border border-[var(--color-border)]">
          <h3 className="text-sm font-medium text-[var(--color-text-muted)] mb-1">Total Categories</h3>
          <p className="text-3xl font-bold text-[var(--color-primary)]">{categoryCount}</p>
        </div>
        <div className="bg-white p-6 rounded-xl shadow-sm border border-[var(--color-border)]">
          <h3 className="text-sm font-medium text-[var(--color-text-muted)] mb-1">Total Enquiries</h3>
          <p className="text-3xl font-bold text-[var(--color-primary)]">{enquiryCount}</p>
        </div>
      </div>

      <div className="bg-white rounded-xl shadow-sm border border-[var(--color-border)] p-6">
        <h3 className="text-lg font-bold text-[var(--color-text-main)] mb-4">Recent Activity</h3>
        <p className="text-[var(--color-text-muted)]">No recent activity to display.</p>
      </div>
    </div>
  );
};

export default AdminDashboard;
