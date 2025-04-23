export const getGameTitle = (gameId: string) => {
    if (!gameId) return null;

    const lowerCaseGameId = gameId.toLowerCase();

    if (lowerCaseGameId.startsWith("sdvx") || lowerCaseGameId.startsWith("sound_voltex")) return "SOUND VOLTEX";
    if (lowerCaseGameId.startsWith("iidx")) return "beatmania IIDX";
    if (lowerCaseGameId.startsWith("chunithm_jp")) return "CHUNITHM (JAPAN)";
    if (lowerCaseGameId.startsWith("maimaidx_jp")) return "maimai DX (JAPAN)";
    if (lowerCaseGameId.startsWith("maimaidx_intl")) return "maimai DX (INTERNATIONAL)";
    if (lowerCaseGameId.startsWith("ongeki_jp")) return "O.N.G.E.K.I"
    if (lowerCaseGameId.startsWith("chunithm_intl")) return "CHUNITHM (INTERNATIONAL)"
    if (lowerCaseGameId.startsWith("ddr")) return "DanceDanceRevolution";
    if (lowerCaseGameId.startsWith("jubeat")) return "jubeat";
    if (lowerCaseGameId.startsWith("gitadora")) return "GITADORA";
    if (lowerCaseGameId.startsWith("nostalgia")) return "NOSTALGIA";
    if (lowerCaseGameId.startsWith("popn_music")) return "pop'n music";
    if (lowerCaseGameId.startsWith("music_diver")) return "MUSIC DIVER";
    if (lowerCaseGameId.startsWith("taiko")) return "Taiko no Tatsujin";
    if (lowerCaseGameId.startsWith("wacca")) return "WACCA PLUS";
    if (lowerCaseGameId.startsWith("museca")) return "MÚSECA PLUS";


    return gameId.toUpperCase();
};
