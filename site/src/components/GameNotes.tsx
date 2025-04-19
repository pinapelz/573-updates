import React from "react";

export const GameNotes = (isMoe: boolean): Record<string, React.ReactNode> => ({
  sdvx: (
    <>
      <ul className={`mt-2 ${isMoe ? "text-pink-900" : "text-white"}`}>
        <li>• [USA] PREMIUM GENERATOR gacha available only ONLINE</li>
        <li>• VP/VOLTEFACTORY rewards only in Japan</li>
      </ul>
      <p className={`mt-3 ${isMoe ? "text-pink-800" : "text-pink-300"} text-right`}>
        Official e-amusement service in NA available only at Round1 USA
        <br />
        Cabinets in Canada/Europe/Australia are on non-official private networks which are running older data
      </p>
    </>
  ),
});
