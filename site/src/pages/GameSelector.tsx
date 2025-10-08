import { Link, useSearchParams } from "react-router-dom";
import TitleBar from "../components/TitleBar";
import { useTranslation } from "react-i18next";

interface GameCategory {
  name: string;
  description: string;
  games: { id: string; title: string }[];
}

const gameInfo: GameCategory[] = [
  {
    name: "KONAMI",
    description: "",
    games: [
      { id: "iidx", title: "beatmania IIDX" },
      { id: "sdvx", title: "SOUND VOLTEX" },
      { id: "ddr", title: "DanceDanceRevolution" },
      { id: "jubeat", title: "jubeat" },
      { id: "popn_music", title: "pop'n music" },
      { id: "nostalgia", title: "NOSTALGIA" },
      { id: "gitadora", title: "GITADORA" },
      { id: "dance_rush", title: "DANCERUSH" },
      { id: "dance_around", title: "DANCE aROUND" },
      { id: "polaris_chord", title: "POLARIS CHORD" },
    ],
  },
  {
    name: "SEGA",
    description: "",
    games: [
      { id: "chunithm_jp", title: "CHUNITHM (JAPAN)" },
      { id: "chunithm_intl", title: "CHUNITHM (INTERNATIONAL)" },
      { id: "maimaidx_jp", title: "maimai DX (JAPAN)" },
      { id: "maimaidx_intl", title: "maimai DX (INTERNATIONAL)" },
      { id: "ongeki_jp", title: "O.N.G.E.K.I" },
      { id: "idac", title: "INITIAL D (頭文字D)" },
    ],
  },
  {
    name: "TAITO",
    description: "",
    games: [
      { id: "music_diver", title: "MUSIC DIVER" },
      { id: "street_fighter", title: "STREET FIGHTER" },
    ],
  },
  {
    name: "BANDAI NAMCO",
    description: "",
    games: [
      { id: "taiko", title: "Taiko no Tatsujin" },
      { id: "wmmt", title: "WANGAN MIDNIGHT MAXIMUM TUNE" },
    ],
  },
  {
    name: "COMMUNITY",
    description:
      "Community-driven projects to continue the legacy of dead/abandoned rhythm games",
    games: [
      { id: "wacca_plus", title: "WACCA PLUS" },
      { id: "museca_plus", title: "MÚSECA PLUS" },
      { id: "rb_deluxe_plus", title: "REFLEC BEAT DELUXE PLUS" },
    ],
  },
];

const GameSelector = () => {
  const [searchParams] = useSearchParams();
  const isMoe = searchParams.has("moe");
  const { t } = useTranslation();

  const renderCategory = (category: GameCategory) => (
    <div key={category.name} className="mb-6">
      <h2
        className={`text-lg font-bold ${isMoe ? "text-pink-700" : "text-gray-200"}`}
      >
        {t(`gameselector.categories.${category.name.toLowerCase().replace(' ', '_')}`)}
      </h2>
      <p
        className={`text-sm ${isMoe ? "text-pink-600" : "text-gray-400"} mb-2`}
      >
        {category.name === "COMMUNITY" ? t('gameselector.community_description') : category.description}
      </p>
      <div className="grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 gap-2 mt-2">
        {category.games.map((game) => (
          <Link
            key={game.id}
            to={`/game/${game.id}?${searchParams.toString()}`}
            className={`block px-3 py-2 rounded text-sm font-medium text-center truncate ${isMoe ? "bg-pink-100 text-pink-800 hover:bg-pink-200" : "bg-gray-800 text-white hover:bg-gray-700"} sm:px-4 sm:py-3`}
          >
            {game.title}
          </Link>
        ))}
      </div>
    </div>
  );

  return (
    <>
      <TitleBar />
      <div
        className={`min-h-screen px-4 py-6 ${isMoe ? "bg-pink-50" : "bg-gray-900"} sm:px-6 sm:py-8`}
      >
        <div className="max-w-[1200px] mx-auto">
          <h1
            className={`text-2xl font-bold mb-4 ${isMoe ? "text-pink-800" : "text-white"} sm:mb-6`}
          >
            {t('gameselector.title')}
          </h1>
          <h2
            className={`text-base font-medium ${isMoe ? "text-pink-700" : "text-gray-300"} mb-4`}
          >
            {t('gameselector.subtitle')}
          </h2>
          {gameInfo.map(renderCategory)}
        </div>
      </div>
    </>
  );
};

export default GameSelector;
