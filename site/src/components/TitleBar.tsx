import { Link } from 'react-router-dom';
import { useState, useEffect, useRef } from 'react';

interface GameCategory {
    name: string;
    games: { id: string; title: string }[];
}

const TitleBar: React.FC = () => {
    const [dropdownOpen, setDropdownOpen] = useState(false);
    const dropdownRef = useRef<HTMLDivElement>(null);

    const gameCategories: GameCategory[] = [
        {
            name: "KONAMI",
            games: [
                { id: "sdvx", title: "SOUND VOLTEX" },
                { id: "iidx", title: "beatmania IIDX" },
            ]
        },
        {
            name: "SEGA",
            games: [
                { id: "chunithm_jp", title: "CHUNITHM (JAPAN)" },
                { id: "maimaidx_jp", title: "maimai DX (JAPAN)" },
                { id: "maimaidx_intl", title: "maimai DX (INTERNATIONAL)"},
                { id: "ongeki_jp", title: "O.N.G.E.K.I"},
            ]
        }
    ];

    useEffect(() => {
        const handleClickOutside = (event: MouseEvent) => {
            if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
                setDropdownOpen(false);
            }
        };

        if (dropdownOpen) {
            document.addEventListener('mousedown', handleClickOutside);
        }

        return () => {
            document.removeEventListener('mousedown', handleClickOutside);
        };
    }, [dropdownOpen]);

    return (
        <div className="bg-gray-900 border-b border-gray-800 py-4 px-6">
            <div className="max-w-[800px] mx-auto">
                <div className="flex flex-col sm:flex-row justify-between items-center">
                  <div className="flex items-center space-x-3 mb-3 sm:mb-0">
                      <img
                          src="/rasis.webp"
                          alt="573 Updates Logo"
                          className="w-8 h-8 object-contain"
                      />
                        <div className="w-8 h-8 bg-red-700 rounded-md flex items-center justify-center">
                            <span className="text-white font-bold">573</span>
                        </div>

                        {/* Site Title */}
                        <Link to="/" className="text-xl font-bold text-white">
                            UPDATES
                        </Link>
                    </div>

                    {/* Navigation Section */}
                    <div className="flex items-center space-x-4">
                        <Link
                            to="/"
                            className="text-gray-300 hover:text-white font-medium"
                        >
                            All Games
                        </Link>

                        {/* Dropdown Menu */}
                        <div className="relative" ref={dropdownRef}>
                            <button
                                className="text-gray-300 hover:text-white font-medium flex items-center"
                                onClick={() => setDropdownOpen(!dropdownOpen)}
                            >
                                Game Select
                                <svg className="w-4 h-4 ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                                </svg>
                            </button>

                            {dropdownOpen && (
                                <div className="absolute right-0 mt-2 w-64 bg-gray-800 border border-gray-700 rounded-md shadow-lg z-10">
                                    <div className="py-1 max-h-[70vh] overflow-y-auto">
                                        {gameCategories.map((category, index) => (
                                            <div key={index} className="px-3 py-2">
                                                <div className="text-sm font-semibold text-gray-400 mb-1 border-b border-gray-700 pb-1">
                                                    {category.name}
                                                </div>
                                                <div className="space-y-1">
                                                    {category.games.map((game) => (
                                                        <Link
                                                            key={game.id}
                                                            to={`/game/${game.id}`}
                                                            className="block text-gray-300 hover:bg-gray-700 hover:text-white px-2 py-1 text-sm rounded"
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
