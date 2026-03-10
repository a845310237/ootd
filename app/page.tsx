import Link from "next/link"

export default function Home() {
  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="container mx-auto px-4 py-16">
        <div className="text-center">
          <h1 className="text-5xl font-bold text-gray-900 mb-4">
            穿搭AI
          </h1>
          <p className="text-xl text-gray-600 mb-8">
            智能穿搭助手，为你打造个性化穿搭方案
          </p>

          <div className="grid md:grid-cols-3 gap-6 max-w-4xl mx-auto mt-12">
            <Link
              href="/auth/login"
              className="bg-white p-6 rounded-xl shadow-lg hover:shadow-xl transition-shadow"
            >
              <div className="text-4xl mb-4">👔</div>
              <h3 className="text-lg font-semibold mb-2">管理衣柜</h3>
              <p className="text-gray-600 text-sm">数字化你的衣物，轻松管理每一件单品</p>
            </Link>

            <Link
              href="/auth/login"
              className="bg-white p-6 rounded-xl shadow-lg hover:shadow-xl transition-shadow"
            >
              <div className="text-4xl mb-4">🤖</div>
              <h3 className="text-lg font-semibold mb-2">AI智能搭配</h3>
              <p className="text-gray-600 text-sm">基于你的特征和场合，AI生成专属穿搭建议</p>
            </Link>

            <Link
              href="/auth/login"
              className="bg-white p-6 rounded-xl shadow-lg hover:shadow-xl transition-shadow"
            >
              <div className="text-4xl mb-4">✨</div>
              <h3 className="text-lg font-semibold mb-2">DIY穿搭</h3>
              <p className="text-gray-600 text-sm">自由组合衣物，创建属于你的独特风格</p>
            </Link>
          </div>

          <div className="mt-12">
            <Link
              href="/auth/register"
              className="inline-block bg-blue-600 text-white px-8 py-3 rounded-lg font-semibold hover:bg-blue-700 transition-colors"
            >
              立即开始
            </Link>
          </div>
        </div>
      </div>
    </div>
  )
}
