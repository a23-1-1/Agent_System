import { Outlet, Link, useLocation } from 'react-router-dom'

const NAV = [
  { path: '/', label: '备课', desc: 'AI Studio' },
  { path: '/classroom', label: '课堂', desc: '演示播放' },
  { path: '/student/demo', label: '学生端', desc: '预览' },
]

export default function AppLayout() {
  const { pathname } = useLocation()

  return (
    <div className="min-h-screen bg-gray-50">
      {/* 顶部导航 */}
      <nav className="bg-white border-b border-gray-200 sticky top-0 z-50">
        <div className="max-w-7xl mx-auto px-4 flex items-center h-14 gap-6">
          <Link to="/" className="font-bold text-lg text-blue-600 whitespace-nowrap">
            DB Demo Studio
          </Link>

          <div className="flex items-center gap-1">
            {NAV.map(n => (
              <Link
                key={n.path}
                to={n.path}
                className={`px-3 py-1.5 rounded-lg text-sm font-medium transition-colors
                  ${pathname === n.path
                    ? 'bg-blue-50 text-blue-700'
                    : 'text-gray-600 hover:bg-gray-100'
                  }`}
              >
                {n.label}
              </Link>
            ))}
          </div>
        </div>
      </nav>

      {/* 页面内容 */}
      <Outlet />
    </div>
  )
}
