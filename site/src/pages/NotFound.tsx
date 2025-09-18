import { useSearchParams } from "react-router-dom";
import TitleBar from "../components/TitleBar";

export default function NotFound() {
  const [searchParams] = useSearchParams();
  const isMoe = searchParams.has("moe");

  return (
    <>
      <TitleBar />
      <div
        className={`${isMoe ? "bg-pink-100 text-pink-900 font-[Zen_Maru_Gothic]" : "bg-gray-950 text-white"} min-h-screen py-6 flex items-center justify-center`}
      >
        <div className="max-w-[600px] mx-auto px-4 text-center">
          <div
            className={`${isMoe ? "bg-pink-200 text-pink-900" : "bg-gray-800 text-white"} rounded-lg p-8 shadow-lg`}
          >
            <h1 className="text-6xl font-bold mb-4">404</h1>
            <h2 className="text-2xl font-semibold mb-4">Page Not Found</h2>
            <div className="mb-6">
              <img
                src="/liris.webp"
                className="w-32 mx-auto mb-4 object-contain rounded-2xl opacity-50"
                alt="Not found"
              />
            </div>
            <p className="text-lg mb-6">
              The page you're looking for doesn't exist or has been moved.
            </p>
            <div className="space-y-3">
              <a
                href="/"
                className={`inline-block px-6 py-3 rounded-lg font-semibold transition-colors ${
                  isMoe
                    ? "bg-pink-500 text-white hover:bg-pink-600"
                    : "bg-purple-600 text-white hover:bg-purple-700"
                }`}
              >
                Go to Homepage
              </a>
              <div className="mt-4">
                <a
                  href="/games"
                  className={`${
                    isMoe ? "text-pink-600 hover:text-pink-800" : "text-blue-400 hover:text-blue-300"
                  } underline`}
                >
                  View All Games
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
}
