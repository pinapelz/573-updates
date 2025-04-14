export const getGameTitle = (gameId: string) => {
    if (!gameId) return null;

    if (gameId.startsWith("sdvx")) return "SOUND VOLTEX";
    if (gameId.startsWith("iidx")) return "beatmania IIDX";
    if (gameId.startsWith("chunithm_jp")) return "CHUNITHM (JAPAN)";
    if (gameId.startsWith("maimaidx_jp")) return "maimai DX (JAPAN)";

    return gameId.toUpperCase();
};
