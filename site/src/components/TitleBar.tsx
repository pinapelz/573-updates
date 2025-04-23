import { useState, useEffect, useRef } from "react";
import {
  Link,
  useSearchParams,
  useNavigate,
  useLocation,
} from "react-router-dom";

interface GameCategory {
  name: string;
  games: { id: string; title: string }[];
}
const TitleBar: React.FC = () => {
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const location = useLocation();
  const isMoe = searchParams.has("moe");

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


  const gameCategories: GameCategory[] = [
    {
      name: "KONAMI",
      games: [
        { id: "iidx", title: "beatmania IIDX" },
        { id: "sdvx", title: "SOUND VOLTEX" },
        { id: "ddr", title: "DDR" },
        { id: "jubeat", title: "jubeat" },
        { id: "popn_music", title: "pop'n music" },
        { id: "nostalgia", title: "NOSTALGIA" },
        { id: "gitadora", title: "GITADORA" },
      ],
    },
    {
      name: "SEGA",
      games: [
        { id: "chunithm_jp", title: "CHUNITHM (JAPAN)" },
        { id: "chunithm_intl", title: "CHUNITHM (INTL)" },
        { id: "maimaidx_jp", title: "maimai DX (JAPAN)" },
        { id: "maimaidx_intl", title: "maimai DX (INTL)" },
        { id: "ongeki_jp", title: "O.N.G.E.K.I" },
      ],
    },
    {
      name: "TAITO",
      games: [{ id: "music_diver", title: "MUSIC DIVER" }],
    },
    {
      name: "BANDAI NAMCO",
      games: [{ id: "taiko", title: "TAIKO" }],
    },
    {
      name: "COMMUNITY",
      games: [
        { id: "wacca_plus", title: "WACCA PLUS" },
        { id: "museca_plus", title: "MÚSECA PLUS" },
      ],
    },
  ];

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (
        dropdownRef.current &&
        !dropdownRef.current.contains(event.target as Node)
      ) {
        setDropdownOpen(false);
      }
    };
    if (dropdownOpen)
      document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, [dropdownOpen]);

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
              {isMoe ? "🌙 Dark" : "🌸 Light"}
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

          <div className="flex items-center space-x-4">
            <Link
              to={`/${isMoe ? "?moe" : ""}`}
              className={`${isMoe ? "text-pink-800 hover:text-pink-600" : "text-gray-300 hover:text-white"} font-medium`}
            >
              All Games
            </Link>

            <div className="relative" ref={dropdownRef}>
              <button
                className={`${isMoe ? "text-pink-800 hover:text-pink-600" : "text-gray-300 hover:text-white"} font-medium flex items-center`}
                onClick={() => setDropdownOpen(!dropdownOpen)}
              >
                Game Select
                <svg
                  className="w-4 h-4 ml-1"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M19 9l-7 7-7-7"
                  />
                </svg>
              </button>

              {dropdownOpen && (
                <div
                  className={`absolute mt-2 w-64 sm:w-80 ${isMoe ? "bg-pink-100 border-pink-300" : "bg-gray-800 border-gray-700"} border rounded-md shadow-lg z-10 right-0`}
                >
                  <div className="py-1 max-h-[70vh] overflow-y-auto scroll-py-2">
                    {gameCategories.map((category, index) => (
                      <div key={index} className="px-2 py-1">
                        <div
                          className={`${isMoe ? "text-pink-600 border-pink-300" : "text-gray-400 border-gray-700"} text-sm font-semibold mb-1 border-b pb-1`}
                        >
                          {category.name}
                        </div>
                        <div
                          className={`${category.games.length > 3 ? "grid grid-cols-1 sm:grid-cols-2 gap-x-2 gap-y-0.5" : "space-y-0.5"}`}
                        >
                          {category.games.map((game) => (
                            <Link
                              key={game.id}
                              to={`/game/${game.id}?${searchParams.toString()}`}
                              className={`${isMoe ? "text-pink-800 hover:bg-pink-200" : "text-gray-300 hover:bg-gray-700 hover:text-white"} block text-left px-2 py-1 text-sm rounded whitespace-nowrap overflow-hidden text-ellipsis`}
                              onClick={() => setDropdownOpen(false)}
                            >
                              {game.title}
                            </Link>
                          ))}
                        </div>
                      </div>
                    ))}
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TitleBar;
