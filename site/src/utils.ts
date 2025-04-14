export const getGameTitle = (gameId: string) => {
    if (!gameId) return null;

    const lowerCaseGameId = gameId.toLowerCase();

    if (lowerCaseGameId.startsWith("sdvx")) return "SOUND VOLTEX";
    if (lowerCaseGameId.startsWith("iidx")) return "beatmania IIDX";
    if (lowerCaseGameId.startsWith("chunithm_jp")) return "CHUNITHM (JAPAN)";
    if (lowerCaseGameId.startsWith("maimaidx_jp")) return "maimai DX (JAPAN)";

    return gameId.toUpperCase();
};
