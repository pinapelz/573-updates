import React from "react";
import { NesicaMaintenancePopup, EamuseMaintenancePopup, AimeIntlMaintenanceInfo, AllnetPrivateServerWarning } from "./NoteModals";

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
      <div className="flex justify-center">
      <AllnetPrivateServerWarning isMoe={isMoe} />
      </div>
    </>
  ),
  idac: (
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
      <div className="flex justify-center">
      <AllnetPrivateServerWarning isMoe={isMoe} />
      </div>
    </>
  ),
  maimaidx_intl: (
    <>
      <div className="flex justify-center">
        <AimeIntlMaintenanceInfo isMoe={isMoe} />
      </div>
      <ul className={`mt-2 ${isMoe ? "text-pink-900" : "text-white"}`}>
        <li>
          • Updates behind JP version. International and JP are completely
          seperated
        </li>
        <li>
          • Certain charts are removed from USA region
        </li>
      </ul>
      <p
        className={`mt-3 ${isMoe ? "text-pink-800" : "text-pink-300"} text-right`}
      >
        Official service in USA/CAN/ASIA{" "}
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
        (No official service in EU)
      </p>
      <div className="flex justify-center">
        <AllnetPrivateServerWarning isMoe={isMoe} />
      </div>
    </>
  ),
  music_diver: (
    <>
      <div className="flex justify-center">
        <NesicaMaintenancePopup isMoe={isMoe} />
      </div>
      <p
        className={`mt-3 ${isMoe ? "text-pink-800" : "text-pink-300"} text-center`}
      >
        Online service available only at Round1 Japan and Round1 USA locations
      </p>
    </>
  ),
  street_fighter: (
    <>
      <div className="flex justify-center">
        <NesicaMaintenancePopup isMoe={isMoe} />
      </div>
      <p
        className={`mt-3 ${isMoe ? "text-pink-800" : "text-pink-300"} text-center`}
      >
        Online service in USA only at Round1 locations
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
      <p
        className={`mt-3 ${isMoe ? "text-pink-800" : "text-pink-300"} text-right`}
      >
        *Not in main feed as date data is unavailable from this source
      </p>
    </>
  ),
  taiko: (
    <>
      <p
        className={`mt-3 ${isMoe ? "text-pink-800" : "text-white"} text-center`}
      >
        Information below only applies to the latest version of the game (LCD + Banapassport Reader)
      </p>
      <p
        className={`mt-3 ${isMoe ? "text-pink-800" : "text-pink-300"} text-right`}
      >
        Maintenance time is 1am - 7am JST (i think?)<br/>Applies to USA cabs as well (9am - 3pm PST)
      </p>
    </>
  ),
  wmmt: (
    <>
      <p
        className={`mt-3 ${isMoe ? "text-pink-800" : "text-white"} text-center`}
      >
        Singular news feed for NA, ASIA/OCE, and JPN
      </p>
      <p
        className={`mt-3 ${isMoe ? "text-pink-800" : "text-pink-300"} text-right`}
      >
        All regions run different versions of the game
      </p>
    </>
  )
});
