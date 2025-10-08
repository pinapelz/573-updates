import { useTranslation } from 'react-i18next';
import { useSearchParams } from 'react-router-dom';
import { useRef, useState, useEffect } from 'react';

const languages = [
  { code: 'en', name: 'English' },
  { code: 'ja', name: '日本語' }
];

const LanguageSwitcher = () => {
  const { i18n } = useTranslation();
  const [searchParams] = useSearchParams();
  const isMoe = searchParams.has("moe");
  const [isOpen, setIsOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  const currentLanguage = languages.find(lang => lang.code === i18n.language) || languages[0];

  // Close the dropdown when clicking outside
  useEffect(() => {
    const handleClickOutside = (event: MouseEvent) => {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setIsOpen(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);

  return (
    <div className="relative inline-block" ref={dropdownRef}>
      <button
        onClick={() => setIsOpen(!isOpen)}
        className={`
          flex items-center justify-between
          transition-all duration-200 text-sm rounded
          px-2 py-0.5 min-w-[80px]
          ${isMoe
            ? 'bg-pink-200 text-pink-800 hover:bg-pink-300'
            : 'bg-gray-800 text-gray-300 hover:bg-gray-700 hover:text-white'
          }
        `}
        aria-haspopup="true"
        aria-expanded={isOpen}
      >
        <span>{currentLanguage.name}</span>
        <span className="ml-1">
          <svg
            className={`h-4 w-4 transition-transform ${isOpen ? 'rotate-180' : ''}`}
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M19 9l-7 7-7-7"
            />
          </svg>
        </span>
      </button>

      {isOpen && (
        <div
          className={`
            absolute right-0 mt-1 z-10 shadow-lg rounded-md overflow-hidden w-24
            ${isMoe ? 'bg-pink-100 border border-pink-300' : 'bg-gray-800 border border-gray-700'}
          `}
        >
          <div className="py-1">
            {languages.map((lang) => (
              <button
                key={lang.code}
                onClick={() => {
                  i18n.changeLanguage(lang.code);
                  setIsOpen(false);
                }}
                className={`
                  block w-full text-left px-4 py-2 text-sm
                  ${i18n.language === lang.code
                    ? isMoe
                      ? 'bg-pink-300 text-pink-800 font-medium'
                      : 'bg-purple-700 text-white font-medium'
                    : isMoe
                      ? 'text-pink-800 hover:bg-pink-200'
                      : 'text-gray-300 hover:bg-gray-700 hover:text-white'
                  }
                `}
              >
                {lang.name}
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default LanguageSwitcher;
