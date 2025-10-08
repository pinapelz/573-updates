import i18n from 'i18next';
import { initReactI18next } from 'react-i18next';
import LanguageDetector from 'i18next-browser-languagedetector';
import Backend from 'i18next-http-backend';
import { updateHtmlLang } from './utils';

i18n
  .use(Backend)
  .use(LanguageDetector)
  .use(initReactI18next)
  .init({
    fallbackLng: 'en',
    backend: {
      loadPath: '/locales/{{lng}}/{{ns}}.json',
    },

    interpolation: {
      escapeValue: false,
    }
  });

// Set the HTML lang attribute when language changes
i18n.on('languageChanged', (lng) => {
  updateHtmlLang(lng);
});

// Initialize HTML lang with the current language
updateHtmlLang(i18n.language);

export default i18n;
