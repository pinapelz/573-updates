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
<<<<<<< Updated upstream
    if (lowerCaseGameId.startsWIth("ddr")) return "DanceDanceRevolution"
=======
    if (lowerCaseGameId.startsWith("ddr")) return "DanceDanceRevolution"
>>>>>>> Stashed changes

    return gameId.toUpperCase();
};
