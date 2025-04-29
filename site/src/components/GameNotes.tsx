import React from "react";
import Popup from "reactjs-popup";

const EamuseMaintenancePopup: React.FC<{ isMoe: boolean }> = ({ isMoe }) => {
  return (
    <Popup
      trigger={
        <button
          className={`mt-4 rounded px-2 py-1 ${isMoe ? "bg-pink-300 text-pink-900 hover:bg-pink-400" : "bg-gray-500 text-white hover:bg-gray-400"}`}
        >
          e-amusement Maintenance
        </button>
      }
      position="center center"
      modal
      closeOnDocumentClick
    >
      <div
        className={`p-6 rounded-lg shadow-lg ${isMoe ? "bg-pink-100 text-pink-900" : "bg-gray-900 text-white"} max-w-md mx-auto`}
      >
        <div className="flex justify-between items-center mb-3">
          <h3 className="text-lg">e-amusement Maintenance Information</h3>
        </div>
        <div className="mb-4">
          <p className="font-bold">Regular Daily Maintenance</p>
          <p className="mt-1 font-semibold">
            Every day from 5:00 AM to 7:00 AM (JST)
          </p>
          <p className="mt-1 text-right">
            In your local time:{" "}
            {(() => {
              const jst5am = new Date();
              jst5am.setUTCHours(20, 0, 0, 0); // 5AM JST is 8PM UTC the day before
              const jst7am = new Date();
              jst7am.setUTCHours(22, 0, 0, 0); // 7AM JST is 10PM UTC the day before
              const options: Intl.DateTimeFormatOptions = {
                hour: "2-digit",
                minute: "2-digit",
                hour12: true,
              };
              return `${jst5am.toLocaleTimeString([], options)} to ${jst7am.toLocaleTimeString([], options)}`;
            })()}
          </p>
          <p>
            e-amusement website, at-home Konasute games offline, Japan + Asia
            cabinets offline. USA cabinets exempt
          </p>
          <p className="font-bold mt-4">Monthly Extended Maintenance</p>
          <p className="mt-1 font-semibold">
            Every Third Tuesday from 2:00 AM to 7:00 AM (JST)
          </p>
          <p className="mt-1 text-right">
            In your local time:{" "}
            {(() => {
              const jst2am = new Date();
              jst2am.setUTCHours(17, 0, 0, 0);
              const jst7am = new Date();
              jst7am.setUTCHours(22, 0, 0, 0);
              const options: Intl.DateTimeFormatOptions = {
                hour: "2-digit",
                minute: "2-digit",
                hour12: true,
              };
              return `${jst2am.toLocaleTimeString([], options)} to ${jst7am.toLocaleTimeString([], options)}`;
            })()}
          </p>
          <p>
            ALL Cabinets + e-amusement services offline. This is moved 1 day
            earlier if that day is a Japanese Holiday.
          </p>
        </div>
        <div className="flex justify-end"></div>
      </div>
    </Popup>
  );
};

export const GameNotes = (isMoe: boolean): Record<string, React.ReactNode> => ({
  sdvx: (
    <>
      <ul className={`mt-2 ${isMoe ? "text-pink-900" : "text-white"}`}>
        <li>
          • [USA] PREMIUM GENERATOR gacha available only ONLINE (No PASELI)
        </li>
        <li>• VP/VOLTEFACTORY rewards only available in Japan</li>
        <li>• [USA] Some cover art and/or charts have been removed </li>
        <li>• Official Online play is cross-region (including Japan)</li>
      </ul>
      <div className="flex justify-center">
        <EamuseMaintenancePopup isMoe={isMoe} />
      </div>
      <p
        className={`mt-3 ${isMoe ? "text-pink-800" : "text-pink-300"} text-right`}
      >
        Official e-amusement service in NA available only at Round1 USA
        <br />
        Online Cabinets in non-supported regions (CAN/EU/AUS) are on private
        networks which run older data
      </p>
    </>
  ),
  iidx: (
    <>
      <ul className={`mt-2 ${isMoe ? "text-pink-900" : "text-white"}`}>
        <li>
          • [USA] Certain e-amusement features such as video upload unavailable{" "}
        </li>
      </ul>
      <div className="flex justify-center">
        <EamuseMaintenancePopup isMoe={isMoe} />
      </div>
      <p
        className={`mt-3 ${isMoe ? "text-pink-800" : "text-pink-300"} text-right`}
      >
        Official e-amusement service in NA available only at Round1 USA
        <br />
        Online Cabinets in non-supported regions (CAN/EU/AUS) are on private
        networks which run older data
      </p>
    </>
  ),
  gitadora: (
    <>
      <div className="flex justify-center">
        <EamuseMaintenancePopup isMoe={isMoe} />
      </div>
      <p
        className={`mt-3 ${isMoe ? "text-pink-800" : "text-pink-300"} text-right`}
      >
        Official e-amusement service in NA available only at Round1 USA
        <br />
        Online Cabinets in non-supported regions (CAN/EU/AUS) are on private
        networks which run older data
      </p>
    </>
  ),
  dance_rush: (
    <>
      <div className="flex justify-center">
        <EamuseMaintenancePopup isMoe={isMoe} />
      </div>
      <p
        className={`mt-3 ${isMoe ? "text-pink-800" : "text-pink-300"} text-right`}
      >
        Official e-amusement service in NA available only at Round1 USA
        <br />
        Online Cabinets in non-supported regions (CAN/EU/AUS) are on private
        networks which run older data
      </p>
    </>
  ),
  dance_around: (
    <>
      <div className="flex justify-center">
        <EamuseMaintenancePopup isMoe={isMoe} />
      </div>
      <p
        className={`mt-3 ${isMoe ? "text-pink-800" : "text-pink-300"} text-right`}
      >
        Official e-amusement service in NA available only at Round1 USA
        <br />
        Online Cabinets in non-supported regions (CAN/EU/AUS) are on private
        networks which run older data
      </p>
    </>
  ),
  polaris_chord: (
    <>
      <div className="flex justify-center">
        <EamuseMaintenancePopup isMoe={isMoe} />
      </div>
      <p
        className={`mt-3 ${isMoe ? "text-pink-800" : "text-pink-300"} text-right`}
      >
        Official e-amusement service only in Japan.
      </p>
    </>
  ),
  ddr: (
    <>
      <div className="flex justify-center">
        <EamuseMaintenancePopup isMoe={isMoe} />
      </div>
      <p
        className={`mt-3 ${isMoe ? "text-pink-800" : "text-pink-300"} text-right`}
      >
        Official e-amusement service in NA available only at Round1 USA
        <br />
        Online Cabinets in non-supported regions (CAN/EU/AUS) are on private
        networks which run older data
      </p>
    </>
  ),
  jubeat: (
    <>
      <p
        className={`mt-3 ${isMoe ? "text-pink-800" : "text-pink-300"} text-center`}
      >
        Online only in Japan and Asia regions. No online service in the US (only
        old versions running offline-kit)
      </p>
      <p
        className={`mt-3 ${isMoe ? "text-pink-800" : "text-pink-300"} text-right`}
      >
        Online Cabinets in non-supported regions (CAN/EU/AUS) are on private
        networks which run older data
      </p>
    </>
  ),
  popn_music: (
    <>
      <p
        className={`mt-3 ${isMoe ? "text-pink-800" : "text-pink-300"} text-center`}
      >
        Online only in Japan and Asia regions. Japan and Asia only. No online
        service in the US (only old versions running offline-kit)
      </p>
      <p
        className={`mt-3 ${isMoe ? "text-pink-800" : "text-pink-300"} text-right`}
      >
        Online Cabinets in non-supported regions (CAN/EU/AUS) are on private
        networks which run older data
      </p>
    </>
  ),
  nostalgia: (
    <>
      <p
        className={`mt-3 ${isMoe ? "text-pink-800" : "text-pink-300"} text-center`}
      >
        Online only in Japan and Asia regions. Japan and Asia only. No online
        service in the US
      </p>
      <p
        className={`mt-3 ${isMoe ? "text-pink-800" : "text-pink-300"} text-right`}
      >
        Online Cabinets in non-supported regions (CAN/EU/AUS) are on private
        networks which run older data
      </p>
    </>
  ),
  chunithm_jp: (
    <>
      <p
        className={`mt-3 ${isMoe ? "text-pink-800" : "text-pink-300"} text-center`}
      >
        This version of the game is only available in Japan
      </p>
      <p
        className={`mt-3 ${isMoe ? "text-pink-800" : "text-pink-300"} text-center`}
      >
        You may be on the International version if you are outside of Japan
      </p>
    </>
  ),
  maimaidx_jp: (
    <>
      <p
        className={`mt-3 ${isMoe ? "text-pink-800" : "text-pink-300"} text-center`}
      >
        This version of the game is only available in Japan
      </p>
      <p
        className={`mt-3 ${isMoe ? "text-pink-800" : "text-pink-300"} text-center`}
      >
        You may be on the International version if you are outside of Japan
      </p>
    </>
  ),
  ongeki_jp: (
    <>
      <p
        className={`mt-3 ${isMoe ? "text-pink-800" : "text-pink-300"} text-center`}
      >
        Official service only in Japan. No International Version
      </p>
      <p
        className={`mt-3 ${isMoe ? "text-pink-800" : "text-pink-300"} text-center`}
      >
        You are on a private network if the cabinet is not in Japan
      </p>
    </>
  ),
  chunithm_intl: (
    <>
      <ul className={`mt-2 ${isMoe ? "text-pink-900" : "text-white"}`}>
        <li>
          • Updates behind JP version. International and JP are completely
          seperated
        </li>
      </ul>
      <p
        className={`mt-3 ${isMoe ? "text-pink-800" : "text-pink-300"} text-right`}
      >
        No official service in NA or EU.{" "}
        <a
          className="underline"
          href="https://location.am-all.net/alm/location?gm=104&lang=en"
        >
          See supported regions here
        </a>
      </p>
      <p
        className={`mt-3 ${isMoe ? "text-pink-800" : "text-pink-300"} text-right`}
      >
        If your region is not shown, you are likely on a private network
      </p>
    </>
  ),
  maimaidx_intl: (
    <>
      <ul className={`mt-2 ${isMoe ? "text-pink-900" : "text-white"}`}>
        <li>
          • Updates behind JP version. International and JP are completely
          seperated
        </li>
      </ul>
      <p
        className={`mt-3 ${isMoe ? "text-pink-800" : "text-pink-300"} text-right`}
      >
        No official service in NA or EU.{" "}
        <a
          className="underline"
          href="https://location.am-all.net/alm/location?gm=98"
        >
          See supported regions here
        </a>
      </p>
      <p
        className={`mt-3 ${isMoe ? "text-pink-800" : "text-pink-300"} text-right`}
      >
        If your region is not shown, you are likely on a private network
      </p>
    </>
  ),
  music_diver: (
    <>
      <p
        className={`mt-3 ${isMoe ? "text-pink-800" : "text-pink-300"} text-center`}
      >
        Online service available only at Round1 Japan and Round1 USA locations
      </p>
    </>
  ),
  wacca_plus: (
    <>
      <p
        className={`mt-3 ${isMoe ? "text-pink-800" : "text-white"} text-center`}
      >
        WACCA PLUS is a community continuation of WACCA REVERSE after online
        services ended in 2022
      </p>
      <p
        className={`mt-3 ${isMoe ? "text-pink-800" : "text-pink-300"} text-right`}
      >
        Runs on Mythos networked cabs. Not all cabinets have WACCA PLUS as these
        updates are opt-in by operators.
      </p>
    </>
  ),
  museca_plus: (
    <>
      <p
        className={`mt-3 ${isMoe ? "text-pink-800" : "text-white"} text-center`}
      >
        MÚSECA PLUS is a fan continuation project for MÚSECA 1+1/2.
      </p>
      <p
        className={`mt-3 ${isMoe ? "text-pink-800" : "text-pink-300"} text-right`}
      >
        Runs on various e-amusement private networks. Not all cabinets have
        MÚSECA PLUS as it is opt-in.
      </p>
      <p
        className={`mt-3 ${isMoe ? "text-pink-800" : "text-pink-300"} text-right`}
      >
        <a className="underline" href="https://museca.plus/downloads">
          You can also download it as a data_mod
        </a>
      </p>
    </>
  ),
  rb_deluxe_plus: (
    <>
      <p
        className={`mt-3 ${isMoe ? "text-pink-800" : "text-white"} text-center`}
      >
        A continuation of the abandoned iOS version of REFLEC BEAT (REFLEC BEAT plus)
      </p>
      <p
        className={`mt-3 ${isMoe ? "text-pink-800" : "text-pink-300"} text-right`}
      >
      Needs to be sideloaded once you get a hold of the IPA. Network features supported. iOS ONLY
      </p>
    </>
  )
});
