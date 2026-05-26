import { Outlet, Link, useNavigate, useLocation } from 'react-router-dom';
import { LayoutDashboard, Package, Tag, MessageSquare, LogOut, Pill } from 'lucide-react';
import { useAuth } from '../features/auth/AuthContext';

const AdminLayout = () => {
  const { logout } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const handleLogout = () => {
    logout();
    navigate('/admin/login');
  };

  const navItems = [
    { name: 'Dashboard', path: '/admin/dashboard', icon: LayoutDashboard },
    { name: 'Products', path: '/admin/products', icon: Package },
    { name: 'Categories', path: '/admin/categories', icon: Tag },
    { name: 'Enquiries', path: '/admin/enquiries', icon: MessageSquare },
  ];

  return (
    <div className="min-h-screen bg-[var(--color-surface)] flex">
      {/* Sidebar */}
      <aside className="w-64 bg-white border-r border-[var(--color-border)] flex flex-col">
        <div className="h-16 flex items-center px-6 border-b border-[var(--color-border)]">
          <Pill className="h-6 w-6 text-[var(--color-primary)] mr-2" />
          <span className="font-bold text-lg text-[var(--color-primary-dark)]">Healix Admin</span>
        </div>
        
        <nav className="flex-1 px-4 py-6 space-y-1">
          {navItems.map((item) => {
            const isActive = location.pathname.startsWith(item.path);
            return (
              <Link
                key={item.name}
                to={item.path}
                className={`flex items-center px-3 py-3 rounded-lg font-medium transition-colors ${
                  isActive 
                    ? 'bg-[var(--color-primary-light)] text-[var(--color-primary)]' 
                    : 'text-[var(--color-text-muted)] hover:bg-gray-50 hover:text-[var(--color-text-main)]'
                }`}
              >
                <item.icon className="h-5 w-5 mr-3" />
                {item.name}
              </Link>
            );
          })}
        </nav>
        
        <div className="p-4 border-t border-[var(--color-border)]">
          <button 
            onClick={handleLogout}
            className="flex items-center w-full px-3 py-2 text-[var(--color-text-muted)] hover:text-red-600 font-medium transition-colors rounded-lg hover:bg-red-50"
          >
            <LogOut className="h-5 w-5 mr-3" />
            Logout
          </button>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 overflow-y-auto">
        <header className="h-16 bg-white border-b border-[var(--color-border)] flex items-center px-8 shadow-sm">
          <h1 className="text-xl font-semibold text-[var(--color-text-main)]">Secure Administration Panel</h1>
        </header>
        <div className="p-8">
          <Outlet />
        </div>
      </main>
    </div>
  );
};

export default AdminLayout;
