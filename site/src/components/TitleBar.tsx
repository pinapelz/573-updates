import { useEffect } from "react";
import {
  Link,
  useSearchParams,
  useNavigate,
  useLocation,
} from "react-router-dom";
import LanguageSwitcher from "./LanguageSwitcher";
import { useTranslation } from "react-i18next";

const TitleBar: React.FC = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const location = useLocation();
  const isMoe = searchParams.has("moe");
  const { t } = useTranslation();

  const toggleTheme = () => {
    const params = new URLSearchParams(searchParams);

    if (isMoe) {
      params.delete("moe");
      localStorage.setItem("theme", "dark");
    } else {
      params.set("moe", "");
      localStorage.setItem("theme", "light");
    }

    navigate(`${location.pathname}?${params.toString()}`);
  };

  useEffect(() => {
    const savedTheme = localStorage.getItem("theme");

    const hasMoe = searchParams.has("moe");

    if (!hasMoe && savedTheme === "light") {
      const params = new URLSearchParams(searchParams);
      params.set("moe", "");
      navigate(`${location.pathname}?${params.toString()}`, { replace: true });
    }

    if (hasMoe && savedTheme === "dark") {
      const params = new URLSearchParams(searchParams);
      params.delete("moe");
      navigate(`${location.pathname}?${params.toString()}`, { replace: true });
    }
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [location.pathname, navigate]);

  return (
    <div
      className={`${isMoe ? "bg-pink-200 border-pink-300" : "bg-gray-900 border-gray-800"} border-b py-4 px-6 font-[Zen_Maru_Gothic]`}
    >
      <div className="max-w-[800px] mx-auto">
        <div className="flex flex-col sm:flex-row justify-between items-center">
          <div className="flex items-center space-x-3 mb-3 sm:mb-0">
            <button
              onClick={toggleTheme}
              className={`text-sm ${isMoe ? "bg-pink-100 text-pink-800 hover:bg-pink-200 hover:text-pink-600" : "bg-gray-800 text-gray-300 hover:bg-gray-700 hover:text-white"} font-medium px-3 py-1 rounded`}
            >
              {isMoe ? "🌙 "+t('dark_theme_text') : "🌸 "+t("light_theme_text")}
            </button>
            <img
              src="/rasis.webp"
              alt="573 Updates Logo"
              className="w-8 h-8 object-contain rounded-full"
            />
            <div
              className={`${isMoe ? "bg-pink-500" : "bg-red-700"} w-8 h-8 rounded-md flex items-center justify-center`}
            >
              <span className="text-white font-bold">573</span>
            </div>
            <Link
              to={`/${isMoe ? "?moe" : ""}`}
              className={`${isMoe ? "text-pink-800" : "text-white"} text-xl font-bold`}
            >
              UPDATES
            </Link>
          </div>

          <div className="flex items-center space-x-2 sm:space-x-4">
            <Link
              to={`/${isMoe ? "?moe" : ""}`}
              className={`${isMoe ? "text-pink-800 hover:text-pink-600" : "text-gray-300 hover:text-white"} font-medium text-sm sm:text-base`}
            >
              {t('news_feed')}
            </Link>
            <Link
              to={`/games${isMoe ? "?moe" : ""}`}
              className={`${isMoe ? "text-pink-800 hover:text-pink-600" : "text-gray-300 hover:text-white"} font-medium text-sm sm:text-base`}
            >
              {t('game_selector')}
            </Link>
            <LanguageSwitcher />
          </div>
        </div>
      </div>
    </div>
  );
};

export default TitleBar;
